# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 17:43:44 2017

@author: natasha1_Yang
"""

#Graphviz(dot语言)是支持所想即所得,图概念中的dot（节点）和edge（边）的概念来处理流程图
import graphviz as gv
import pygraphviz as pgv

def pagerank(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}

    min_value = (1.0 - damping_factor)/graph_size
    pagerank = dict.fromkeys(nodes, 1.0)
    for i in range(max_iterations):
        diff = 0
        for node in nodes:
            rank = min_value
            for referring_page in graph.incidents(node):
                rank += damping_factor * pagerank[referring_page] / len(graph.neighbors(referring_page))
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        print 'This is NO.%s iteration' % (i+1)
        print pagerank
        print ''
        
        if diff < min_delta:
            break
    
    return pagerank
    
if __name__ == "__main__":
    gr = gv.Digraph();
    gr.add_node(["1","2","3","4"])
    gr.add_edge(("1","2"))
    gr.add_edge(("1","3"))
    gr.add_edge(("1","4"))
    gr.add_edge(("2","3"))
    gr.add_edge(("2","4"))
    gr.add_edge(("3","4"))
    gr.add_edge(("4","2"))
    
    gr = pgv.AGraph()
    gr.add_node(["1","2","3","4"])
    gr.add_edge(("1","2"))
    gr.add_edge(("1","3"))
    gr.add_edge(("1","4"))
    gr.add_edge(("2","3"))
    gr.add_edge(("2","4"))
    gr.add_edge(("3","4"))
    gr.add_edge(("4","2"))
    pgr = pgv.AGraph('simple.dot')
    pgr.layout("dot")
    pgr.draw('simple.png')
    