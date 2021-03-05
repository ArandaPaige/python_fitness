import sys, json
from pathlib import Path

userid = sys.argv[1]

BASE_DIR = pathlib.Path().resolve()

if BASE_DIR.exists('database.txt'):
    with open('database.txt'), 'r', encoding='utf-8') as dbread:
        try:
            if userid in dbread:
                pass
        except ValueError:
            return f''

else:
    with open('database.txt'), 'w', encoding='utf-8') as dbcreate:
        try:
            dbcreate.write()

def main():
    pass

class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, *args, **kwargs):
        self.firstname = firstname
        self.surname =  surname
        self.startingweight = startingweight
        self.currentweight = weight
        self.height = height
        self.weight_history = {}

    def set_weight(self, weight):
        self.currentweight = weight

    def __str__(self):
        return f'{self.surname}'

    def __repr__(self):
        return f'{self.firstname} {self.surname}' \
               f'{self.weight}' \
               f'{self.height}'

    def weight_entry(self, date, weight):
        '''Assigns a new weight entry to the dictionary with the date as the key'''
        self.weight_history[date] = weight

    def weight_change(self):
        '''Averages all of the dictionary's entries and compares to starting weight and current weight'''
        total = 0
        for values in self.weight_history.values():
            total += value



def user_creation():
    pass

if __name__ == '__main__':
    main()