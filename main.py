import sys, json
from pathlib import Path

userid = sys.argv[1]

BASE_DIR = pathlib.Path().resolve()

def create_database():
    '''
    Exclusively creates and opens a new database if one does not exist. The file should be closed when finished
    '''
    try:
        database = open('userdb.json', 'x', encoding='utf-8')
        return database
    except FileExistsError:
        return

def read_database():
    '''Opens the database for data retrieval. The file should be closed when finished'''
    try:
        database = open('userdb.json', 'r', encoding='utf-8')
        return database
    except FileNotFoundError:
        return

def edit_database(user):
    '''Overwrites the database with new data and closes the file'''
    try:
        with open('userdb.json', 'w', encoding='utf-8') as dbedit:
            pass
    except KeyError:
        return f'Username not found'

def append_database(user):
    '''Appends a new user to the database and closes the file'''
    try:
        with open('userdb.json', 'a', encoding='utf-8') as dbedit:
            pass
    except:
        pass

class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, username, firstname, surname, startingweight, weight, height, weight_history=None):
        self.user_dict = self.user_dict_create(username, firstname, surname, startingweight, weight, height)

    def set_weight(self, weight):
        self.currentweight = weight

    def __str__(self):
        return f'{self.surname}'

    def __repr__(self):
        return f'{self.firstname} {self.surname}' \
               f'{self.currentweight}' \
               f'{self.height}'

    def user_dict_create(self, username, firstname, surname, startingweight, currentweight, height):
        return {
            'username' : username,
            'firstname' : firstname,
            'surname' : surname,
            'starting weight' : startingweight,
            'current weight' : currentweight,
            'height' : height,
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
       username = str(input("Enter a valid username: "))
       firstname = str(input("What is the user's first name?" ))
       surname = str(input("What is the user's surname?" ))
       startingweight = str(input("What is the user's starting weight? "))
       currentweight = str(input("What is the user's current weight? "))
       height = str(input("What is the user's height? "))
       print("Are these the correct values? ")
    else:
        user = User(username, firstname, surname, startingweight, currentweight, height, weight_history)


def main():
    if BASE_DIR.exists('userdb.json'):
        dbread = read_database()
        userid = str(input('Enter a username  to query the database: '))
        try:
            if userid in dbread:
                user = json.load(userid, dbread)
        except KeyError:
            pass
        user_obj = user_creation(user)
    else:
        db = create_database()


if __name__ == '__main__':
    main()