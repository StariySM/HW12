from datetime import datetime, timedelta
from collections import UserDict
import pickle



class AddressBook(UserDict):
    def __init__(self):
        # self.n = 0
        self.data = {}
        self.index = 0

    def add_record(self, record):
        self.data.update({record.name.value: record})

    def __iter__(self):
        # print("start __iter__")
        return self

    def __next__(self):
        # print("start __next__")
        if self.index >= len(self.data.keys()):
            self.index = 0
            raise StopIteration
        key = list(self.data.keys())[self.index]
        self.index += 1
        return key, self.data[key]

    def iterator(self, n):
        # print("start iterator")
        index = 0
        for i in self:
            print(i)
            index += 1
            if index >= n:
                break


    def search(self, search_word):
        result = []
        for name, record in self.data.items():
            # print(type(record), record)
            if search_word.lower() in record.name.value.lower():
                result.append(name)
                continue
            for phone in record.phones:
                if search_word in phone.value:
                    result.append(name)
                    break
        return result


    def save_to_file(self, filename):
        with open(filename, 'wb') as fh:
            pickle.dump(self, fh)


    def read_from_file(self, filename):
        with open(filename, 'rb') as fh:
            self.data = pickle.load(fh).data



class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday

    def add(self, new_phone):
        self.phones.append(new_phone)

    def change(self, old_phone, new_phone):
        for i, ph in enumerate(self.phones):
            if ph == old_phone:
                self.phones[i] = new_phone
                break

    def delete(self, old_phone):
        for i, ph in enumerate(self.phones):
            if ph == old_phone:
                self.phones.pop(i)
                break

    def days_to_birthday(self):
        if self.birthday:
            current_birthday_day = datetime(year=datetime.now().year, month=self.birthday.value.month,
                                            day=self.birthday.value.day)
            days_to_birthday = current_birthday_day - datetime.now()
            return days_to_birthday.days


class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.isdigit():
            self.__value = value
        else:
            print("telephone number must include only digits")
            self.__value = None


class Birthday(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d.%m.%Y')
        except Exception:
            self.__value = None
            print("date must be in format day.month.year")

