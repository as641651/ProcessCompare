import pm4py
from pm4py.objects.log.obj import EventLog
from typing import List
from .dfg_compare import DFGCompare, gviz_dfg_diff, gviz_dfg_diff2
from pm4py.visualization.petri_net import visualizer as pn_visualizer

class VariantsCompare:
    def __init__(self, log:EventLog, variants_best:List, variants_worst:List, 
                 variants_id_key = "concept:name",
                activity_key="concept:name"):
        
        self.variants = variants_best + variants_worst
        self.best = variants_best.copy()
        self.worst = variants_worst.copy()
        self.variants_id_key = variants_id_key
        
        self.log_filtered = pm4py.filter_log(lambda x: x.attributes[variants_id_key] in self.variants, log)
        self.log_best = pm4py.filter_log(lambda x: x.attributes[variants_id_key] in self.best, self.log_filtered)
        self.log_worst = pm4py.filter_log(lambda x: x.attributes[variants_id_key] in self.worst, self.log_filtered)
        
        self.dfg_compare = DFGCompare(self.log_filtered, self.log_best, self.log_worst,activity_key)
        ##TODO:
        # Footprints compare
        # Petrinets compare
                 
    def show_petrinet(self, variants_list:List, activity_key='concept:name'):
        log = pm4py.filter_log(lambda x: x.attributes[self.variants_id_key] in variants_list, self.log_filtered)
        net, im, fm = pm4py.discover_petri_net_inductive(log,activity_key=activity_key)
        return pn_visualizer.apply(net,im,fm)

    def get_dfg_minus_best(self, orientation='TD'):
        return gviz_dfg_diff(self.dfg_compare.get_dfg(), self.dfg_compare.get_dfg_best(),orientation=orientation)

    def get_dfg_minus_best_worst(self, orientation='TD'):
        return gviz_dfg_diff2(self.dfg_compare.get_dfg(), 
                            self.dfg_compare.get_dfg_best(), 
                            self.dfg_compare.get_dfg_worst(),
                            orientation=orientation)