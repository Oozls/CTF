# -*- coding: utf-8 -*-

from matplotlib import font_manager, rc, rcParams
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import os, sys, json

class Main():
    def __init__(self):
        os.system('cls')
        print('CTF Statistic Mode\n')

        # Setting Location #
        if getattr(sys, 'frozen', False):
            self.dir_path = os.path.split(sys.executable)[0]
        else:
            self.dir_path = os.path.split(__file__)[0]
        self.record_path = os.path.join(self.dir_path, 'record.json')

        # Setting Options #
        self.graph_type = input('--------------------\n'
                                '1. Bar Graph\n'
                                '--------------------\n'
                                'Select Graph Type... ')
        
        self.column_count = input('Type Column Count... ')
        if not self.column_count.isdigit():
            print('Unexpected Column Count Entered')
            os.system('pause')
        elif int(self.graph_type) <= 0:
            print('Unexpected Column Count Entered')
            os.system('pause')
        self.column_count = int(self.column_count)

        # Getting Data #
        if not os.path.exists(self.record_path):
            print('Data Not Found\nResearch First!')
            os.system('pause')
        with open(self.record_path, "r", encoding='utf-8') as file:
            self.data = json.load(file)
        print('Loaded Data')

        if self.graph_type == '1': self.bar()
        os.system('pause')

    def bar(self):

        # Setting Font #
        font_path = "C:/Windows/Fonts/malgunsl.ttf"
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)
        rc('xtick', labelsize=5)

        # Disabling Toolbar #
        rcParams['toolbar'] = 'None'

        # Transforming Data #
        data = dict(sorted(self.data.items(), key=lambda item: item[1], reverse=True))
        data = OrderedDict(list(data.items())[:self.column_count])

        x = np.arange(len(data))
        plt.bar(x, data.values())
        plt.xticks(x, data.keys(), rotation=45)

        plt.show()
        print('Showed Graph')