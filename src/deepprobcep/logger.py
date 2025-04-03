from typing import List, Dict
from time import strftime


class Logger(object):
    def __init__(self):
        self.basic_info = dict
        self.log_list = List[dict]
        

    def write_to_file(self, name):
        columns = list(self.log_data.keys())
        lines = ['i,'+','.join(columns)]
        for i in self.indices:
            row = [str(i)]
            for c in columns:
                row.append(str(self.log_data[c].get(i, '')))
            lines.append(','.join(row))
        datetime = strftime('_%y%m%d_%H%M')
        filename = name+datetime+'.log'
        with open(filename, 'w')as f:
            f.write('\n'.join(lines))
        print("=========================== logger file saved ===========================")


    # ====================================================================#
    # ====================       old functions        ====================#
    # ====================================================================#
    # def log(self, name, index, value):
    #     if name not in self.log_data:
    #         self.log_data[name] = dict()
    #     i = bisect.bisect_left(self.indices, index)
    #     if i >= len(self.indices) or self.indices[i] != index:
    #         self.indices.insert(i, index)
    #     self.log_data[name][index] = value

    # def log_list(self, i, l):
    #     print("log_list",l)
    #     for e in l:
    #         self.log(e[0], i, e[1])

    # def old_write_to_file(self, name):
    #     columns = list(self.log_data.keys())
    #     lines = ['i,'+','.join(columns)]
    #     for i in self.indices:
    #         row = [str(i)]
    #         for c in columns:
    #             row.append(str(self.log_data[c].get(i, '')))
    #         lines.append(','.join(row))
    #     datetime = strftime('_%y%m%d_%H%M')
    #     filename = name+datetime+'.log'
    #     with open(filename, 'w')as f:
    #         f.write('\n'.join(lines))
    #     print("=========================== logger file saved ===========================")