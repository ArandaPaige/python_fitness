import sys
import json
import pathlib
import datetime


BASE_DIR = pathlib.Path().resolve()
DATABASE = BASE_DIR / 'userdb.json'
DATETODAY = datetime.date.today()


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
            dbedit.write(f'Username: {user.username} - ')
            json.dump(user.user_dict, dbedit)
            dbedit.write(f'\n\n')
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

    def __init__(self, username, name, startingweight, currentweight, height, weight_history=None):
        self.user_dict = self.user_dict_create(username, name, startingweight, currentweight, height)
        self.username = username
        self.name = name
        self.starting_weight = startingweight
        self.current_weight = currentweight
        self.height = height

    def __repr__(self):
        return f'{self.user_dict}'

    def set_weight(self, weight=None):
        if weight == None:
            while True:
                weight = input("What is the user's current weight in lbs: ")
                try:
                    weight = float(weight)
                    break
                except ValueError as error:
                    print(error)
                    print("Please type a valid number.")
                    continue
        self.current_weight = weight
        self.user_dict['current weight'] = weight

    def set_startweight(self, weight):
        if weight == None:
            while True:
                weight = input("What is the user's starting weight in lbs: ")
                try:
                    weight = float(weight)
                    break
                except ValueError as error:
                    print(error)
                    print("Please type a valid number.")
                    continue
        self.starting_weight = weight
        self.user_dict['starting weight'] = weight

    def user_dict_create(self, username, name, startingweight, currentweight, height):
        return {
            'username': username,
            'name': name,
            'starting weight': startingweight,
            'current weight': currentweight,
            'height': height
        }

    def weight_entry(self, date, weight):
        '''Assign a new weight entry to the dictionary with the date as the key'''
        self.user_dict['weight history'][date] = weight

    def weight_change(self):
        '''Average all of the dictionary's entries and compares to starting weight and current weight'''
        total = 0
        for value in self.user_dict.values():
            total += value


def user_create_username(database):
    while True:
        username = input("Enter a valid username: ")
        if username in database:
            print('\nUsername is already taken. Please enter another.\n')
            continue
        else:
            return username


def user_create_name():
    while True:
        name = input('What is your first and last name: ')
        return name


def user_create_startweight():
    while True:
        startingweight = input("What is the user's starting weight in lbs: ")
        try:
            startingweight = float(startingweight)
            return startingweight
        except ValueError as error:
            print(error)
            print("\nPlease type a valid number.\n")
            continue


def user_create_curweight():
    while True:
        currentweight = input("What is the user's current weight in lbs: ")
        try:
            currentweight = float(currentweight)
            return currentweight
        except ValueError as error:
            print(error)
            print("\nPlease type a valid number.\n")
            continue


def user_create_height():
    while True:
        height = input("What is the user's height in inches: ")
        try:
            height = float(height)
            return height
        except ValueError as error:
            print(error)
            print("\nPlease type a valid number.\n")
            continue


def create_user(database):
    username = user_create_username(database)
    name = user_create_name()
    startingweight = user_create_startweight()
    currentweight = user_create_curweight()
    height = user_create_height()

    while True:
        print(
            f'1. Username: {username}\n'
            f'2. Name: {name}\n'
            f'3. Starting weight: {startingweight}\n'
            f'4. Current weight: {currentweight}\n'
            f'5. Height: {height}'
        )

        userinput = input("Is this information correct? Type 'Yes' or 'no.'\n").lower()

        if userinput == 'yes':
            user = User(username, name, startingweight, currentweight, height)
            append_database(user)
            return user
        elif userinput == 'no':
            userchange = input("What would you like to change? ").lower()
            if userchange == '1' or userchange == 'username':
                username = user_create_username(database)
                continue
            elif userchange == '2' or userchange == 'name':
                name = user_create_name()
                continue
            elif userchange == '3' or userchange == 'starting weight':
                startingweight = user_create_startweight()
                continue
            elif userchange == '4' or userchange == 'current weight':
                currentweight = user_create_curweight()
                continue
            elif userchange == '5' or userchange == 'height':
                height = user_create_height()
                continue
            else:
                print("\nPlease type in a valid response.\n")
                continue
        else:
            print("\nPlease type only 'Yes' or 'no'\n")
            continue


def existing_user(user):
    username = user['username']
    name = user['name']
    startingweight = user['starting weight']
    currentweight = user['current weight']
    height = user['height']
    weight_history = user['weight history']

    user = User(username, name, startingweight, currentweight, height, weight_history)
    return user


def retrieve_user(database):
    while True:
        username = input('Please type your username in to query the database: ')
        if username in database:
            try:
                user = json.load()
                print(user)
                return user
            except:
                e = sys.exc_info()[0]
                print(e)
                continue
        else:
            print(f'\n{username} was not found in the database. Please enter another username.\n')


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
            user_obj = create_user(database)
            return user_obj
        if selection == 'existing user':
            user = retrieve_user(database)
            user_obj = existing_user(user)
            return user_obj
        else:
            print('\nPlease enter a valid selection.\n')


def user_main_menu(user):
    while True:
        print(
            f'Username: {user.username}\n'
            f'Name: {user.name}\n'
            f'Starting weight: {user.starting_weight}\n'
            f'Current weight: {user.current_weight}\n'
            f'Height: {user.height}'
        )
        print(
            f'Menu Options\n'
            f'1. New Weight Entry\n'
            f'2. Change Starting Weight\n'
            f'3. Update Weight\n'
            f'4. Return to User Selection\n'
        )
        selection = input("What is your selection? Type 'Quit' if you are finished.").lower()

        if selection == "1" or selection == "update weight":
            user_weight_change(user)
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
            print("\nPlease enter a valid selection.\n")


def user_weight_change(user):
    while True:
        weight = input("Please enter your new weight in imperial measurements.")
        try:
            weight = float(weight)
            break
        except ValueError as error:
            print(error)
            print("\nPlease input a valid number.\n")
            continue
    date = user_date_entry()
    user.set_weight(weight)
    user.weight_entry(weight, date)
    return


def user_date_entry():
    date_list = []
    while True:
        date_unchecked = input(
            "Input a custom date in MM/DD/YYYY format or leave blank if you want it automatically logged.")
        if len(date_unchecked) == 0:
            date = DATETODAY
            return date
        else:
            try:
                date_split = date_unchecked.split('/')
            except ValueError as error:
                print("\nEncountered invalid input. Please input a date in MM/DD/YYYY format.\n")
                continue
        for date in date_split:
            try:
                date = int(date)
                date_list.append(date)
            except ValueError as error:
                print("\nNon-numerical input encountered. Please type in valid numerical input in MM/DD/YYYY format.\n")
                continue
        if date_list[0] <= 0 or date_list[0] > 12:
            print('\nInvalid month entered. Please input a proper month in MM format.\n')
            continue
        if date_list[1] <= 0 or date_list[1] > 31:
            print('\nInvalid day entered. Please input a proper day in DD format.\n')
            continue
        if date_list[2] > curyear:
            print("\nPlease input a year equal to or before the current year. Future dates are not permissible.\n")
            continue


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
