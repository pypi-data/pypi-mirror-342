import aidge_core

def remove_optional_inputs(graph_view: aidge_core.GraphView):
    """ Remove optional inputs from the ordered_list of the model

    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.graph_view
    """

    inputNodes = []
    for n in graph_view.get_ordered_inputs():
        if not (int(n[0].get_operator().input_category(n[1])) & int(aidge_core.InputCategory.Optional)):
            inputNodes.append(n)
    graph_view.set_ordered_inputs(inputNodes)
