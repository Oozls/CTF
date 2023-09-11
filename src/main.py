# -*- coding: utf-8 -*-

import os
import research, statistic

class Main():
    def __init__(self):
        os.system('cls')
        self.operation = input('--------------------\n'
                               '1. Research Roblox Games/Places\n'
                               '2. Show Statistics\n'
                               '--------------------\n'
                               'Select Operation... ')
        if self.operation.strip() == '1':
            self.main_r = research.Main()
        elif self.operation.strip() == '2':
            self.main_s = statistic.Main()
        else:
            print('Unexpected Operation Entered.')
            os.system('pause')            


if __name__ == '__main__':
    main = Main()