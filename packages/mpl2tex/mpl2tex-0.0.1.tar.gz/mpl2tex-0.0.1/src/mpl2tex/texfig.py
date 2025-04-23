import datetime
import os


class TexFig:

    '''
    Keeping the TexFig as a seperate class to allow for easier updating in the future
    figure: matplotlib figure
    title: figure title
    caption: figure caption
    figure_filename: name of figure can be generated automatically
    figure_size: set relative to tex width

    
    Need to still implement labels.
    '''


    def __init__(self, figure, title, caption, figure_filename=None, subfigure = False, figure_size = 0.45, output_type = '.pdf'):

        self.figure = figure
        self.title = title
        self.caption = caption
        self.figure_size = figure_size
        self.subfigure = subfigure
         
        if figure_filename is None:
            figure_filename = title.lower().replace(' ','_')


        date_now = datetime.datetime.now()
        date_id = date_now.strftime("%Y%m%d") 
        self.figure_filename = '_'.join([date_id, figure_filename]) + output_type
        

    def savefig(self): 
        if os.path.exists(self.figure_path):
            raise Exception(f'{self.figure_path} already exists! Please rename')

        self.figure.savefig(self.figure_path)

    def add_plot_path(self, plot_path):
        self.figure_path = os.path.join(plot_path, self.figure_filename)

    def figtotex(self):

        if self.figure_path == None:
            raise Exception('Must run add_plot_path method first!')

        figpath = '/'.join(self.figure_path.split('/')[-2:])

        if self.subfigure:
            tex_out = f'\n\t\\begin{{subcaptionblock}}[t]{{{self.figure_size}\\textwidth}}\n\t\t\\centering\n\t\t\\includegraphics[width = \\linewidth]{{{figpath}}}\n\t\t\\caption{{{self.caption}}}\n\t\\end{{subcaptionblock}}'
        else:
            tex_out = f'\n\\begin{{figure}}[tbhp]\n\t\\centering\n\t\\includegraphics[width = {self.figure_size}\\textwidth]{{{figpath}}}\n\t\\caption[{self.title}]{{\\textbf{{{self.title}}} {self.caption}}}\n\\end{{figure}}'
    

        return tex_out
    




class MPTexFig:

    '''
    This class takes list of TexFig and generates a subfigure. The goal is not perfection, but rather documentation.
    '''

    def __init__(self, figures, title, caption):
        
        self.figures = figures
        self.title = title
        self.caption = caption

        
    def savefig(self):
        for fig in self.figures:
            fig.figure.savefig(fig.figure_path)


    def add_plot_path(self, plot_path):
        for fig in self.figures:
            fig.add_plot_path(plot_path)

    def figtotex(self):

        tex_out = f'\n\\begin{{figure}}[tbhp]\n\t\\centering'

        for f in self.figures:
            tex_out += f.figtotex() + '\n\t\\hfill'

        tex_out += f'\n\t\\caption[{self.title}]{{\\textbf{{{self.title}}} {self.caption}}}\n\\end{{figure}}'

        return tex_out