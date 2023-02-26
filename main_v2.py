from collections import UserDict
from datetime import datetime
from itertools import islice

DEBUG_MODE = True

# decorator Errors handling


def decorator(func):
    if DEBUG_MODE:
        print("Debugger mode is on")

    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return f"Wrong input{IndexError} (enter '?' for help). Try again!"
        except ValueError:
            return f"Wrong input.({ValueError}) Try again!"
        except KeyError:
            return f"Wrong input. No such entity.({KeyError}) Try again!"
        except TypeError:
            return f"Wrong input.({TypeError}) (enter '?' for help). Try again!"
    return inner


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    @decorator
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"{self.value}"


class Name(Field):
    @Field.value.setter
    @decorator
    def value(self, name):
        if name.isalpha() and len(name) > 1:
            self._value = name.capitalize()
        else:
            print("Name too short. Should be 2 letters at least")
            self._value = input("Enter contact name\n").capitalize()


class Phone(Field):
    @Field.value.setter
    def value(self, phone):
        clean = ''
        for p in phone:
            clean += p.strip("-+)( _")
        if clean.isdigit() and len(clean) > 9:
            self._value = clean


class Birthday(Field):

    @property
    def value(self):

        return self._value

    @Field.value.setter
    def value(self, bday):
        clean = ''
        for d in bday:
            clean += d.strip("-+).,( \/_")
        if clean.isdigit() and len(clean) == 8:
            self._value = clean


class Record:
    def __init__(self, name: Name, phone: Phone = None, bday: Birthday = None):
        self.name = name
        self.phone = phone
        self.bday = bday

    def add_phone(self, phone) -> None:
        ab.data[self.value].phone = f" {ab.data[self.value].phone}, {phone.value}"

    def change_phone(self, phone) -> None:
        ab.data[self.value].phone = phone.value
        return f"Number for user '{ab.data[self.value].name}' changed to: '{ab.data[self.value].phone}'"

    def del_phone(self, phone) -> None:
        ab.data[self.value].phone = 'removed'

    def add_birthday(self, birthday: Birthday):
        ab.data[self.value].bday = birthday.value

    def days_to_birthday(self):
        d = ab.data[self.value].bday.value

        if d:
            current_date = datetime.now()
            n_str = d[0:2]+'-'+d[2:4]+'-'+d[4:9]
            dt_str = datetime.strptime(
                n_str, "%d-%m-%Y").replace(year=current_date.year).date()
            delta = dt_str-current_date.date()
            return print(f"{delta.days} days left to {ab.data[self.value].name} birthday")
        else:
            return print("No birth date set")


class AddressBook(UserDict):

    current_index = 0

    def __repr__(self):
        return f"{self.data}"

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
        # self.data[record.name.value]

    def del_record(self, key) -> Record | None:
        self.data.pop(key.value)
        print(f"Contact '{key.value}' removed from Address Book")

    def show_all(self) -> str:
        if self.data == {}:
            print('No contacts yet')
        
        for v in self.data.keys():
            print(f"Name: {self.data[v].name}, phone: {self.data[v].phone}, birthday {self.data[v].bday}")

    def iterator(self, num: int = 2):
        while self.current_index < len(self.data):
            n_dict = dict(islice(self.data.items(),
                          self.current_index, self.current_index + num))
            for v in n_dict.keys():
                print(
                    f"Name: {n_dict[v].name}, phone: {n_dict[v].phone}, birthday {n_dict[v].bday}")
            yield f'next {num} contacts'
            self.current_index += num
        self.current_index = 0

def main():
    print("Hello. This is Address Book v 0.1.1")
    print("""Enter 'a' to add a contact, 's' to show all contacts, 'dr' to delete a contact, 'cp' to change phone, 'df' to delete phone, 'dtb' for days to birthday, 'ad' add birthday and 'q' to quit""")

    while True:
        choice = input("Enter your choice\n>>>")
        if choice == 'q':
            break
        elif (choice == 'a'):
            name = Name(input("Enter contact name\n"))
            phone = Phone(input("Enter contact phone number\n"))
            bday = Birthday(input("Enter contact birthday (mm/dd/yyy)\n"))
            rec = Record(name, phone, bday)
            ab.add_record(rec)
        elif (choice == 's'):
            ab.show_all()
        elif (choice == 'i'):
            for i in ab.iterator(num=3):
                print(i)
        elif (choice == 'dr'):
            name = Name(input("Enter contact name\n"))
            ab.del_record(name)
        elif (choice == 'af'):
            name = Name(input("Enter contact name\n"))
            phone = Phone(input("Enter phone number to be added\n"))
            Record.add_phone(name, phone)
        elif (choice == 'cp'):
            name = Name(input("Enter contact name\n"))
            phone = Phone(input("Enter new phone number\n"))
            Record.change_phone(name, phone)
        elif (choice == 'dp'):
            name = Name(input("Enter contact name\n"))
            phone = Phone(input("Enter phone number to delete\n"))
            Record.del_phone(name, phone)
        elif (choice == 'dtb'):
            name = Name(input("Enter contact name\n"))
            Record.days_to_birthday(name)
        elif (choice == 'ab'):
            name = Name(input("Enter contact name\n"))
            bday = Birthday(input("Enter contact birthday (mm/dd/yyy)\n"))
            Record.add_birthday(name, bday)
        elif (choice == '?'):
            print("""Enter 'a' to add a contact, 's' to show all contacts, 'dr' to delete a contact, 'cp' to change phone, 'df' to delete phone, 'dtb' for days to birthday, 'ad' add birthday and 'q' to quit""")
        else:
            print("Incorrect choice. Need to enter the choice again. for help enter '?'")


if __name__ == "__main__":
    ab = AddressBook()
    # name = Name('Bill')
    # phone = Phone('1234567890')
    # bday = Birthday('24.05.1985')
    # rec = Record(name, phone, bday)
    # name = Name('bob')
    # phone = Phone('0000000000000')
    # bday = Birthday('24.10.1995')
    # rec1 = Record(name, phone, bday)
    # ab.add_record(rec1)
    # name = Name('koN')
    # phone = Phone('1233218799000')
    # bday = Birthday('00.00.1905')
    # rec2 = Record(name, phone, bday)
    # ab.add_record(rec2)
    # ab.add_record(rec)
    main()



# @classmethod
# def read_file(self):
#     pass


# def write_file(self):
#     pass
