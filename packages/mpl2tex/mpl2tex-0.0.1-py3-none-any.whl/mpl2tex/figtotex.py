import os
import shutil
import importlib
import subprocess

import matplotlib.pyplot as plt

class FigToTex:

    '''
    Class to dump figures to latex file. We will make a simple .tex file which can be loaded into a larger document. This prevents issues with such as tags and specialized preambles.
    
    For now all figures will be saved as an svg.

    folder structure
    main.tex
    plots/plot_type/fig.svg
    inputs/plot_type/fig.tex
    '''

    def __init__(self, plot_type:str, figures:list, outpath:str, commit_message = None):

        self.figures = figures
        self.outpath = outpath
        self.plot_type = plot_type

        number_of_newfigures = len(figures)

        if commit_message is None:
            commit_message = f'Added {number_of_newfigures} figures of plot type {plot_type}.'


        self.commit_message = commit_message

        self.setup_dir()
        self.plot_to_tex()
        self.update_maintex()
        self.log()
        
    def setup_dir(self):

        self.plot_path = os.path.join(self.outpath,'plots')
        self.input_path = os.path.join(self.outpath,'inputs')
        self.tex_path = os.path.join(self.input_path, f'{self.plot_type}.tex')
        self.main_tex_path = os.path.join(self.outpath,'main.tex')

        os.makedirs(self.plot_path, exist_ok = True)
        os.makedirs(self.input_path, exist_ok = True)

        if not os.path.exists(self.main_tex_path):
            template_path = importlib.resources.files('mpl2tex.template') / 'template.tex'
            shutil.copy(template_path, self.main_tex_path)

            proc = subprocess.run(['git','init','.'], cwd = self.outpath)


        
        for f in self.figures:
            f.add_plot_path(self.plot_path)


    def plot_to_tex(self):

        with open(self.tex_path, 'a') as f:
            for fig in self.figures:
                f.write(fig.figtotex())
                fig.savefig()

    def update_maintex(self):
        
        tmp_tex = self.main_tex_path.replace('.tex','tmp.tex')
        input_path = '/'.join(self.tex_path.split('/')[-2:])
        input_in_doc = False

        with open(tmp_tex, 'w') as tmptex:
            with open(self.main_tex_path, 'r') as maintex:
                for l in maintex:
                    if input_path in l:
                        input_in_doc = True
                    
                    elif '\\end{document}' in l and not input_in_doc:
                        tmptex.write(f'\\input{{{input_path}}}\n\n\\end{{document}}')
                        break

                    tmptex.write(l)
            
        os.remove(self.main_tex_path)
        os.rename(tmp_tex, self.main_tex_path)

    def log(self):

        subprocess.run(['git','add','.'], cwd = self.outpath)
        subprocess.run(['git','commit','-m', self.commit_message], cwd = self.outpath)

    def show_git_log(self):
        subprocess.run(['git','log'], cwd = self.outpath)

    def undo(self):
                
        proc = subprocess.Popen(['git','log'], stdout = subprocess.PIPE, cwd = self.outpath)
        out, error = proc.communicate()
        out = out.decode('utf-8')
        commit_id = out.split('\n')[0].split()[1]
        subprocess.run(['git','reset', '--hard', 'HEAD~1'], cwd = self.outpath) 
        print(f'Removed commit {commit_id}')


def figtotex(plot_type:str, figures:list, outpath:str):
    return FigToTex(plot_type=plot_type, figures=figures, outpath=outpath)
