import sys, json
from pathlib import Path

userid = sys.argv[1]

BASE_DIR = pathlib.Path().resolve()

def create_database():
    try:
        database = open(userdb.json, 'x', encoding='utf-8')
        return database
    except FileExistsError:
        return

def read_database():
    try:
        database = open(userdb.json, 'r', encoding='utf-8')
        return database
    except FileNotFoundError:
        return

def edit_database(name):
    pass

class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, firstname, surname, startingweight, weight, height):
        self.firstname = firstname
        self.surname =  surname
        self.startingweight = startingweight
        self.currentweight = weight
        self.height = height

    def set_weight(self, weight):
        self.currentweight = weight

    def __str__(self):
        return f'{self.surname}'

    def __repr__(self):
        return f'{self.firstname} {self.surname}' \
               f'{self.currentweight}' \
               f'{self.height}'

    def user_dict_create(self, firstname, surname, startingweight, currentweight, height):
        return {
            'firstname' : firstname,
            'surname' : surname,
            'starting weight' : startingweight,
            'current weight' : currentweight,
            'height' : height
            'weight history' : {
                date : startingweight
            }
        }

    def weight_entry(self, date, weight):
        '''Assigns a new weight entry to the dictionary with the date as the key'''
        self.user_dict['weight history'][date] = weight

    def weight_change(self):
        '''Averages all of the dictionary's entries and compares to starting weight and current weight'''
        total = 0
        for value in self.user_dict.values():
            total += value



def user_creation(user=None):
    if user == None:
       firstname = str(input("What is the user's first name?" ))
       surname = str(input("What is the user's surname?" ))
       startingweight = str(input("What is the user's starting weight? "))
       currentweight = str(input("What is the user's current weight? "))
       height = str(input("What is the user's height? "))
       print("Are these the correct values? ")
    else:


def main():
    if BASE_DIR.exists('userdb.json'):
        dbread = read_database()
        userid = str(input('Enter a user ID to query the database: '))
        if userid in dbread:
            json.load(userid, dbread)



    else:
        db = create_database()


if __name__ == '__main__':
    main()