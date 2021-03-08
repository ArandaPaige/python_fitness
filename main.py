import sys, json, pathlib
from pathlib import Path

userid = sys.argv[1]

BASE_DIR = pathlib.Path().resolve()

def create_database():
    '''Exclusively creates and opens a new database if one does not exist.'''
    try:
        database = open('userdb.json', 'x', encoding='utf-8')
        database.close()
        return
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
    except KeyError as keyerror:
        print(keyerror)
        print('Please provide another username to query the database')
    except FileNotFoundError as fnferror:
        print(fnferror)

def append_database(user):
    '''Appends a new user to the database and closes the file'''
    try:
        with open('userdb.json', 'a', encoding='utf-8') as dbedit:
            dbedit.write()
            json.dump(user, dbedit)
    except KeyError as keyerror:
        print(keyerror)
    except FileNotFoundError as fnferror:
        print(fnferror)

class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, username, firstname, surname, startingweight, currentweight, height, weight_history=None):
        self.user_dict = self.user_dict_create(username, firstname, surname, startingweight, currentweight, height)
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
        f'1. Username: {username}\n'
        f'2. Name: {firstname} {surname}\n'
        f'3. Starting weight: {startingweight}\n'
        f'4. Current weight: {currentweight}\n'
        f'5. Height: {height}'
    )

    userinput = input("Is this information correct? Type 'Yes' or 'no.'").lower()

    if userinput == 'yes':
        user = User(username, firstname, surname, startingweight, currentweight, height, weight_history)
    elif userinput == 'no':
        userchange = input("What would you like to change?")
    else:
        print("Please type only 'Yes' or 'no'")

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

def user_selection(database):
    '''
    A selection menu for querying a new or existing user. A new user will be required to generate a unique user object.
    Existing users will have their information loaded from the database provided.
    :param database: accepts a database entity as a parameter for querying
    :return: returns a User object
    '''
    while True:
        selection = input("Type 'New user' to begin user creation or 'existing user' to access an existing user.").lower()
        if selection == 'new user':
            new_user = user_handler()
            return new_user
        elif selection == 'existing user':
            username = input('Please type your username in to query the database: ')
            try:
                if username in database:
                    user = json.load(user)
                    old_user = user_handler(user)
                    return old_user
            except KeyError as error:
                print(error)
                print("That username was not in the database. Please make sure you typed it in correctly.")
            old_user = existing_user()
        else:
            print('Please enter a valid selection.')

def user_menu(user):
    pass

def main():
    if BASE_DIR.exists('userdb.json') == False:
        create_database()
        dbread = read_database()
    else:
        dbread = read_database()
    user = user_selection(dbread)


if __name__ == '__main__':
    main()