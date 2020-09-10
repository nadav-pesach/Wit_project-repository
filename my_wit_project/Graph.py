import os


from graphviz import Digraph
from my_wit_project import my_wit_tools


def graph():
    # cant upload...trying to change file so will upload
    dst = my_wit_tools.find_parent_wit(os.getcwd())
    wit_dst = os.path.join(dst, '.wit')
    images_dst = os.path.join(wit_dst, 'images')
    try:
        with open(os.path.join(wit_dst, 'references.txt'), "r") as my_file:
            lines = my_file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError
    try:
        pre_name = [lines[0][5:45]]
    except UnboundLocalError:
        return 'failed.'
    # credit to https://graphviz.readthedocs.io/en/stable/examples.html#hello-py
    my_graph = Digraph(filename='luck', format='png', node_attr={'color': 'lightblue2', 'style': 'filled'})
    my_graph.attr(size='6,6')
    current_name = my_wit_tools.find_next_file_name(pre_name[0], images_dst)
    my_graph = my_wit_tools.my_fun_graph(pre_name, current_name, my_graph, images_dst)
    # while current_name:
    #     for pre in pre_name:
    #         print('pre', pre)
    #         for current in current_name:
    #             print('c', current)
    #             my_graph.edge(pre, current)
    #     pre_name = current_name
    #     current_name = my_wit_tools.find_next_file_name(current_name, images_dst)
    # while current_name:
    #     for current in current_name:
    #         my_graph.edge(pre_name, current)
    #     pre_name = current_name
    #     current_name = my_wit_tools.find_next_file_name(current_name, images_dst)
    my_graph.view()
# Reupload
