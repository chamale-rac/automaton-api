class Renderer:
    def __init__(self, directory='./imgs'):
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

    def web(self, graph, format='svg'):
        '''
        Generate a Graphviz render of the graph and return it as a byte string

        :param graph: the graph to render
        :param name: the name of the render
        :param identifier: the identifier of the render
        :param format: the format of the render (default: 'svg')
        :return: a byte string representing the Graphviz render
        '''
        return graph.pipe(format=format)
