import pygraphviz as pgv
import graphviz
from graphviz.graphs import Digraph
from pm4py.objects.log.obj import EventLog
import pm4py
from pm4py.visualization.dfg import visualizer as dfg_visualizer
from typing import Dict

def gviz_dfg_diff(dfg1:Digraph,
                  dfg2:Digraph, 
                  node_color='#F0B4B6',
                  edge_color='red',
                  orientation='TD'):

    """DFG difference: dfg1 - dfg2"""
    
    g1 = pgv.AGraph(dfg1.source)
    g2 = pgv.AGraph(dfg2.source)
    
    g1_node_id = {}
    g1_node_label = {}
    for node in g1.nodes():
        #skip start and end nodes
        if '@@' not in node.name:
            
            for i in range(3,6):
                if node.attr['label'][-i] == '(':     
                    label = node.attr['label'][:-i]
                    break

            g1_node_id[label] = node.name
            g1_node_label[node.name] = label
        else:
            g1_node_id[node.name] = node.name
            g1_node_label[node.name] = node.name
            
    g2_node_id = {}
    for node in g2.nodes():
        #skip start and end nodes
        if '@@' not in node.name:
            for i in range(3,6):
                if node.attr['label'][-i] == '(':     
                    label = node.attr['label'][:-i]
                    break
            g2_node_id[label] = node.name
        else:
            g2_node_id[node.name] = node.name
        
    # Node subtraction
    for k,v in g1_node_id.items():
        if "@@" not in k:
            node = g1.get_node(v)
            node.attr['label'] = k
            if k not in list(g2_node_id.keys()):
                node.attr['fillcolor'] = node_color
            else:
                node.attr['fillcolor'] = '#FFFFFF'
            
    # Edge subtraction
    for edge in g1.edges():
        n1_label = g1.get_node(edge[0]).attr['label']
        n2_label = g1.get_node(edge[1]).attr['label']
        
        try:
            n1_label = g1_node_label[g1.get_node(edge[0]).name]
            n2_label = g1_node_label[g1.get_node(edge[1]).name]
        except KeyError: #happens for start and end nodes
            continue
        
        try:    
            if (g2_node_id[n1_label], g2_node_id[n2_label]) not in g2.edges():
                edge.attr['color'] = edge_color
        except KeyError: #happens for nodes that doesnt exist in g2
            edge.attr['color'] = edge_color
        
    g1.graph_attr['rankdir'] = orientation
    return graphviz.Source(g1.string())


class DFGCompare:
    def __init__(self, log:EventLog, log_best:EventLog, log_worst:EventLog,
                activity_key:str = 'concept:name'):
        self.log = log
        self.log_best = log_best
        self.log_worst = log_worst
        self.activity_key = activity_key
        
        self._dfg = {}
        self._dfg_best = {}
        self._dfg_worst = {}
        
    def _store_dfg(self, log:EventLog, store_var:Dict ):
        if not store_var:
            dfg, im, fm = pm4py.discover_dfg(log, activity_key=self.activity_key)
            store_var['model'] = dfg
            store_var['im'] = im
            store_var['fm'] = fm
            
    def _get_dfg_gviz(self, dfg:Dict):
        
        dfg_parameters = dfg_visualizer.Variants.FREQUENCY.value.Parameters
        parameters = {}
        parameters[dfg_parameters.START_ACTIVITIES] = dfg["im"]
        parameters[dfg_parameters.END_ACTIVITIES] = dfg["fm"]
        
        return dfg_visualizer.apply(dfg["model"], parameters=parameters)
        
    
    def get_dfg(self) -> Digraph:
        if not self._dfg:
            self._store_dfg(self.log, self._dfg)
            
        return self._get_dfg_gviz(self._dfg)
    
    def get_dfg_best(self) -> Digraph:
        if not self._dfg_best:
            self._store_dfg(self.log_best, self._dfg_best)
            
        return self._get_dfg_gviz(self._dfg_best)
    
    def get_dfg_worst(self) -> Digraph:
        if not self._dfg_worst:
            self._store_dfg(self.log_worst, self._dfg_worst)
            
        return self._get_dfg_gviz(self._dfg_worst)  

