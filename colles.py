import datetime
from requests import get
from bs4 import BeautifulSoup

"""
Made by Armand JAMET the 17.12.23,
Just a program taking the colle planing of a student
Also auto-giving the Physic colles program to those who need it

Takes a copy of the colloscope and output a much more convenient dictionary
You can see an exemple of if on the function above
"""

class Colloscope():

    def __init__(self):
        self.colles = []
        self.date, self.week, self.colloscope = None, None, None

    # Convert the text of the colloscope to a dictionary, with all the data fetched
    def text_to_dict(self, txt):
        collo = {'Maths': {}, 'Phys': {}, 'Anglais': {}, 'Lettres': {}}
        for line in txt.split('\n'):
            lineTxt = line.split(' ')
            if not lineTxt[1] in collo[lineTxt[0]].keys():
                collo[lineTxt[0]][lineTxt[1]] = {}
            collo[lineTxt[0]][lineTxt[1]][lineTxt[2] + ' ' + lineTxt[3]] = [int(num) for num in line.split('h ')[1].split(' ')]
        return collo

    # Returns the colloscope in function of the week
    def get_colloscope(self):
        # The colloscope have been hidden since I don't want to have any trouble with the teachers
        if self.week < 15:
            return None
        else:
            raise Exception('Please contact Armand JAMET:\nThe colle database is not updated, do your job man')

    # Get the group of a specific student given his name
    def get_group(self, name):
        # Note: The students groups have been hidden since I don't hav ethe right to use their names ig
        try:
            return {}[name]
        except KeyError:
            return None

    # Main function, handle pretty much all th functionalities of the program
    def info(self, name):
        if self.get_group(name) == None:
            return 'Le nom renseigné est incorrect, merci de réessayer'
        self.group = self.get_group(name)

        # Get week
        month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        date = str(datetime.datetime.today())[:10]
        self.date = [date[8:10], date[5:7], date[2:4]]  # JJ/MM/YY
        self.week = (sum(month_lengths[0:int(self.date[1]) - 1]) + int(self.date[0]) - 1 - sum(
            month_lengths[0:9]) + 18) // 7 - 1

        # This is pretty much self-explanatory
        self.colloscope = self.get_colloscope()

        # Gets the full planning of colles coming next week
        for subject in self.colloscope.keys():
            for teacher in self.colloscope[subject].keys():
                for date in self.colloscope[subject][teacher].keys():
                    if self.colloscope[subject][teacher][date][self.week - 1] == self.group:
                        self.colles.append({'subject': subject, 'teacher': teacher, 'date': date})

        date = '%s %s 20%s:' % (self.date[0],
                                ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre',
                                 'octobre', 'novembre', 'décembre'][int(self.date[1]) - 1], self.date[2])

        print('Colles de la semaine du ' + date)
        for colle in self.colles:
            print('\t- le %s, %s avec %s' % (colle['date'], colle['subject'], colle['teacher']))
        # If we have an original...
        if name == 'JAMET' and self.week % 2 != 0:
            print('\t- T\'as allemand')

        # Check if the student have a Physic colle this week
        if sum(['Phys' == colle['subject'] for colle in self.colles]) > 0:
            if input('Programme de colle de Physique ? [type nothing if yes] ') == '':
                try:
                    self.get_physInfo()
                except ConnectionError:
                    print('Please connect to internet to download Physics colle')

    # Get the Physic's colle from his website
    # The data processing (if we can call this like that) is made using BeautifulSoup
    def get_physInfo(self):
        soup = BeautifulSoup(get('https://mpsi.dioptre.fr/colles.html').text, features="html.parser")
        content = soup.find_all('ul')[self.week - 1]
        print('Question de cours :')
        print(' ** ' + '\n ** '.join(
            '\n\t\t'.join(str(content).split('Question de cours : ')[1].split('</li>')[0].split(', ')).split('. ')))
        print('Exercice :')
        print('\t' + '\n\t'.join(str(content).split('Exercice : ')[1].split('</li>')[0].split('. ')))
