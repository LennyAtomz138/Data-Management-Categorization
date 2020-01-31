"""
CLI Menu is used to display the Command Line Interface menu at application startup.
It is called by Main.py.
"""

#add check for when user inputs non integer input
def MainMenu():	
	while True:
		print("Main Menu")
		print("",
				"1 - Open SubMenu1\n",
				"2 - Open SubMenu2\n",
				"0 - Exit program\n")
		
		user_input = int(input("Enter number here: "))
		
		if user_input == 0:
			input("Press Enter to exit program...")
			break
		elif user_input == 1:
			SubMenu1()
		elif user_input == 2:
			SubMenu2()
		else:
			print("Incorrect input. Enter a valid input \n")
	return

def SubMenu1():
	print("Submenu1")
	
	while True:
		print("", 
				"0 - Go back to the main menu\n",
				"1 - Hamburger\n",
				"2 - Cheeseburger\n",
				"3 - Hotdog\n",
				"4 - Cheesedog\n",
				"5 - Milkshake\n",
				"6 - Cheeseshake\n")
		
		user_input = int(input("Input your favorite food: "))
		
		if user_input == 0:
			input("Press Enter to go back to main menu...")
			break
		elif user_input == 1:
			print("You're Wrong\n")
		elif user_input == 2:
			print("You're Wrong\n")
		elif user_input == 3:
			print("You're Wrong\n")
		elif user_input == 4:
			print("You're Wrong\n")
		elif user_input == 5:
			print("You're Wrong\n")
		elif user_input == 6:
			print("You have good tastes!\n")
		else:
			print("Incorrect input. Enter a valid input \n")

def SubMenu2():
	print("Submenu2")
	
	while True:
		print("", 
				"0 - Go back to the main menu\n",
				"1 - Green\n",
				"2 - Bean\n",
				"3 - Eating machine\n",
				)
		
		user_input = int(input("Input a number: "))
		
		if user_input == 0:
			input("Press Enter to go back to main menu...")
			break
		elif user_input == 1:
			print("Tasty\n")
		elif user_input == 2:
			print("Be nice\n")
		elif user_input == 3:
			print("Don't forget your vegetables\n")
		else:
			print("Incorrect input. Enter a valid input \n")
		
print("This is the Database Management-Categorization Tool")
MainMenu()

		
