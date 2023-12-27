from pypdf import PdfReader
import matplotlib.pyplot as plt
from os import *

"""
Program made by Armand Jamet 14.12.23
Handler of mpsi.dioptre data

Collects all the grades from all the students for each DS
Functionalities :
     - calculates the average of all the students, and calculate ranks from it
     - Give for each student the rank, the grades and the average
     - Draw each student grades evolution, sorted by rank counted from 0, from the end, by student...
     - Draw all statistics from the class : evolution of the grades, histogram, diagram
     And some more!
Have fun!
"""

class Reader():

    def __init__(self, folder):
        self.folder = folder
        self.isLoaded = 0

    def setup(self):
        self.coef = [1, 1, 1, 1/3, 1, 1, 1, 1]
        self.get_grades()
        self.grades_to_int()
        self.get_avg()
        self.get_rank()
        self.DS_avg()
        self.isLoaded = 1

    # Collects all the data of the DS in string
    def get_grades(self):
        self.gradeTxt = []
        self.DS = {}
        for file in listdir(self.folder):
            if 'anaexamen' in file:
                self.DS[file.removesuffix('-anaexamen.pdf')] = 'N/a'
                pdf = PdfReader(self.folder + '/' + file)
                rawText = pdf.pages[0].extract_text()
                croppedText = rawText.split('NOM Prénom Note Rang')[1]
                croppedText = croppedText.split(file[:2])[0]
                self.gradeTxt.append(croppedText)

    # Convert the string data collected in the function below to a dictionary with int
    def grades_to_int(self):
        self.grade = []
        for DS in range(len(self.DS)):
            self.grade.append({})
            for line in self.gradeTxt[DS].split('\n')[1:]:
                grade = line.split(' ')[-2]
                name = line.split(' ')[0].upper()
                if len(name) <= 2:
                    name = line.split(' ')[1].upper()
                if 'Feng' in grade: # Exception caused by a different layout of the grades
                    self.grade[DS]['BELMAR'] = 15.5
                elif grade[0] in list('0123456789'):
                    self.grade[DS][name] = eval(grade.replace(',', '.'))
                else:
                    self.grade[DS][name] = 'Abs'
                    # if you want to have some more precision from all the missing students
                    # print('\t', ' '.join(line.split(' ')[0:2]), 'was', line.split(' ')[-1], 'on DS', DS + 1)

    # Calculates average of the students
    def get_avg(self):
        print('Calculating averages...')
        self.avg = {}
        for student in list(self.grade[-2].keys()):
            avg = 0
            N = 0
            for DS in range(len(self.grade)):
                if self.grade[DS][student] != 'Abs':
                    avg += self.grade[DS][student] * self.coef[DS]
                    N += self.coef[DS]
            if N != 0:
                self.avg[student] = avg / N

    # Calculate the average of each DS
    def DS_avg(self):
        for DS in range(len(self.DS)):
            total = sum([mark if mark!='Abs' else 0 for mark in self.grade[DS].values()])
            N = len(self.grade[DS].values()) - list(self.grade[DS].values()).count('Abs')
            self.DS[list(self.DS.keys())[DS]] = total / N

    def get_rank(self):
        print('Ranking...')
        sorted_dict = dict(sorted(self.avg.items(), key=lambda item: item[1], reverse=True))
        self.rank = {name: rank + 1 for rank, (name, value) in enumerate(sorted_dict.items())}

    # Draw evolution of each student (grade in function of the DS)
    def draw_students(self, names, soloRun = 1):
        fig, ax = plt.subplots()
        ax.set_ylim((0, 20))
        plt.xlabel('DS')
        plt.ylabel('Grade')
        plt.plot(list(range(len(self.DS))), list(self.DS.values()), color =  'red')
        for student in names:
            try:
                self.draw_grade(student)
            except:
                print('Something wrong...')
        plt.title('Grade of %s\n average in red'%(', '.join(names)))
        if soloRun:
            plt.show()

    def info(self, name):
        print('%s (in physics):\n\tAverage: %s\n\tRank: %s /%s\n\tGrades: %s' % (
            name, str(self.avg[name]), str(self.rank[name]), str(len(self.avg)),
            ', '.join([str(self.grade[DS][name]) for DS in range(len(self.grade))])))

    def stats(self):
        maj = min(self.rank, key=lambda k: self.rank[k])
        minorant = max(self.rank, key=lambda k: self.rank[k])
        print('Max: %s, avg: %s\nMin: %s, avg: %s' % (maj, self.avg[maj], minorant, self.avg[minorant]))
        print('Class avg.', sum(self.avg.values()) / len(self.avg))

    def draw_grade(self, student):
        plt.plot(range(len(self.grade)),
                 [self.grade[DS][student] if self.grade[DS][student] != 'Abs' else None for DS in
                  range(len(self.grade))])

    # Draw all stuff possible
    def draw(self):
        self.draw_students(list(self.rank.keys()), 0)
        plt.figure()
        plt.xlim(0, 20)
        plt.hist(self.avg.values())
        plt.title('Histogram of Average Grades')
        plt.xlabel('Average Grade')
        plt.ylabel('Frequency')
        plt.figure()
        plt.ylim(0, 20)
        plt.bar(self.avg.keys(), self.avg.values())
        plt.title('Bar Chart of Average Grades')
        plt.xlabel('Student')
        plt.ylabel('Average Grade')
        plt.show()

