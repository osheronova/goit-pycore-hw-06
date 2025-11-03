from collections import UserDict

class PhoneValidationError(ValueError): 
    pass  # custom error

# base field
class Field:
    def __init__(self, value): self.value = value
    def __str__(self): return str(self.value)

class Name(Field): 
    pass

# phone: must be 10 digits
class Phone(Field):
    def __init__(self, value: str):
        value = str(value)
        if not (value.isdigit() and len(value) == 10):
            raise PhoneValidationError("Phone must be 10 digits")
        super().__init__(value)

# contact record
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str): self.phones.append(Phone(phone))
    def find_phone(self, value: str):
        return next((p for p in self.phones if p.value == value), None)

    def remove_phone(self, value: str) -> bool:
        p = self.find_phone(value)
        if p: self.phones.remove(p)
        return bool(p)

    def edit_phone(self, old: str, new: str) -> bool:
        p = self.find_phone(old)
        if p:
            p.value = Phone(new).value
        return bool(p)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# address book
class AddressBook(UserDict):
    def add_record(self, record: Record): 
        self.data[record.name.value] = record
    def find(self, name: str): 
        return self.data.get(name)
    def delete(self, name: str) -> bool: 
        return self.data.pop(name, None) is not None


# Demo test
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
