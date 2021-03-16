import sys
import json
import pathlib
import datetime

BASE_DIR = pathlib.Path().resolve()
DATABASE = 'userdb.json'
DB_BACKUP = 'dbbackup.json'
DATABASEPATH = BASE_DIR / DATABASE
DATETODAY = str(datetime.date.today())


def create_database():
    '''
    Exclusively create a new database.
    :return None:
    '''
    try:
        database = open(DATABASE, 'x', encoding='utf-8')
        database.close()
        return
    except FileExistsError as error:
        print(error)


def read_database():
    '''
    Opens the database for data retrieval.
    :return Object: readable collection of JSON user objects
    '''
    try:
        database = open(DATABASE, 'r', encoding='utf-8')
        return database
    except FileNotFoundError as error:
        print(error)


def fetch_user(user=None):
    '''
    Fetches a JSON string from the database based on the input provided.
    :return Object: a deserialized object of the user fetched.
    '''
    with open(DATABASE, 'r', encoding='utf-8') as dbread:
        if user == None:
            while True:
                username = input('Please type your username in to query the database: ')
                for line in dbread:
                    if line.startswith(username):
                        user = json.loads(next(dbread))
                        return user, username
                else:
                    print(f'\n{username} was not found in the database. Please enter another username.\n')
                    continue
        else:
            username = user.username
            for line in dbread:
                if line.startswith(user.username):
                    user = json.loads(next(dbread))
                    return user, username


def edit_user(user):
    '''
    Overwrites user JSON with new data.
    :param user: a User object
    :return None:
    '''
    try:
        with open(DATABASE, 'r+', encoding='utf-8') as dbread:
            for line in dbread:
                if line.startswith(user.username):
                    next(dbread)
                    return
    except KeyError as keyerror:
        print(keyerror)
        print('Please provide another username to query the database')
    except FileNotFoundError as fnferror:
        print(fnferror)
    except:
        error = sys.exc_info()[1]
        print(error)


def append_user(user):
    '''
    Appends a new user to the database.
    :param user: a User Object
    :return None:
    '''
    try:
        with open(DATABASE, 'a', encoding='utf-8') as dbedit:
            dbedit.write(f'{user.username}\n')
            json.dump(user.user_dict, dbedit)
            dbedit.write(f'\n\n')
    except KeyError as keyerror:
        print(keyerror)
    except FileNotFoundError as fnferror:
        print(fnferror)


def backup_database():
    try:
        with open(DATABASE, 'r', encoding='utf-8') as dbread, open(DB_BACKUP, 'w', encoding='utf-8') as dbwrite:
            data = dbread.readlines()
            dbwrite.write(data)
    except FileNotFoundError as error:
        print(error)


class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, username, name, startingweight, currentweight, height, weight_history=None):
        self.username = username
        self.user_dict = self.user_dict_create(name, startingweight, currentweight, height, weight_history)

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

    def set_startweight(self, weight=None):
        '''
        Sets the user's starting weight to a new figure.
        :param weight: the new starting weight entry
        '''
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

    def user_dict_create(self, name, startingweight, currentweight, height, weight_history=None):
        '''
        Creates a dictionary with all of the user's personal statistics to be serialized as JSON.
        :param name: User's full name
        :param startingweight: The user's starting weight.
        :param currentweight: The user's current weight.
        :param height: The user's height.
        :param weight_history: User's weight history is mapped by date.
        :return Dictionary: a dictionary containing the user's personal statistics.
        '''
        if weight_history == None:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': {
                    DATETODAY: currentweight
                }
            }
        else:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': weight_history
            }

    def weight_entry(self, date, weight):
        '''Assign a new weight entry to the dictionary with the date as the key'''
        try:
            self.user_dict['weight history'][date] = weight
        except KeyError as error:
            print(error)
        edit_user(self)

    def weight_change(self):
        '''Average all of the dictionary's entries and compares to starting weight and current weight'''
        total = 0
        for value in self.user_dict.values():
            total += value


def username_check(username):
    '''
    References database to prevent duplication of usernames.
    :param username: the input given by the user
    :return bool: True if username is found and false if not
    '''
    with open('userdb.json', 'r', encoding='utf-8') as dbread:
        for line in dbread:
            if line.startswith(username):
                return True
            else:
                return False


def user_create_username():
    '''
    Queries user for their username. Username is checked against the database to ensure no duplication.
    And the username is checked to ensure it length parameters.
    :return String: the username of the user
    '''

    print(
        f'\n*****************************************\n'
        f'           Username Selection\n'
        f'*****************************************\n\n'
        f'A valid username contains a minimum of 8 characters and a maximum of 30 characters.\n'
        f'Usernames must not contain any spaces.\n'
    )
    while True:
        username = input("Enter a valid username: ")
        if " " in username:
            print('No spaces are allowed in usernames. Please input another username.')
            continue
        if len(username) < 8:
            print(f'{username} is too short. Please input a username that is equal to or more than 8 characters.')
            continue
        if len(username) > 30:
            print(f'{username} is too long. Please input a username that is equal to or less than 30 characters.')
            continue
        userbool = username_check(username)
        if userbool == True:
            print(f'{username} is taken. Please input another username.')
            continue
        else:
            return username


def user_create_name():
    '''
    Queries user for their first and last names.
    :return String: the user's first and last name
    '''
    while True:
        name = input('What is your first and last name: ')
        return name


def user_create_startweight():
    '''
    Queries user for their starting weight.
    :return Integer: the user's starting weight
    '''
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
    '''
    Queries user for their current weight.
    :return Integer: the user's current weight
    '''
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
    '''
    Queries user for their height.
    :return Integer: the user's height
    '''
    while True:
        height = input("What is the user's height in inches: ")
        try:
            height = float(height)
            return height
        except ValueError as error:
            print(error)
            print("\nPlease type a valid number.\n")
            continue


def new_user_prompt():
    '''
    Splash screen that welcomes the user and initiates the user creation process.
    :return Tuple: packs a tuple with all the user's inputs
    '''
    print(
        f'\n*****************************************\n'
        f'               WELCOME!\n'
        f'           NEW USER CREATION\n'
        f'*****************************************\n\n'
    )
    username = user_create_username()
    name = user_create_name()
    startingweight = user_create_startweight()
    currentweight = user_create_curweight()
    height = user_create_height()
    return username, name, startingweight, currentweight, height


def create_user():
    '''
    Finalization of user creation with the user being prompted for changes, if necessary, and then the new User object
    is created from the user input given.
    :return Object: a user object is created with all user data gathered
    '''
    username, name, startingweight, currentweight, height = new_user_prompt()

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
            user.weight_entry(DATETODAY, currentweight)
            append_user(user)
            return user
        elif userinput == 'no':
            userchange = input("What would you like to change? ").lower()
            if userchange == '1' or userchange == 'username':
                username = user_create_username()
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


def existing_user(user, username):
    username = username
    name = user['name']
    startingweight = user['starting weight']
    currentweight = user['current weight']
    height = user['height']
    weight_history = user['weight history']

    user = User(username, name, startingweight, currentweight, height, weight_history)
    return user


def selection_menu_print():
    print(
        f'\n*****************************************\n'
        f"      BOOG'S BODACIOUS BODY CRUNCHER!\n"
        f'             USER SELECTION\n'
        f'*****************************************\n\n'
    )


def user_selection():
    '''
    A selection menu for querying a new or existing user. A new user will be required to generate a unique user object.
    Existing users will have their information loaded from the database.
    :return Object: returns a User object
    '''
    selection_menu_print()
    while True:
        selection = input(
            "Type 'New user' to begin user creation or 'existing user' to access an existing user.\n").lower()
        if selection == 'new user':
            user_obj = create_user()
            return user_obj
        if selection == 'existing user':
            user, username = fetch_user()
            user_obj = existing_user(user, username)
            return user_obj
        else:
            print('\nPlease enter a valid selection.\n')


def main_menu_print(user):
    print(
        f'\n*****************************************\n'
        f"                MAIN MENU\n"
        f'*****************************************\n\n'
        f"           Username: {user.username}\n"
        f"           Name: {user.user_dict['name']}\n"
        f"           Starting weight: {user.user_dict['starting weight']}\n"
        f"           Current weight: {user.user_dict['current weight']}\n"
        f"           Height: {user.user_dict['height']}"
    )
    print(
        f'\n*****************************************\n'
        f"               USER OPTIONS\n"
        f'*****************************************\n\n'
        f'          1. New Weight Entry\n'
        f'          2. Change Starting Weight\n'
        f'          3. Update Weight\n'
        f'          4. Return to User Selection\n'
    )


def user_main_menu(user):
    '''
    Provides user with access to various functions to alter personal statistics in the User object provided.
    :param user: a User object
    :return None:
    '''
    while True:
        user, username = fetch_user(user)
        user = existing_user(user, username)
        main_menu_print(user)
        selection = input("What is your selection? Type 'Quit' if you are finished.").lower()
        if selection == "1" or selection == "new weight entry":
            new_weight_entry(user)
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


def new_weight_entry(user):
    '''
    User input is used to alter User object to set a new weight and establish additional weight history.
    :param user: a User object
    :return None:
    '''
    while True:
        weight = input("Please enter a new weight in imperial measurements: \n")
        try:
            weight = float(weight)
            break
        except ValueError as error:
            print(error)
            print("\nPlease input a valid number.\n")
            continue
    date = user_date_entry()
    user.weight_entry(date, weight)
    return


def user_date_entry():
    date_list = []
    while True:
        date_unchecked = input(
            "Input a custom date in YYYY/MM/DD format or leave blank if you want it automatically logged.")
        if len(date_unchecked) == 0:
            date = DATETODAY
            return date
        else:
            try:
                date_split = date_unchecked.split('/')
            except ValueError as error:
                print("\nEncountered invalid input. Please input a date in YYYY/MM/DD format.\n")
                continue
        for date in date_split:
            try:
                date = int(date)
                date_list.append(date)
            except ValueError as error:
                print("\nNon-numerical input encountered. Please type in valid numerical input in YYYY/MM/DD format.\n")
                continue
        if date_list[1] <= 0 or date_list[0] > 12:
            print('\nInvalid month entered. Please input a proper month in MM format.\n')
            continue
        if date_list[2] <= 0 or date_list[1] > 31:
            print('\nInvalid day entered. Please input a proper day in DD format.\n')
            continue
        if date_list[0] > curyear:
            print("\nPlease input a year equal to or before the current year. Future dates are not permissible.\n")
            continue


def main():
    if DATABASEPATH.exists() == False:
        create_database()
    user = user_selection()
    user_main_menu(user)


if __name__ == '__main__':
    main()
