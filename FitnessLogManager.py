#! python3

import datetime
import os
import shutil
from distutils.dir_util import copy_tree
import pyperclip
from typing import List, Dict, Optional

PROGRAM_LIST = 0
SESSION_DICT = 1
EVERYTHING_LIST = 2

CURRENT_PROGRAM = -1

USER = 0
PLACE_TO_LOG = 1


def read(filename: str) -> str:
    """
    reads the file specified and returns it as a str
    """
    try:
        file_handle = open(filename)
        lines = file_handle.read()
        file_handle.close()
        return lines
    except FileNotFoundError:
        print("File couldn't be found.")


def parse_logger(filename: str) -> (List[str],
                                    Dict[str, List[str]],
                                    List[str]):
    """
    reads the logger specified and parses it into appropriate dictionaries for later use
    """
    program_list = []
    program_filters = ['First Pair']
    session_dict = {}
    days_of_week = ['Monday', 'Wednesday', 'Friday', 'Saturday', 'Thursday', 'Tuesday', 'Sunday']
    everything_list = []

    file_handle = open(filename)
    whole_file = file_handle.read()
    file_handle.close()
    file_list = whole_file.split("---")

    for element in file_list:
        # add to program_list
        for key in program_filters:
            if key in element[:33]:
                program_list.append(element)

        # add to session_dict
        for day in days_of_week:
            if day in element[:9]:
                initial_split_element = element.split('\n')
                split_element = list(filter(None, initial_split_element))  # filters out empty strings in the list
                header = split_element[0]
                session_dict[header] = split_element[1:]

        # add to everything_list
        if element != '':
            everything_list.append(element)

    return program_list, session_dict, everything_list


def parse_date(wanted_date: str) -> datetime.date:
    """
    helper function for create_header() that takes a user inputted date in the form of dd/mm/yyyy and turns it into a
    date instance
    """
    date_elements = wanted_date.split("/")
    formatted_date = datetime.date(int(date_elements[2]), int(date_elements[1]), int(date_elements[0]))
    return formatted_date


def return_user_spec() -> tuple[str, str]:
    """
    returns user specifications (User's name and logging directory)
    """
    file_handle = open(os.path.join(python_dir, "src", "user_spec.txt"))
    whole_file = file_handle.read()
    file_handle.close()
    u_name = ""
    u_log_dir = ""
    try:
        file_list = whole_file.split("\n")
        u_name = file_list[USER]
        u_log_dir = file_list[PLACE_TO_LOG]
        if u_log_dir.lower() == "same":
            u_log_dir = python_dir
    except IndexError:
        return u_name, u_log_dir
    return u_name, u_log_dir


def read_user_spec() -> None:
    """
    Parses and reads user specifications to the user.
    """
    u_name, u_log_dir = return_user_spec()
    print("\nName:", u_name)
    print("\nLogging Directory:", u_log_dir)


def adjust_user_spec() -> None:
    """
    Adjusts user specifications, in the form of:

    1) User's name
    2) User's working directory (where the logs are being stored)
    """
    old_name, old_log_dir = return_user_spec()
    o_valid = False
    while not o_valid:
        starting_prompt = input("\nWhat do you want to Adjust?\n\n1- Name\n2- Directory to store logs\n\n")

        if starting_prompt.lower() == "1":
            name_prompt = "\nPlease enter your name:\n\n"
            u_name = input(name_prompt)
            write_user_spec(u_name, old_log_dir)
            print("\nName changed to {}.".format(u_name))
            o_valid = True

        elif starting_prompt.lower() == "2":
            directory_prompt = "\nPlease enter a valid filepath where you want to store your logs\n\n"
            u_log_dir = input(directory_prompt)
            if u_log_dir.lower() == "same":
                u_log_dir = os.getcwd()
            valid = os.path.isdir(u_log_dir)
            while not valid:
                u_log_dir = input("\nCome on man, that's an invalid path. Try again\n\n")
                if u_log_dir.lower() == "same":
                    u_log_dir = os.getcwd()
                valid = os.path.isdir(u_log_dir)
            write_user_spec(old_name, u_log_dir)
            print("\nSuccessfully changed logging directory to {}".format(u_log_dir))
            old_file_location = os.path.join(old_log_dir, 'my_fitness_logs.txt')
            print("\nMoving \"my_fitness_logs\" from {} to {}".format(old_log_dir, u_log_dir))
            shutil.move(old_file_location, u_log_dir)
            print("\nMoved file successfully!")
            o_valid = True
        else:
            print("\nInvalid number.")


def write_user_spec(w_name: str,w_log_dir: str) -> None:
    """
    helper function for adjust_user_spec that writes to "user_spec".txt in src
    """
    file_handle = open(os.path.join(python_dir, "src", "user_spec.txt"), "w")
    file_handle.write(w_name)
    file_handle.write("\n")
    file_handle.write(w_log_dir)
    file_handle.close()


def create_log_file() -> None:
    """
    Creates my_fitness_logger.txt for user at desired location
    """
    u_log_dir = return_user_spec()[PLACE_TO_LOG]
    starter_file = read(os.path.join(python_dir, "src", "starter_file.txt"))
    file_handle = open(os.path.join(u_log_dir, "my_fitness_logs.txt"), "w")
    file_handle.write(starter_file)
    file_handle.close()


def create_header() -> str:
    """
    helper function for log() that specifies the header
    """
    try:
        wanted_date = input("\nWhat day do you want to log to? (DD/MM/YYYY)\n\n")  # 29/12/2020
        formatted_date = parse_date(wanted_date)  # datetime.date(2020, 12, 29)
        weekday = formatted_date.strftime('%A')  # Tuesday
        header_tuple = (weekday, wanted_date)  # ('Tuesday', '29/12/2020')
        header = " ".join(header_tuple)  # 'Tuesday 29/12/2020'
        return header

    except ValueError or IndexError:
        print("\nInvalid values entered, format must be an appropriate DD/MM/YYYY.")
        create_header()


def create_comment() -> (Optional[str],
                         bool):
    """
    helper function for log that asks user if they want to add a comment, then sets the comment appropriately.
    """
    valid = False

    while not valid:
        prompt = "\nPlease select an option:\n\n1- Log a session w/ comment\n2- Log a session w/o comment\n" \
                 "3- Log a skipped session\n\n"
        wanted = input(prompt)
        if wanted.lower() == "1":
            comment_decision = True
            comment = input("\nPlease enter your comment:\n\n")
        elif wanted.lower() == "2":
            comment_decision = False
            comment = None
        elif wanted.lower() == "3":
            comment_decision = True
            comment = "(SKIPPED)"
        else:
            print("\nInvalid number.")
            continue
        valid = True

    return comment, comment_decision


def return_current_program(filename: str) -> str:
    """
    returns the current program being followed
    """
    program_list = parse_logger(filename)[PROGRAM_LIST]
    try:
        current_program = program_list[CURRENT_PROGRAM]
        return current_program
    except IndexError:
        print("Couldn't detect a program.")
        return


def write_adjusted_program(filename: str, new_program: str) -> None:
    """
    a helper function for adjust_program() that writes the adjusted program to file
    """
    file_handle = open(filename, 'a')
    file_handle.write('\n')
    file_handle.write(new_program)
    file_handle.write('---')
    file_handle.close()


def parse_current_program(filename: str) -> Dict[str, list[str]]:
    """
    helper function for adjust_program() that parses the current program for easy adjusting
    """
    current_program = return_current_program(filename)
    current_program_dict = {}
    header_list = create_program_header(filename)
    current_program_list = current_program.split('\n\n')
    index = 0
    for index in range(len(current_program_list)):
        element = current_program_list[index]
        element = element.strip('\n')
        element = element.strip(':')
        if element in header_list:
            appropriate_link = current_program_list[index + 1]
            appropriate_link_list1 = appropriate_link.split('\n')
            appropriate_link_list2 = list(filter(None, appropriate_link_list1))
            current_program_dict[element] = appropriate_link_list2

    return current_program_dict


def parse_adjusted_program(new_program_dict: Dict[str, list[str]]) -> str:
    """
    helper function for adjust_program() that turns a dictionary into a str for file writing
    """
    new_program_list = []

    for key in new_program_dict:
        new_program_list.append(key)
        new_program_list.append('')

        sets = new_program_dict[key]
        for element in sets:
            new_program_list.append(element)
        new_program_list.append('')

    new_program_str = '\n'.join(new_program_list)

    return new_program_str


def log_feedback(filename: str) -> str:
    """
    helper function for log() and adjust_program() that gives feedback on log made
    """
    everything_list = parse_logger(filename)[EVERYTHING_LIST]
    last_3_list = everything_list[-3:]
    last_3_str = "---".join(last_3_list)
    last_3_str += '---'
    return last_3_str


def adjust_program(filename: str) -> None:
    """
    adjusts the current program being followed
    """
    current_program = return_current_program(filename)
    if current_program is None:
        return

    print("\nCurrent program is:\n", current_program)

    current_program_dict = parse_current_program(filename)
    new_program_dict = {}

    for key in current_program_dict:
        prompt = "\nWhat do you want to do with the {}?\n\n1- Keep\n2- Adjust\n3- Delete\n\n".format(key.lower())
        response = input(prompt)
        set_list = current_program_dict[key]
        if response == '1':
            new_program_dict[key] = set_list
        if response == '2':
            index = 0
            for index in range(len(set_list)):
                element = set_list[index]
                print(element)
                prompt = "Adjust?\n\n1- Yes\n2- No\n\n"
                response = input(prompt)
                if response == '1':
                    prompt = "Enter new subset:\n\n"
                    response = input(prompt)
                    set_list[index] = response
            prompt = "Add new subset?\n\n1- Yes\n2- No\n\n"
            response = input(prompt)
            if response == '1':
                prompt = "Enter new subset:\n\n"
                response = input(prompt)
                set_list.append(response)
            new_program_dict[key] = set_list
        if response == '3':
            continue

    # turn the dictionary into a readable string
    new_program_str = parse_adjusted_program(new_program_dict)
    prompt = 'The new program is going to be:\n\n{}\nProceed?\n\n1- Yes\n2- No\n\n'.format(new_program_str)
    response = input(prompt)
    if response == '1':
        write_adjusted_program(filename, new_program_str)
        print("\nProgram adjusted successfully.")
        print(log_feedback(filename))


def create_program_header(filename: str) -> List[str]:
    """
    a helper function for create_body() that returns the section headers for the current program being followed
    """
    current_program = return_current_program(filename)
    possible_header_list = current_program.split('\n\n')
    temp_header_list = []
    for possible_header in possible_header_list:
        if 'pair' in possible_header.lower() or 'triplet' in possible_header.lower():
            temp_header_list.append(possible_header)

    # strip newlines and ':' from temp_header_list
    header_list = []
    for header in temp_header_list:
        header = header.strip('\n')
        header = header.strip(':')
        header_list.append(header)

    return header_list


def max_reps_clipboard(header: str) -> None:
    """
    helper function for create_body() that copies the max reps possible to clipboard as appropriate to the given header
    """
    if 'pair' in header.lower():
        pyperclip.copy('8 8 8, 8 8 8')

    elif 'triplet' in header.lower():
        pyperclip.copy('12 12 12, 30 30 30, 12 12 12')


def create_body(filename: str) -> Dict[str, str]:
    """
    helper function for log() that creates a body for the log based on user input
    """
    header_list = create_program_header(filename)
    body = {}

    print("\nMax reps copied to clipboard as appropriate.")
    for header in header_list:
        max_reps_clipboard(header)
        prompt = "\nPlease enter your reps for the {}\n\n".format(header.lower())
        response = input(prompt)
        body[header] = response

    return body


def log(filename: str) -> None:
    """
    logs a workout based on specified user input:
    1- A given date
    2- Comment (optional)
    3- reps
    """
    try:
        file_handle = open(filename)
        file_handle.close()
    except FileNotFoundError:
        print("File couldn't be found.")
        return
    # specify header
    header = create_header()
    print("\nLogging to:", header)

    # specify comment (optional)
    comment, comment_decision = create_comment()

    # specify body
    if comment == "(SKIPPED)":
        body = []
    else:
        body = create_body(filename)

    # confirm with user
    if comment_decision:
        to_be_logged = [header, comment]
    else:
        to_be_logged = [header]
    for key in body:
        reps = body[key]
        to_be_logged.append(reps)
    to_be_logged_str = '\n'.join(to_be_logged)
    prompt = '\nThe following is going to be logged:\n\n{}\n\nProceed?\n\n1- Yes\n2- No\n\n'.format(to_be_logged_str)
    response = input(prompt)
    if response == '1':
        file_handle = open(filename, 'a')
        file_handle.write('\n')
        file_handle.write(header)
        if comment_decision:
            file_handle.write('\n')
            file_handle.write(comment)
        for key in body:
            reps = body[key]
            file_handle.write('\n')
            file_handle.write(reps)
        file_handle.write('\n')
        file_handle.write('---')
        file_handle.close()
        print("\nLog successful.")
        print(log_feedback(filename))


def backup(filename: str):
    """
    creates a backup to 'backup.txt' before altering to the main file
    """
    file = read(filename)
    file_handle = open('backup.txt', 'w')
    file_handle.write(file)
    file_handle.close()


def delete_entries(filename: str) -> None:
    """
    deletes entries in the file based on user input
    """

    prompt = "\nHow many entries would you like to delete?\n\n"
    entries_to_delete = int(input(prompt))

    everything_list = parse_logger(filename)[EVERYTHING_LIST]
    delete_list = everything_list[-entries_to_delete:]
    delete_str = '---'.join(delete_list)

    prompt = "{}\nDelete these entries?\n\n1- Yes\n2- No\n\n".format(delete_str)
    response = input(prompt)

    if response == '1':
        backup(filename)
        everything_list = everything_list[:-entries_to_delete]
        everything_str = '---'.join(everything_list)
        file_handle = open(filename, 'w')
        file_handle.write(everything_str)
        file_handle.write('---')
        file_handle.close()
        print("\nEntries deleted successfully.")


# def backup_to_z():
#     """
#     backs up the folder from python_dir and log_dir to Z:\\_Mostafa\\PycharmProjects\\FitnessLogManager and
#     Z:\\_Mostafa respectively (intended for me)
#
#     """
#     print('\nStarting backup..')
#     z_python_dir = r'Z:\_Mostafa\PycharmProjects\FitnessLogManager'
#     z_log_dir = r'Z:\_Mostafa\Reddit bodyweight routine'
#     copy_tree(python_dir, z_python_dir)
#     copy_tree(log_dir, z_log_dir)
#     print('\nBacked up to (Z:) successfully.')


def is_new_user() -> bool:
    """
    helper function for new_user_sequence that determines if user is new
    """
    spec = os.path.join(python_dir, "src", "user_spec.txt")
    return os.stat(spec).st_size == 0


def new_user_sequence():
    """
    deals with a new user by introducing and welcoming him to the program
    (and hopefully not driving him away with the sass)
    """
    print("Welcome to FitnessLogManager, a simple program that helps organize your fitness progress in a simple and "
          "intuitive matter!")
    print("\nYou will be using the command line interface to interact with FitnessLogManager and give it commands.")
    input("\nTry it out! Type anything that your heart desires and feed it into this program by pressing enter:\n\n")
    print("\nThat was very insightful.")

    u_name = input(
        "\nOkay sorry, enough messing around. Will you be so kind to give me your name? Because I am assuming you are "
        "kind, enter your name:\n\n")
    valid_number = False
    valid_name = False
    while not valid_number:
        confirmation_prompt = "\nYour name is {}?\n\n1- Yes, and what about it?\n2- No, I somehow got my name wrong (" \
                              "who does that?)\n\nEnter the number associated with your response: ".format(
            u_name)
        desired_name = input(confirmation_prompt)
        if desired_name == "1":
            valid_number = True
            valid_name = True
        elif desired_name == "2":
            valid_number = True
            valid_name = False
        else:
            print("\nI didn't quite get that, please enter a valid number (1 or 2, in this case)")

    while not valid_name:
        u_name = input(
            "\nNo worries, we all make mistakes sometimes (although it IS pretty weird to get your name "
            "wrong..)\n\nPlease enter your name, no second chances this time:\n\n")
        valid_name = True

    print(
        "\nWelcome to this very sassy program, {}. While I am programmed to always say this, that's a very nice name.".format(
            u_name))
    print("\nOkay let's actually get you started now, shall we?")
    input("\nPress enter to continue..")

    print("\nThis is what a workout program typically looks like:")
    print('\n', read(os.path.join(python_dir, "src", "example_workout_program.txt")), sep='')
    print(
        "\nThis is what you are going to be logging your workout sessions to (obviously). You can change this at any "
        "time through FitnessLogManager.")
    input("\nPress enter to continue..")
    print("\nHere is an example of a log:")
    print('\n', read(os.path.join(python_dir, "src", "example_log.txt")), sep='')

    print("\nYou are almost set! Finally, you are going to enter a directory to store the logs you make "
          "through this program. A .txt file will be made in the directory you choose.")
    print("\nExample of what a directory looks like: D:\\Folders\\Training")
    print("\nIf you simply want to store that .txt file in the same directory as FitnessLogManager, just write "
          "\"same\" (without quotations)")
    pyperclip.copy(python_dir)
    u_log_dir = input("\nCurrent directory has been copied to clipboard for convenience. Please enter a valid "
                      "directory to store your logs:\n\n")
    if u_log_dir.lower() == "same":
        u_log_dir = os.getcwd()
    valid = os.path.isdir(u_log_dir)
    while not valid:
        u_log_dir = input("\nCome on man, that's an invalid path. Try again\n\n")
        if u_log_dir.lower() == "same":
            u_log_dir = os.getcwd()
        valid = os.path.isdir(u_log_dir)
    file_handle = open(os.path.join(python_dir, "src", "user_spec.txt"), "w")
    file_handle.write(u_name)
    file_handle.write("\n")
    file_handle.write(u_log_dir)
    file_handle.close()
    create_log_file()
    print("\nYou are all set now! FitnessLog.txt has been created with title \"my_fitness_logs.txt\" at:", u_log_dir)
    print("\nTo get you set up, FitnessLog.txt has been initialized with a sample workout program. Feel free to alter "
          "it either using FitnessLogManager or through the .txt file itself.")
    print("\nThey grow up so fast *sniff*. Please enjoy using FitnessLogManager! If you have any ideas or suggestions "
          "for this project, don't hesistate to contact me @mostafashalaby on github.")
    input("\nType and Enter anything to start up the program.\n\n")
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


python_dir = os.getcwd()

if is_new_user():
    new_user_sequence()

name, log_dir = return_user_spec()

os.chdir(log_dir)

# interface:

logger = os.path.join(log_dir, 'my_fitness_logs.txt')

welcome = ' Welcome, {}. What would you like to do today? '.format(name)
welcome = welcome.center(211, '*')
print(welcome)
option_1 = ' (1) Read the logger '
option_1 = option_1.center(211, '*')
option_2 = ' (2) Log a session '
option_2 = option_2.center(211, '*')
option_3 = ' (3) Read the current program '
option_3 = option_3.center(211, '*')
option_4 = ' (4) Adjust the current program '
option_4 = option_4.center(211, '*')
option_5 = ' (5) Remove entries '
option_5 = option_5.center(211, '*')
option_6 = ' (6) Read user specifications '
option_6 = option_6.center(211, '*')
option_7 = ' (7) Adjust user specifications '
option_7 = option_7.center(211, '*')
# option_8 = ' (8) Backup to (Z:) '
# option_8 = option_8.center(211, '*')
exit_prompt = ' (Type \'exit\' to exit the program) '
exit_prompt = exit_prompt.center(211, '*')

answer = ""

while 'exit' != answer.lower():
    print('\n{}\n'
          '{}\n'
          '{}\n'
          '{}\n'
          '{}\n'
          '{}\n'
          '{}\n'
          '{}\n'.format(option_1, option_2, option_3, option_4, option_5, option_6, option_7, exit_prompt))

    answer = input()

    if answer == '1':
        print('\n', read(logger), sep='')

    elif answer == '2':
        log(logger)

    elif answer == '3':
        print(return_current_program(logger))

    elif answer == '4':
        adjust_program(logger)

    elif answer == '5':
        delete_entries(logger)

    elif answer == '6':
        os.chdir(python_dir)
        read_user_spec()
        os.chdir(log_dir)

    elif answer == '7':
        os.chdir(python_dir)
        adjust_user_spec()
        os.chdir(log_dir)

    # elif answer == '8':
    #     backup_to_z()
