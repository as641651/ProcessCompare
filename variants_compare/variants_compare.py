import pm4py
from pm4py.objects.log.obj import EventLog
from typing import List
from .dfg_compare import DFGCompare, gviz_dfg_diff

class VariantsCompare:
    def __init__(self, log:EventLog, variants_best:List, variants_worst:List, 
                 variants_id_key = "concept:name",
                activity_key="concept:name"):
        
        self.variants = variants_best + variants_worst
        self.best = variants_best.copy()
        self.worst = variants_worst.copy()
        
        self.log_filtered = pm4py.filter_log(lambda x: x.attributes[variants_id_key] in self.variants, log)
        self.log_best = pm4py.filter_log(lambda x: x.attributes[variants_id_key] in self.best, self.log_filtered)
        self.log_worst = pm4py.filter_log(lambda x: x.attributes[variants_id_key] in self.worst, self.log_filtered)
        
        self.dfg_compare = DFGCompare(self.log_filtered, self.log_best, self.log_worst,activity_key)
        ##TODO:
        # Footprints compare
        # Petrinets compare
                 
       
    def get_dfg_minus_best(self):
        return gviz_dfg_diff(self.dfg_compare.get_dfg(), self.dfg_compare.get_dfg_best())