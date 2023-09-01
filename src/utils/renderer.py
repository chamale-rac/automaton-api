class Renderer:
    def __init__(self, directory):
        self.directory = directory

    def render(self, graph, name, identifier, format='svg'):
        '''
        Render the graph to a file

        :param graph: the graph to render
        :param name: the name of the file
        '''
        save_on = f'{self.directory}/{identifier}/{name}'
        graph.render(save_on,
                     format=format, cleanup=True)
        print('Rendered:', save_on)
