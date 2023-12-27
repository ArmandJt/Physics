from pypdf import *
from os import *

"""
Made by Armand Jamet the 19/12/22
Program made to search for a solution of the current week dm

Load the dm of this week, and the last dm and ds of the last year
Search for an exercice that have been used in the last year

Limitation: if the teachers use a different name for the problem
"""

class DM():

    def __init__(self, dm_path, ds_path):
        self.dm_path = dm_path
        self.ds_path = ds_path
    
    def load(self):
        self.annales = []
        self.dmTitles = []
        dms = []
        getPath = lambda: input('Please enter path of your DM\n\t$ ')

        # Search for the last dm there is in the Documents
        for file in listdir("C:/Users/jamet/OneDrive/Documents"):
            if 'DM' in file:
                dms.append(eval(file.removesuffix('.pdf')[2:4]))
        if len(dms) != 0:
            if input('Do you want to search for the DM%s ?\n[y/n] '%(str(max(dms)))) != 'n':
                self.path = 'C:/Users/jamet/OneDrive/Documents/DM%s.pdf'%(str(max(dms)))
            else:
                self.path = getPath()
        else:
            print('No DM have been found on Documents')
            self.path = getPath()

        try:
            self.dm = PdfReader(self.path)
        except Exception:
            raise Exception('Path of your DM is not correct. Please modify it')

        # Loads the dm and ds of the last year
        try:
            self.subjects = {}
            self.corrections = {}
            for doc in listdir(self.dm_path):
                if 'DM' in doc:
                    if 'corr' in doc:
                        self.corrections[doc[0:4] + '.pdf'] = PdfReader(self.dm_path + '/' + doc)
                    else:
                        self.subjects[doc] = PdfReader(self.dm_path + '/' + doc)
            for doc in listdir(self.ds_path):
                if 'DS' in doc:
                    if 'corr' in doc:
                        self.corrections[doc[0:4] + '.pdf'] = PdfReader(self.ds_path + '/' + doc)
                    else:
                        self.subjects[doc] = PdfReader(self.ds_path + '/' + doc)
        except Exception:
            raise Exception('Path of your annales is not correct. Please modify it\n' + self.dm_path)
        print('Loading successful')

    def search(self):
        # Gets all the names of the problems from the current DM
        for pb in '\n'.join([self.dm.pages[page].extract_text() for page in range(len(self.dm.pages))]).split(
                'Problème'):
            self.dmTitles.append(pb.split('\n')[0].split(':')[-1])

        # Search for an occurrence of a problem in the last year subjects
        for subject in self.subjects.keys():
            for pb in '\n'.join([self.subjects[subject].pages[page].extract_text() for page in
                                 range(len(self.subjects[subject].pages))]).split('Problème'):
                title = pb.split('\n')[0].split(':')[-1]
                for dmTitle in self.dmTitles:
                    if dmTitle.upper() == title.upper():
                        page = [dmTitle in self.subjects[subject].pages[page].extract_text() for page in
                                range(len(self.subjects[subject].pages))].index(1) + 1
                        page = page / len(self.subjects[subject].pages)
                        page = page * len(self.corrections[subject].pages)
                        self.annales.append([title, subject, page])

    def get_corr(self):
        print('Now searching...')
        self.search()

        # Output the result of the search to the user
        if len(self.annales) == 0:
            print('The output of the search is empty unfortunately...')
        else:
            input('The search has an output ! ')
            print('Result(s):')
            for names in self.annales:
                print('\t%s was a problem of the %s problem,' % (names[0], names[1]))
            input('Now proceding to open the files... ')
            for stuff in self.annales:
                input('The problem should be in page %s ' % (int(stuff[2])))
                if 'DM' in stuff[1]:
                    startfile(self.dm_path + '/' + stuff[1].removesuffix('.pdf') + '-corr.pdf')
                else:
                    startfile(self.ds_path + '/' + stuff[1].removesuffix('.pdf') + '-corr.pdf')