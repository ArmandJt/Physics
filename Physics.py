from DM import DM
from anaexam import Reader
from colles import Colloscope

print('Loading... ')

class User():
    def __init__(self, anaexam_path, colloscope_path, dm_path, ds_path):
        self.colloscope = Colloscope(colloscope_path)
        self.anaexam = Reader(anaexam_path)
        self.dm = DM(dm_path, ds_path)

    def launch(self):
        self.comm = ''
        self.anaexam.setup()
        while self.comm != 'E':
            self.comm = input('[...] ').upper()
            self.execute()

    def execute(self):
        if 'COLLE' in self.comm:
            self.colloscope.info(self.comm.split(' ')[-1])
        elif self.comm == 'DRAW':
            self.anaexam.draw()
        elif 'DRAW ' in self.comm:
            if self.comm[5] == '-':
                names = list(self.anaexam.rank.keys())[eval(self.comm[5:]):]
            elif self.comm[5] in '0123456789':
                names = list(self.anaexam.rank.keys())[:eval(self.comm[5:])]
            else:
                names = self.comm[5:].split(' ')
            if 'DE' in names: names.remove('DE')
            if 'EL' in names: names.remove('EL')
            self.anaexam.draw_students(names)
        elif self.comm == 'HELP':
            print('Options:\n\t'+('\n\t').join(['[name]: get your grades, average and rank in physics', 'STATS: get stats of physics class', 'DRAW [name(s), index]: draw the evolution of the class [name: draw evolution of specified student(s), index: draw top (negative values supported)]', 'DM: find for anny occurrence of any exercice in dm', 'COLLE [name]: get your colle planning for the week to come', 'LS: get list of students in alphabetical order','RANK: get rank of all the students','PROG: get you the physic colle program of the week','...']))
        elif 'STAT' in self.comm:
            self.anaexam.stats()
        elif 'DM' in self.comm:
            self.dm.load()
            self.dm.get_corr()
        elif self.comm == 'LS':
            print(', '.join(self.anaexam.avg.keys()))
        elif self.comm == 'RANK':
            print(', '.join(self.anaexam.rank.keys()))
        elif self.comm == 'PROG':
            self.colloscope.get_physInfo()
        else:
            for name in self.comm.split(' '):
                if 'DE' in name or 'EL' in name:
                    pass
                elif self.colloscope.get_group(name) != None:
                    self.anaexam.info(name)

User().launch()
print('Thanks for using me!')