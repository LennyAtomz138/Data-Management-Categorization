"""
CLI Menu is used to display the DMCT menu at application startup.
It is called by Main.py.
"""
from Source import TextractPDFVersion


def MainMenu():
    """
    The Main Menu for the DMCT program that contains submenus for user navigation.
    :return:
    """

    print("*=*" * 14)
    print("Database Management Categorization Tool")
    print("\t" * 3, " " * 2, "(DMCT)")
    print("*=*" * 14)

    while True:
        print("="*14, "Main Menu", "="*16)
        print("",
              "1 - Input Keyword(s) and Parse Documents\n",
              "0 - Exit DMCT")
        print("="*41)
        user_input = int(input("Enter Number: "))

        try:
            if user_input < 0 or user_input > 2:
                raise ValueError
            elif user_input == 0:
                print("Exiting the Data Management Categorization Tool")
                break
            elif user_input == 1:
                print("\n")
                GetUserKeywords()
            else:
                print("Invalid input: Please try again.")
        except ValueError:
            print("Invalid integer. Please enter either 0 or 1.")


def GetUserKeywords():
    """
    Prompts user for keywords and stores them in an array.
    Displays the array to the screen upon completion.
    :return:
    """
    keyword_list = []
    keyword_counter = 0

    print("="*8, "Keyword Entry Screen", "="*11)
    print("(Input 'halt dmct' when finished)")
    print("=" * 41)

    while True:
        keyword_counter += 1
        user_input = input("Enter keyword # {counter}: ".format(counter=keyword_counter))
        if user_input.lower() == 'halt dmct':
            break
        else:
            keyword_list.append(user_input.lower())

    keyword_list.sort()
    print("=" * 41)
    print("You've entered the following keyword(s):\n", keyword_list)
    user_input = int(input("Proceed with document tagging?\n"
                           "Enter 1 for 'Yes' or 0 for 'No': "))
    try:
        if user_input < 0 or user_input > 1:
            raise ValueError
        elif user_input == 0:
            print("Would you like to try again?\n",
                  "1 - Try Again\n",
                  "0 - Quit to Main Menu")
            user_input = int(input("Enter Number: "))
            try:
                if user_input < 0 or user_input > 1:
                    raise ValueError
                elif user_input == 0:
                    print("\n")
                    MainMenu()
                elif user_input == 1:
                    print("=" * 41)
                    print("\n")
                    GetUserKeywords()
                else:
                    print("Invalid input: Please try again.")
            except ValueError:
                print("Invalid integer. Please enter a value between 0 and 1.")
        elif user_input == 1:
            TextractPDFVersion.Main(keyword_list)
        else:
            print("Invalid input: Please try again.")
    except ValueError:
        print("Invalid integer. Please enter a value between 0 and 1.")
