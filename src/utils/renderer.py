class Renderer:
    def __init__(self, directory, identifier):
        self.directory = directory
        self.identifier = identifier

    def render(self, graph, name, format='svg'):
        '''
        Render the graph to a file

        :param graph: the graph to render
        :param name: the name of the file
        '''
        save_on = f'{self.directory}/{self.identifier}/{name}'
        graph.render(save_on,
                     format=format, cleanup=True)
        print('Rendered:', save_on)
