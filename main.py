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
    except FileExistsError as error:
        print(error)


def read_database():
    '''Opens the database for data retrieval. The file should be closed when finished'''
    try:
        database = open('userdb.json', 'r', encoding='utf-8')
        return database
    except FileNotFoundError as error:
        print(error)


def edit_database(user):
    '''Overwrites the database with new data and closes the file'''
    try:
        with open('userdb.json', 'w', encoding='utf-8') as dbedit:
            pass
    except KeyError as error:
        print(error)
        print('Please provide another username to query the database')

def append_database(user):
    '''Appends a new user to the database and closes the file'''
    try:
        with open('userdb.json', 'a', encoding='utf-8') as dbedit:
            pass
    except KeyError as keyerror:
        print(keyerror)

class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, username, firstname, surname, startingweight, weight, height, weight_history=None):
        self.user_dict = self.user_dict_create(username, firstname, surname, startingweight, weight, height)
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.starting_weight = startingweight
        self.current_weight = currentweight
        self.height = height

    def set_weight(self, weight):
        self.currentweight = weight

    def __repr__(self):
        return f'{self.user_dict}'

    def user_dict_create(self, username, firstname, surname, startingweight, currentweight, height, date):
        return {
            'username': username,
            'firstname': firstname,
            'surname': surname,
            'starting weight': startingweight,
            'current weight': currentweight,
            'height': height,
            'weight history': {
                date: startingweight
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

def create_user():
    username = input("Enter a valid username: ")
    firstname = input("What is the user's first name?")
    surname = input("What is the user's surname?")
    startingweight = input("What is the user's starting weight? ")
    currentweight = input("What is the user's current weight? ")
    height = input("What is the user's height? ")

    print(
        f'Username: {username}\n'
        f'Name: {firstname} {surname}\n'
        f'Starting weight: {startingweight}\n'
        f'Current weight: {currentweight}\n'
        f'Height: {height}'
    )
    userinput = (input("Is this information correct? Type 'Yes' or 'no.'").lower()
    if userinput == 'yes':
        user = User(username, firstname, surname, startingweight, currentweight, height, weight_history)
        return user
    elif userinput == 'no':
        pass
    else:
        print("Please only enter 'Yes' or 'no.'")

def existing_user(user):
    username = user['username']
    firstname = user['firstname']
    surname = user['surname']
    startingweight = user['starting weight']
    currentweight = user['current weight']
    height = user['height']
    weight_history = user['weight history']

    user = User(username, firstname, surname, startingweight, currentweight, height, weight_history)
    return user

def user_handler(user=None):
    if user == None:
        new_user = create_user()
        return new_user

    else:
        old_user = existing_user(user)
        return old_user

def main():
    selection = input("Type 'New user' to begin user creation or 'existing user' to access an existing user.").lower()
    if selection == 'new user':
        pass
    elif selection == 'existing user':
        pass
    else:
        pass

    if BASE_DIR.exists('userdb.json'):
        dbread = read_database()
        user = input('Enter a username to query the database: ')
        try:
            if user in dbread:
                user = json.load(userid, dbread)
        except KeyError as error:
            print(error)
            print('Incorrect username provided. Please provide another')
        user_obj = user_creation(user)
    else:
        db = create_database()

if __name__ == '__main__':
    main()