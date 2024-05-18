'''
Create a simple assistant bot that can do the following:
- Greet you when you start the program
- Say hello and ask how it can help you
- Add your name and phone number to the Address Book
- Change your phone number in the Address Book
- Get your phone number from the Address Book
- Remove your phone number from the Address Book
- Delete the record from the Address Book
- Get all the contacts in the Address Book
- Add your birthday to the Address Book
- Show your birthday from the Address Book
- Get all the birthdays from the Address Book for the next 7 days
- Say goodbye and end the program
- Save the Address Book to a file when you close the program
- Load the Address Book from a file when you start the program or create 
a new one if the file does not exist
'''

from collections import UserDict
from datetime import datetime
import pickle

class Field:
    '''
    Base class for all fields.
    '''
    def __init__(self, value): # Initialize the field with a value.
        self.value = value # Set the value of the field.

    def __str__(self): # Return the string representation of the field.
        return str(self.value) # Return the value of the field.

class Name(Field):
    '''
    Class to store a name field.
    '''
    def __init__(self, value): # Initialize the name field with a value.
        super().__init__(value) # Call the __init__ method from the base class Field.
        if not value.isalpha(): # Check if the value contains only alphabetic characters.
            raise ValueError("Name should contain only alphabetic characters.")
            # Raise a ValueError.

class Phone(Field):
    '''
    Class to store a phone number field.
    '''
    def __init__(self, value): # Initialize the phone number field with a value.
        super().__init__(value) # Call the __init__ method from the base class Field.
        if not value.isdigit() or len(value) != 10:
            # Check if the value contains only digits and has a length of 10.
            raise ValueError("Phone number should contain 10 digits.") # Raise a ValueError.

class Birthday(Field):
    '''
    Class to store a birthday field.
    '''
    def __init__(self, value): # Initialize the birthday field with a value.
        super().__init__(value) # Call the __init__ method from the base class Field.
        try: # Try to parse the value as a date.
            self.value = datetime.strptime(value, "%d.%m.%Y") # Set the value of the birthday field.
        except ValueError as exc: # If the value is not a valid date.
            raise ValueError('Invalid date format. Use DD.MM.YYYY') from exc # Raise an error.

class Record:
    '''
    Class to store a contact record.
    '''
    def __init__(self, name): # Initialize the record with a name.
        self.name = Name(name) # Set the name of the record.
        self.phones = [] # Initialize the list of phones.
        self.birthday = None # Initialize the birthday field.

    def add_birthday(self, birthday):
        '''
        Add a birthday to the record.
        '''
        self.birthday = Birthday(birthday) # Set the birthday of the record.

    def add_phone(self, phone):
        '''
        Add a phone to the record.
        '''
        self.phones.append(Phone(phone)) # Add the phone to the list of phones.

    def remove_phone(self, phone):
        '''
        Remove a phone from the record.
        '''
        for p in self.phones: # Iterate over the list of phones.
            if p.value == phone: # If the phone number is found.
                self.phones.remove(p) # Remove the phone number.

    def edit_phone(self, old_phone, new_phone):
        '''
        Edit a phone in the record.
        '''
        for phone in self.phones: # Iterate over the list of phones.
            if phone.value == old_phone: # If the phone number is found.
                phone.value = new_phone # Update the phone number.

    def find_phone(self, phone):
        '''
        Find a phone in the record.
        '''
        for p in self.phones: # Iterate over the list of phones.
            if p.value == phone: # If the phone number is found.
                return p.value # Return the phone number.
        return None # Return None if the phone number is not found.

    def __str__(self):
        '''
        Return the string representation of the record.
        '''
        if self.birthday: # Check if the record has a birthday
            birthday_str = self.birthday.value.strftime('%d.%m.%Y') # Get the birthday date
        else: # If the record does not have a birthday
            birthday_str = "no birthday record" # Set the birthday string
        return f"Contact name: {self.name.value.capitalize()}, Phones: {
            ', '.join(str(p) for p in self.phones)}, Birthday: {
                birthday_str
                }"
            # Return the string representation of the record

class AddressBook(UserDict):
    '''
    Class to store the Address Book.
    '''
    def add_record(self, record):
        '''
        Add a record to the Address Book.
        '''
        self.data[record.name.value] = record # Add the record to the Address Book.

    def delete(self, name):
        '''
        Delete a record from the Address Book.
        '''
        return self.data.pop(name) # Remove the record from the Address Book.

    def find(self, name):
        '''
        Find a record in the Address Book.
        '''
        return self.data.get(name) # Return the record from the Address Book.

    def get_upcoming_birthdays(self) -> list[dict]:
        '''
        This method returns a list of upcoming birthdays within the next 7 days.
        '''
        upcoming_birthdays = []
        today = datetime.today() # Remove .date() to keep it as datetime
        for record in self.data.values():  # Iterate over records in the Address Book
            if record.birthday:  # Check if the record has a birthday
                birthday = record.birthday.value # Get the birthday date
                birthday_this_year = birthday.replace(year=today.year)
                # Set the year to the current year
                if birthday_this_year < today: # Change to datetime comparison
                    birthday_this_year = birthday.replace(year=today.year + 1)
                    # Set the year to the next year
                days_until_birthday = (birthday_this_year - today).days
                # Calculate the days until the birthday
                if 0 <= days_until_birthday <= 7:  # Check if the birthday is within the next 7 days
                    while birthday_this_year.weekday() > 4:  # Adjust if birthday falls on a weekend
                        birthday_this_year = birthday_this_year.replace(day=
                        birthday_this_year.day + 1)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                    })  # Add the user's name and the congratulation date to the list
        return upcoming_birthdays  # Return the list of upcoming birthdays

def input_error(func):
    '''
    Decorator to handle input errors.
    '''
    def inner(*args, **kwargs): # Inner function to handle errors
        try: # Try to execute the function
            return func(*args, **kwargs) # Execute the function
        except KeyError: # Handle key errors
            return "Contact not found." # Return a message
        except ValueError as ve: # Handle value errors
            return str(ve) # Return the error message as a string
        except IndexError as ie: # Handle index errors
            if str(ie) == "Please enter a name.":
                return str(ie) # Return the error message as a string
            elif str(ie) == "Please enter a name and phone number.":
                return str(ie)
            elif str(ie) == "Please enter name, old phone, and new phone.":
                return str(ie)
    return inner # Return the inner function

@input_error
def parse_input(user_input):
    '''
    Parse the user input and return the command and arguments.
    '''
    cmd, *args = user_input.split() # Split the input into command and arguments
    cmd = cmd.strip().lower() # Convert the command to lowercase
    args = [arg.lower() for arg in args] # Convert the arguments to lowercase
    return cmd, *args # Return the command and arguments

@input_error
def add_contact(args, book: AddressBook):
    '''
    Add a contact to the Address Book.
    '''
    if len(args) != 2: # Check if the number of arguments is not equal to 2
        raise IndexError("Please enter a name and phone number.")
        # Raise an IndexError with the specified message
    name, phone = args
    try: # Try to create a record with the name
        record = Record(name)  # Name validation occurs here
        record.add_phone(phone)  # Phone validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    existing_record = book.find(name) # Find the record in the Address Book
    if existing_record is None: # If the record is not found
        book.add_record(record) # Add the record to the Address Book
        message = "Contact added." # Set the message
    else: # If the record is found
        if phone not in [p.value for p in existing_record.phones]:
            # Check if the phone number is not already in the record
            existing_record.add_phone(phone) # Add the phone number to the record
            message = "Contact updated." # Set the message
        else: # If the phone number is already in the record
            message = "Phone number already exists for this contact." # Set the message
    return message # Return the message

@input_error
def delete_contact(args, book: AddressBook):
    '''
    Delete a contact from the Address Book.
    '''
    if len(args) != 1: # Check if the number of arguments is not equal to 1
        raise IndexError("Please enter a name.") # Raise an IndexError with the specified message
    name_input = args[0] # Get the name from the arguments
    try: # Try to create a name object
        name = Name(name_input)  # Name validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    record = book.delete(name.value) # Delete the record from the Address Book
    if record is None: # If the record is not found
        return "Contact not found." # Return a message
    return "Contact deleted." # Return a message

@input_error
def remove_contact_phone(args, book: AddressBook):
    '''
    Remove the phone number of a contact in the Address Book.
    '''
    if len(args) != 2: # Check if the number of arguments is not equal to 2
        raise IndexError("Please enter a name and phone number.")
        # Raise an IndexError with the specified message
    name, phone = args # Unpack the arguments
    try: # Try to create name and phone objects
        name = Name(name)  # Name validation occurs here
        phone = Phone(phone)  # Phone validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    record = book.find(name.value) # Find the record in the Address Book
    if record is None: # If the record is not found
        return "Contact not found." # Return a message
    if phone.value not in [p.value for p in record.phones]: # If the phone number is not found
        return "Phone number not found in contact's phones." # Return a message
    record.remove_phone(phone.value) # Remove the phone number from the record
    return "Phone removed." # Return a message

@input_error
def change_contact(args, book: AddressBook):
    '''
    Change the phone number of a contact in the Address Book.
    '''
    if len(args) != 3: # Check if the number of arguments is not equal to 3
        raise IndexError("Please enter name, old phone, and new phone.")
        # Raise an IndexError with the specified message
    name, old_phone, new_phone = args # Unpack the arguments
    try: # Try to create name, old phone, and new phone objects
        name = Name(name)  # Name validation occurs here
        old_phone = Phone(old_phone)  # Old phone validation occurs here
        new_phone = Phone(new_phone)  # New phone validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    record = book.find(name.value) # Find the record in the Address Book
    if record is None: # If the record is not found
        return "Contact not found." # Return a message
    if old_phone.value not in [p.value for p in record.phones]: 
        # If the old phone number is not found
        return "Old phone number not found in contact's phones." # Return a message
    record.edit_phone(old_phone.value, new_phone.value) # Change the phone number in the record
    return "Contact changed." # Return a message

@input_error
def get_contact(name, book: AddressBook):
    '''
    Get the phone number of a contact from the Address Book.
    '''
    if len(name) != 1: # Check if the number of arguments is not equal to 1
        raise IndexError("Please enter a name.") # Raise an IndexError with the specified message
    try: # Try to create a name object
        name = Name(name[0])  # Name validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    record = book.find(name.value) # Find the record in the Address Book
    if record is None: # If the record is not found
        return "Contact not found." # Return a message
    return f"{record.name.value.capitalize()}'s phones: {', '.join(str(p) for p in record.phones)}."
    # Return the contact's name and phones

@input_error
def get_all_contacts(book: AddressBook):
    '''
    Get all the contacts from the Address Book.
    '''
    if not book.data: # Check if the Address Book is empty
        return "No contacts found." # Return a message
    return "\n".join(str(record) for record in book.data.values())
    # Return the string representation of all records in the Address Book

@input_error
def add_birthday(args, book: AddressBook):
    '''
    Add a birthday to a contact in the Address Book.
    '''
    if len(args) != 2: # Check if the number of arguments is not equal to 2
        raise IndexError("Please enter a name and birthday in the format DD.MM.YYYY.")
        # Raise an IndexError with the specified message
    name, birthday = args # Unpack the arguments
    try: # Try to create name and birthday objects
        name = Name(name)  # Name validation occurs here
        birthday = Birthday(birthday)  # Birthday validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    record = book.find(name.value) # Find the record in the Address Book
    if record is None: # If the record is not found
        return "Contact not found." # Return a message
    record.add_birthday(birthday.value.strftime("%d.%m.%Y")) # Add the birthday to the record
    return "Birthday added." # Return a message

@input_error
def show_birthday(args, book: AddressBook):
    '''
    Show the birthday of a contact in the Address Book.
    '''
    if len(args) != 1: # Check if the number of arguments is not equal to 1
        raise IndexError("Please enter a name.") # Raise an IndexError with the specified message
    name = args[0] # Get the name from the arguments
    try: # Try to create a name object
        name = Name(name)  # Name validation occurs here
    except ValueError as ve: # Handle value errors
        return str(ve) # Return the error message as a string
    record = book.find(name.value) # Find the record in the Address Book
    if record is None: # If the record is not found
        return "Contact not found." # Return a message
    if record.birthday: # If the record has a birthday
        return f"{name.value.capitalize()}'s day of birth is {
            record.birthday.value.strftime('%d.%m.%Y')}."
        # Return the contact's name and birthday
    return f"{name.value.capitalize()} has no birthday record." # Return a message

@input_error
def birthdays(book: AddressBook):
    '''
    Get all the birthdays from the Address Book for the next 7 days.
    '''
    upcoming_birthdays = book.get_upcoming_birthdays() # Get the upcoming birthdays
    if not upcoming_birthdays: # If there are no upcoming birthdays
        return "No upcoming birthdays." # Return a message
    return "\n".join([f"{birthday['name'].capitalize()}'s birthday is on {
        birthday['congratulation_date']}."
                      for birthday in upcoming_birthdays]) 
                      # Return the list of upcoming birthdays

def save_data(book, filename="addressbook.pkl"):
    '''
    Save the Address Book to a file.
    '''
    with open(filename, "wb") as f: # Open the file in binary write mode
        pickle.dump(book, f) # Dump the Address Book to the file

def load_data(filename="addressbook.pkl"):
    '''
    Load the Address Book from a file.
    '''
    try: # Try to open the file
        with open(filename, "rb") as f: # Open the file in binary read mode
            return pickle.load(f) # Load the Address Book from the file
    except FileNotFoundError: # Handle file not found errors
        return AddressBook() # Return an empty Address Book

def main(): # Main function to run the assistant bot
    '''
    Main function to run the assistant bot.
    '''
    book = load_data() # Load the Address Book
    print("Welcome to the assistant bot!") # Print a welcome message
    while True: # Run the assistant bot in a loop
        user_input = input("Enter a command: ") # Get the user input
        command, *args = parse_input(user_input) # Parse the user input

        if command in ["close", "exit"]: # Check if the command is close or exit
            print("Good bye!") # Print a goodbye message
            save_data(book) # Save the Address Book
            break # Exit the loop

        elif command == "hello": # Check if the command is hello
            print("How can I help you?") # Print a message

        elif command == "add": # Check if the command is add
            print(add_contact(args, book)) # Add a contact to the Address Book

        elif command == "delete": # Check if the command is delete
            print(delete_contact(args, book)) # Delete a contact from the Address Book

        elif command == "remove": # Check if the command is remove
            print(remove_contact_phone(args, book)) # Remove the phone number of a contact

        elif command == "change": # Check if the command is change
            print(change_contact(args, book)) # Change the phone number of a contact

        elif command == "phone": # Check if the command is phone
            print(get_contact(args, book)) # Get the phone number of a contact

        elif command == "all": # Check if the command is all
            print(get_all_contacts(book)) # Get all the contacts from the Address Book

        elif command == "add-birthday": # Check if the command is add-birthday
            print(add_birthday(args, book)) # Add a birthday to a contact

        elif command == "show-birthday": # Check if the command is show-birthday
            print(show_birthday(args, book)) # Show the birthday of a contact

        elif command == "birthdays": # Check if the command is birthdays
            print(birthdays(book)) # Get all the birthdays for the next 7 days

        else: # If the command is not recognized
            print("Invalid command.") # Print an error message

if __name__ == "__main__": # Check if the script is executed
    main() # Run the assistant bot if the script is executed
