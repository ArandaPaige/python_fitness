import sys, json, pathlib

from pathlib import Path

BASE_DIR = pathlib.Path().resolve()
DATABASE = BASE_DIR / 'userdb.json'


def create_database():
    '''Exclusively create a new database.'''
    try:
        database = open('userdb.json', 'x', encoding='utf-8')
        database.close()
        return
    except FileExistsError as error:
        print(error)


def read_database():
    '''Open the database for data retrieval.'''
    try:
        database = open('userdb.json', 'r', encoding='utf-8')
        return database
    except FileNotFoundError as error:
        print(error)


def edit_database(user):
    '''Overwrite the database with new data.'''
    try:
        with open('userdb.json', 'w', encoding='utf-8') as dbedit:
            pass
    except KeyError as keyerror:
        print(keyerror)
        print('Please provide another username to query the database')
    except FileNotFoundError as fnferror:
        print(fnferror)


def append_database(user):
    '''Append a new user to the database.'''
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

    def __repr__(self):
        return f'{self.user_dict}'

    def set_weight(self, weight):
        self.currentweight = weight
        self.user_dict['current weight'] = weight

    def set_startweight(self, weight):
        self.startingweight = weight
        self.user_dict['starting weight'] = weight

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


def user_create_username():
    while True:
        username = input("Enter a valid username: ")
        return username


def user_create_names():
    while True:
        firstname = input("What is the user's first name: ")
        surname = input("What is the user's surname: ")
        return


def user_create_startweight():
    while True:
        startingweight = input("What is the user's starting weight in lbs: ")
        try:
            startingweight = float(startingweight)
            return startingweight
        except ValueError as error:
            print(error)
            print("Please type a valid number.")
            continue


def user_create_curweight():
    while True:
        currentweight = input("What is the user's current weight in lbs: ")
        try:
            currentweight = float(currentweight)
            return currentweight
        except ValueError as error:
            print(error)
            print("Please type a valid number.")
            continue


def user_create_height():
    while True:
        height = input("What is the user's height in inches: ")
        try:
            height = float(height)
            return height
        except ValueError as error:
            print(error)
            print("Please type a valid number.")
            continue


def create_user():
    while True:
        username = user_create_username()
        name = user_create_names()
        startingweight = user_create_startweight()
        currentweight = user_create_curweight()
        height = user_create_height()


        print(
            f'1. Username: {username}\n'
            f'2. Name: {name}\n'
            f'3. Starting weight: {startingweight}\n'
            f'4. Current weight: {currentweight}\n'
            f'5. Height: {height}'
        )

        userinput = input("Is this information correct? Type 'Yes' or 'no.'\n").lower()

        if userinput == 'yes':
            user = User(username, firstname, surname, startingweight, currentweight, height, weight_history)
            return user
        elif userinput == 'no':
            userchange = input("What would you like to change?")
        else:
            print("Please type only 'Yes' or 'no'")
            continue


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
        selection = input(
            "Type 'New user' to begin user creation or 'existing user' to access an existing user.\n").lower()
        if selection == 'new user':
            user_obj = user_handler()
            return user_obj
        elif selection == 'existing user':
            username = input('Please type your username in to query the database: ')
            try:
                if username in database:
                    user = json.load(username)
                    user_obj = user_handler(user)
                    return user_obj
            except KeyError as error:
                print(error)
                print("That username was not in the database. Please make sure you typed it in correctly.")
        else:
            print('Please enter a valid selection.')


def user_main_menu(user):
    while True:
        print(
            f'Username: {user.username}\n'
            f'Name: {user.firstname} {user.surname}\n'
            f'Starting weight: {user.startingweight}\n'
            f'Current weight: {user.currentweight}\n'
            f'Height: {user.height}'
        )
        print(
            f'Menu Options\n'
            f'1. New Weight Entry\n'
            f'2. Change Starting Weight\n'
            f'3. Update weight\n'
            f'4. Return to user selection\n'
        )
        selection = input("What is your selection? Type 'Quit' if you are finished.").lower()

        if selection == "1" or selection == "update weight":
            user_weight_change()
            continue
        if selection == "2":
            pass
        if selection == "3":
            pass
        if selection == "4":
            pass
        elif selection == 'quit':
            sys.exit()
        else:
            print("Please enter a valid selection.")

def user_date_entry():
    date_list = []
    while True:
        date_unchecked = input("Input a custom date in MM/DD/YYYY format or leave blank if you want it automatically logged")
        try:
            date_split = date_unchecked.split('/')
            continue
        except ValueError as error:
            print("Encountered invalid input. Please input a date in MM/DD/YYYY format.")
        for date in date_split:
            try:
                int(date)
                date_list.append(date)
            except ValueError as error:
                print("Non-numerical input encountered. Please type in valid numerical input in MM/DD/YYYY format.")
                continue
        if date_list[0] <= 0 or date_list[0] > 12:
            print('Invalid month entered. Please input a proper month in MM format.')
            continue
        if date_list[1] <= 0:
            print('Invalid day entered. Please input a proper day in DD format.')
            continue
        if date_list[2] > curyear:
            print("Please input a year equal to or before the current year. Future dates are not permissible.")
            continue


def user_weight_change(user):
    while True:
        weight = input("Please enter your new weight in imperial measurements.")
        try:
            weight = float(weight)
            break
        except ValueError as error:
            print(error)
            print("Please input a valid number.")
            continue
    date = user_date_entry()
    user.set_weight(weight)
    user.weight_entry(weight, date)
    return


def main():
    if DATABASE.exists() == False:
        create_database()
        dbread = read_database()
    else:
        dbread = read_database()
    user = user_selection(dbread)
    user_main_menu(user)


if __name__ == '__main__':
    main()
