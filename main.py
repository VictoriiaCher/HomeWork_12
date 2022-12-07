from time import sleep
from ABook import ABook, Record


def input_error(func):
    def wrapper(user_data):
        try:
            return func(user_data)
        except KeyError:
            return f"Contact is not found. Try again!"
        except ValueError:
            return f"Invalid format of data. Try again!"
        except IndexError:
            return f"You didn't enter the contact name or phone. Try again!"
        except RuntimeError:
            return f"This is the end of AddressBook"
        except FileNotFoundError:
            return f"File not found. Try again!"

    return wrapper


@input_error
def handler(command: str):
    return HANDLER[command]


def main():
    user_input = input("For start say 'hello': ").lower()

    while True:
        command, user_data = handle_user_input(user_input)
        # try:
        output = handler(command)(user_data)
        # except TypeError:
        #     print(f"I dont understand the command '{command}'. Try again!")
        # else:
        print(output)
        user_input = input("\n" + "How can i help you?: ").lower()


@input_error
def handle_user_input(user_input: str) -> tuple:
    """Функція 'розпізнає' команду та інформацію про контакт"""

    command, user_data = user_input.split(" ")[0], user_input.split(" ")[1:]
    return command, user_data


@input_error
def hello_handler(*args, **kwargs) -> str:
    """Функція считує з файлу та виводить на екран текст привітання"""

    with open('HELP.txt', "r") as hello:
        for line in hello.readlines():
            print(line, end='')
    return f'.'


@input_error
def add_record(user_data: list) -> str:
    """Функція додає новий контакт у список контактів"""

    name = user_data[0]
    if len(user_data) == 1:
        phone = []
        birthday = None
    elif len(user_data) == 2:
        phone = user_data[1]
        birthday = None
    else:
        phone = user_data[1]
        birthday = user_data[2]

    return BOOK.add_record(Record(name, phone, birthday))


@input_error
def add_phone(user_data: list) -> str:
    """Функція додає новий номер телефону до обраного контакту"""

    return BOOK[user_data[0]].add_phone(user_data[1])


@input_error
def add_birthday(user_data: list) -> str:
    """Функція додає дату народження контакту"""

    return BOOK[user_data[0]].add_birthday(user_data[1])


@input_error
def change_birthday(user_data: list) -> str:
    """Функція змінює дату народження контакту"""

    return BOOK[user_data[0]].change_birthday(user_data[1])


@input_error
def del_birthday(user_data: list) -> str:
    """Функція видаляє дату народження контакту"""

    return BOOK[user_data[0]].remove_birthday()


@input_error
def change_phone(user_data: list) -> str:
    """Функція замінює номер телефону існуючого контакту"""

    return BOOK[user_data[0]].change_phone(user_data[1], user_data[2])


@input_error
def show_phone_handler(user_data: list) -> str:
    """Функція виводить на екран номер телефону існуючого контакту"""

    return BOOK[user_data[0]].show_phones()


@input_error
def bye_handler(*args, **kwargs):
    """Закінчення діалогу"""

    print("Goodbye!")
    sleep(3)
    return exit()


@input_error
def del_record(user_data: list) -> str:
    """Функція видаляє контакт зі списку контактів або номер телефону контакту"""

    del BOOK[user_data[0]]
    return f"'{user_data[0]}' is delete"


@input_error
def del_phone(user_data: list) -> str:
    """"Функція видаляє вказаний номер телефону контакту"""

    return BOOK[user_data[0]].remove_phone(user_data[1])


@input_error
def show_all_handler(*args, **kwargs) -> str:
    """Функція виводить на екран весь список контактів"""

    dict_to_str, count = [], 0
    for key, value in BOOK.items():
        count += 1
        if value.birthday:
            days = BOOK[key].days_to_birthday()
            dict_to_str.append("  {}. {}, {} days to birthday".format(count, value, days))
        else:
            dict_to_str.append("  {}. {}".format(count, value))
    dict_output = "\n".join(dict_to_str)

    return f"{dict_output}"


@input_error
def pagination(user_data: list):
    num = int(user_data[0])
    pages = BOOK.iterator(num)
    result = ''
    for page in pages:
        for name in page:
            result += f"\n {BOOK[name]}"
    return result


@input_error
def search(user_data):
    found = BOOK.search(str(user_data[0]))
    sep = '\n'
    return f"{sep.join(found)}" if found else f"Sorry, no matches found"


@input_error
def save_to_file(*args, **kwargs):
    name_file = input("Please, enter file name: ") + '.bin'
    return BOOK.save_to_file(name_file)


@input_error
def load_from_file(*args, **kwargs):
    name_file = input("Please, enter the file name from which you want to download: ") + '.bin'
    return BOOK.load_from_file(name_file)


BOOK = ABook()

HANDLER = {
    "hello": hello_handler,
    "add": add_record,
    "add_phone": add_phone,
    "change_phone": change_phone,
    "del_phone": del_phone,
    "add_birthday": add_birthday,
    "change_birthday": change_birthday,
    "del_birthday": del_birthday,
    "show_all": show_all_handler,
    "show": pagination,
    "del": del_record,
    "phone": show_phone_handler,
    "search": search,
    "save": save_to_file,
    "load": load_from_file,
    "exit": bye_handler,
    "close": bye_handler,
    "good": bye_handler,
}

if __name__ == "__main__":
    main()
