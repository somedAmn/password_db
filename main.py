import sqlite3
import string

DATABASE_NAME = TABLE_NAME = 'passwords'
SYMBOLS = string.ascii_letters + string.digits + string.punctuation


def encryptor(word, key):
    """Шифрует слово по ключу"""
    key *= len(word) // len(key) + 1
    encrypted_word = ''
    for i, j in enumerate(word):
        index = SYMBOLS.index(j) + SYMBOLS.index(key[i])
        if index > 93:
            encrypted_word += SYMBOLS[index-93]
        else:
            encrypted_word += SYMBOLS[index]
    return encrypted_word


def decryptor(encrypted_word, key):
    """Дешифрует слово по ключу"""
    key *= len(encrypted_word) // len(key) + 1
    word = ''
    for i, j in enumerate(encrypted_word):
        index = SYMBOLS.index(j) - SYMBOLS.index(key[i])
        if index < 0:
            word += SYMBOLS[index+93]
        else:
            word += SYMBOLS[index]
    return word


def create_db():
    """Создаёт базу данных"""
    with sqlite3.connect(f'{DATABASE_NAME}.db') as db:
        cursor = db.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            website text NOT NULL,
            password text NOT NULL,
            email text,
            login text)"""
        )


def new_record(website, password, email=None, login=None):
    """Создаёт новую запись в базу данных"""
    with sqlite3.connect(f'{DATABASE_NAME}.db') as db:
        cursor = db.cursor()
        cursor.execute(
            f"""INSERT INTO {TABLE_NAME}
            (website, password, email, login)
            VALUES (:website, :password, :email, :login)""",
            {
                'website': website,
                'password': password,
                'email': email,
                'login': login
            }
        )


def select_records():
    """Выборка всех записей из базы данных"""
    with sqlite3.connect(f'{DATABASE_NAME}.db') as db:
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM {TABLE_NAME}')
        records = cursor.fetchall()
        if not records:
            print('В базе нет данных :(\n')
        return records


def passwords_in_console(records):
    """Выводит записи в консоль"""
    for record in records:
        for element in record:
            print(f' || {element} || ', end='')
        print('\n')


def passwords_in_txt(records):
    """Создаёт файл с записями"""
    with open('passwords.txt', 'w+') as file:
        for record in records:
            for element in record:
                file.write(f' || {element} || ')
            file.write('\n')
        print("В текущей директории создан файл с паролями!")


def data_entry():
    """Служит для работы в main, как ввод данных"""
    website = input('Введите вебсайт:\n')
    password = input('Введите пароль:\n')
    email = input('Введите электронную почту:\n')
    login = input('Введите логин:\n')
    key = input('Введите ключ шифровки:\n')
    return ({
        'website': website.strip(),
        'password': password.strip(),
        'email': email.strip(),
        'login': login.strip()
    }, key.strip()
    )


def combat_decryptor(func_output):
    """Служит для работы в main, как интерфейс к decryptor"""
    key = input('Введите ключ шифровки:\n')
    records = select_records()
    decrypted_records = list()
    for record in records:
        decrypted_element = list()
        for element in record:
            decrypted_element.append(decryptor(element, key))
        decrypted_records.append(decrypted_element)
    func_output(decrypted_records)


def main():
    create_db()

    available_commands_msg = """
        СПИСОК ДОСТУПНЫХ КОМАНД:
        list ---> список паролей в консоль
        txt  ---> создать txt файл с паролями
        new  ---> создать новый пароль
        help ---> показать команды
        exit ---> выход
    """

    print(f"""
        Добро пожаловать в хранилище паролей!
        {available_commands_msg}
    """)

    while True:
        command = input().strip().lower()

        if command == 'list':
            combat_decryptor(passwords_in_console)

        elif command == 'txt':
            combat_decryptor(passwords_in_txt)

        elif command == 'new':
            data, key = data_entry()
            encrypted_data = dict()
            for name, value in data.items():
                encrypted_data[name] = encryptor(value, key)
            try:
                new_record(
                    website=encrypted_data['website'],
                    password=encrypted_data['password'],
                    email=encrypted_data['email'],
                    login=encrypted_data['login']
                )
                print('Зашифрованные данные сохранены!\n')
            except Exception:
                print('ОШИБКА! Данные не сохранёны.')

        elif command == 'help':
            print(available_commands_msg)

        elif command == 'exit':
            break

        else:
            print('Несуществующая команда!\n')


if __name__ == '__main__':
    main()
