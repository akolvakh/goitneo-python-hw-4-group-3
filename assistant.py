from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def validate(self, value):
        return len(value) == 10 and value.isdigit()

class Email(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid email format")
        super().__init__(value)

    def validate(self, value):
        # Implement email validation logic
        return True  # Placeholder validation

class Address(Field):
    pass

class Birthday(Field):
    def __init__(self, value=None):
        if value and not self.validate(value):
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)

    def validate(self, value):
        # Add validation logic for DD.MM.YYYY format
        pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_email(self, email):
        self.emails.append(Email(email))

    def add_address(self, address):
        self.addresses.append(Address(address))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def delete_email(self, email):
        self.emails = [e for e in self.emails if e.value != email]

    def delete_address(self, address):
        self.addresses = [a for a in self.addresses if a.value != address]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    # Implement edit_email and edit_address methods similarly

    def add_birthday(self, birthday):
        self.birthday = birthday

    def show_birthday(self):
        return str(self.birthday) if self.birthday else "Birthday not set."

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        emails_str = '; '.join(str(email) for email in self.emails)
        addresses_str = '; '.join(str(address) for address in self.addresses)
        return f"Contact name: {self.name}, phones: {phones_str}, emails: {emails_str}, addresses: {addresses_str}, birthday: {self.show_birthday()}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def find(self, name):
        if name in self.data:
            return self.data[name]
        
    @classmethod
    def load_from_file(cls, filename):
        address_book = cls()
        try:
            with open(filename, 'rb') as file:
                address_book.data = pickle.load(file)
        except FileNotFoundError:
            pass
        return address_book

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
            return "Contact added."
        else:
            return f"Contact '{record.name.value}' already exists."

    # Implement other methods like delete, find, get_birthdays_per_week, etc.

class Note:
    def __init__(self, content, tags):
        self.content = content
        self.tags = tags

    def edit_content(self, new_content):
        self.content = new_content

    def add_tag(self, tag):
        self.tags.append(tag)

class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def delete_notes_by_tag(self, tag):
        self.notes = [note for note in self.notes if tag not in note.tags]

    def search_notes_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    # Implement other note management methods

class PersonalAssistant:
    def __init__(self):
        self.address_book = AddressBook()
        self.notes_manager = NotesManager()

    # def input_error(func):
    #     def inner(*args, **kwargs):
    #         try:
    #             return func(*args, **kwargs)
    #         except ValueError:
    #             return "Give me name and phone please."
    #         except KeyError as e:
    #             return f"Error: Key '{e.args[0]}' does not exist."
    #         except IndexError:
    #             return "Error: Insufficient arguments."

    #     return inner




    # Implement contact management methods (add_contact, delete_contact, search_contact, etc.)

    # Implement note management methods (add_note, delete_note, search_note, etc.)

    #CONTACTS

    def display_contacts_with_upcoming_birthdays(self, days):
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.address_book.data.values():
            if record.birthday:
                birth_date = datetime.strptime(record.birthday.value, '%d.%m.%Y')
                if birth_date.month == today.month and birth_date.day - today.day <= days:
                    upcoming_birthdays.append(str(record))
        return
    
    # @input_error
    def add_contact(self, args, address_book):
        if len(args) == 2:
            name, phone = args
            # address_book[name] = phone
            record = Record(name)  # Create a Record instance with the provided name
            record.add_phone(phone)  # Add the phone number to the Record
            address_book.add_record(record)  # Add the Record to the AddressBook
            return "Contact added."
        else:
            return "Invalid command format for adding a contact."

    # @input_error
    def change_contact(self, args, address_book):
        if len(args) == 2:
            name, phone = args
            record = address_book.find(name)
            if record:
                record.phones = [Phone(phone)]  # Update the phone number for the found record
                return f"Phone number updated for {name}."
            else:
                return f"{name} does not exist in contacts."
        else:
            return "Invalid command format for changing a contact's phone number."

    # @input_error
    def get_phone(self, args, address_book):
        if len(args) == 1:
            name = args[0]
            record = address_book.find(name)
            if record:
                return f"Phone number for {name}: {record.phones}"
            else:
                return f"{name} does not exist in contacts."
        else:
            return "Invalid command format for retrieving a phone number."

    # @input_error
    def display_all(self, address_book):
        if address_book:
            result = "All contacts:\n"
            for record in address_book.data.values():
                result += f"{str(record)}\n"
            return result
        else:
            return "No contacts available."

    # @input_error
    def add_birthday(self, args, address_book):
        if len(args) == 2:
            name, birthday = args
            print(name)
            print(birthday)
            record = self.address_book.find(name)
            if record:
                record.add_birthday(birthday)
                return f"Birthday added for {name}."
            else:
                return f"{name} does not exist in the address book."
        else:
            return "Invalid command format for adding a birthday."

    # @input_error
    def show_birthday(self, args, address_book):
        if len(args) == 1:
            name = args[0]
            record = address_book.find(name)
            if record:
                return f"Birthday for {name}: {record.show_birthday()}"
            else:
                return f"{name} does not exist in the address book."
        else:
            return "Invalid command format for displaying a birthday."

    # @input_error
    def birthdays(self, address_book):
        upcoming_birthdays = address_book.get_birthdays_per_week()
        if upcoming_birthdays:
            return "Upcoming birthdays:\n" + "\n".join(upcoming_birthdays)
        else:
            return "No upcoming birthdays in the next week."

    #NOTES

    def add_note(self, content, tags):
        note = Note(content, tags)
        self.notes_manager.add_note(note)
        return "Note added successfully."

    def delete_notes_by_tag(self, tag):
        self.notes_manager.delete_notes_by_tag(tag)
        return f"Notes with tag '{tag}' deleted."

    def search_notes_by_tag(self, tag):
        matching_notes = self.notes_manager.search_notes_by_tag(tag)
        if matching_notes:
            result = f"Matching notes for tag '{tag}':\n"
            for note in matching_notes:
                result += f"Content: {note.content}, Tags: {note.tags}\n"
            return result
        else:
            return f"No notes found for tag '{tag}'."


def handle_command(user_input, assistant, filename):
    command, *args = user_input.split()
    command = command.lower()

    if command in ["close", "exit"]:
        assistant.address_book.save_to_file(filename)
        return "Good bye!"
    elif command == "hello":
        return "How can I help you?"
    elif command == "save":
        assistant.address_book.save_to_file(filename)
        return "Address book saved."
    elif command == "load":
        assistant.address_book = AddressBook.load_from_file(filename)
        return "Address book loaded."
    elif command == "add":
        return assistant.add_contact(args, assistant.address_book)
    elif command == "change":
        return assistant.change_contact(args, assistant.address_book)
    elif command == "phone":
        return assistant.get_phone(args, assistant.address_book)
    elif command == "all":
        return assistant.display_all(assistant.address_book)
    elif command == "add-birthday":
        return assistant.add_birthday(args, assistant.address_book.data)
    elif command == "show-birthday":
        return assistant.show_birthday(args, assistant.address_book)
    elif command == "birthdays":
        return assistant.birthdays(assistant.address_book)
    elif command == "add-note":
        content = ' '.join(args[:-1])
        tags = args[-1].split(',')
        return assistant.add_note(content, tags)
    elif command == "delete-notes-by-tag":
        return assistant.delete_notes_by_tag(args[0])
    elif command == "search-notes-by-tag":
        return assistant.search_notes_by_tag(args[0])
    else:
        return "Invalid command."

def main():   
    filename = "address_book.pkl"
    assistant = PersonalAssistant()
    assistant.address_book = AddressBook.load_from_file(filename)
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        result = handle_command(user_input, assistant, filename)
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()



# if command in ["close", "exit"]:
#     book.save_to_file(filename)
#     return "Good bye!"
# elif command == "hello":
#     return "How can I help you?"
# elif command == "save":
#     book.save_to_file(filename)
#     return "Address book saved."
# elif command == "load":
#     book = AddressBook.load_from_file(filename)
#     return "Address book loaded."
# elif command == "add":
#     return add_contact(args, book.data)
# elif command == "change":
#     return change_contact(args, book.data)
# elif command == "phone":
#     return get_phone(args, book.data)
# elif command == "all":
#     return display_all(book.data)
# elif command == "add-birthday":
#     return add_birthday(args, book.data)
# elif command == "show-birthday":
#     return show_birthday(args, book.data)
# elif command == "birthdays":
#     return birthdays(book)
# else:
#     return "Invalid command."



# filename = "address_book.pkl"
# book = AddressBook.load_from_file(filename)
# print("Welcome to the assistant bot!")

# while True:
#     user_input = input("Enter a command: ")
#     result = handle_command(user_input, book, filename)
#     print(result)
#     if result == "Good bye!":
#         break

# def parse_input(user_input, book, filename):
#     cmd, *args = user_input.split()
#     cmd = cmd.strip().lower()
#     return cmd, args, book, filename

