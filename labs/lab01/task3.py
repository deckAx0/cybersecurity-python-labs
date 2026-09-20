import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../')))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

PERSONAL_SALT = str(VARIANT_NUMBER).zfill(5)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

users_db = []

# Task 3
users_to_register = (
                        ('admin', 'password1234567890'),
                        ('qa_test', 'Axw1#0!Zq3C1mgA@a07MnAg'),
                        ('nazar', '12345678901234567890'),
                        ('matviy', 'Vk!8A?7$aCjA19JaAh%qwgA45'),
                        ('ebaka228', 'ebaka22888888888'),
                        ('kerberos_cooker', 'roasting_attacks_enjoyer'),
                        ('wiener', 'peteraasdfasdeasdfsadfgdsdsf'),
                        ('" OR 1=1-- -', 'asdfasdfasdf" OR 1=1-- -'),
                        ('osiris', '4bid_the_best_XDDDDD'),
                        ('{{7*7}}', 'reallystrongpassword123456')
                        )

class ValidationError(Exception):
    pass


def generate_hash(password: str, salt: str = "00000") -> str:
    min_length = 14

    if not password or not salt:
        raise ValueError("Сіль або пароль не можуть бути пустими")

    if min_length > len(password):
        raise ValidationError(f"Пароль має містити не менше {min_length} символів\nВаш пароль містить {len(password)} символів")

    return (hashlib.sha3_256((salt+password).encode())).hexdigest()


def create_user(username, password):
    return (username, generate_hash(password, PERSONAL_SALT))


def create_users(users_list):
    db_file = os.path.join(DATA_DIR, 'users.csv')

    try:
        os.makedirs(DATA_DIR, exist_ok=True)

        if not os.path.isfile(db_file):
            open(db_file, "w").close()
    except (OSError, PermissionError, FileNotFoundError) as e:
        print(f'[-] Халепа! Не змогли створити файл/папку: {e}')
        return False
    else:
        print(f'[+] Створили БД за шляхом: {db_file}\n')

    try:
        with open(db_file, 'w', newline='', encoding='utf-8') as db:
            writer = csv.writer(db)
            writer.writerow(['Username', 'password_hash'])
            writer.writerows(create_user(username, password) for username, password in users_list)
    except (OSError, PermissionError, ValidationError, ValueError) as e:
        print(f'[-] Помилка: {e}')
        return False
    else:
        print('[+] Користувачів записано!\n')
        return True


def read_db():
    path = os.path.join(DATA_DIR, 'users.csv')

    try:
        df = pd.read_csv(path)
        print(df)

        list_of_lists = df.values.tolist()
        return list_of_lists

    except (OSError, PermissionError, FileNotFoundError) as e:
        print(f'[-] Помилка: {e}')
        return False


def log_event(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = False
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            username = args[0] if args else kwargs.get("username", "")
            event = {
                "event": "login",
                "user": username,
                "result": "success" if result else "failure",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "args": [],
                "kwargs": {},
            }
            log_path = os.path.join(DATA_DIR, 'log.json')
            try:
                os.makedirs(DATA_DIR, exist_ok=True)

                if os.path.isfile(log_path):
                    with open(log_path, 'r', encoding='utf-8') as f:
                        try:
                            logs = json.load(f)
                        except json.JSONDecodeError:
                            logs = []
                else:
                    logs = []

                logs.append(event)

                with open(log_path, 'w', encoding='utf-8') as f:
                    json.dump(logs, f, ensure_ascii=False, indent=2)
            except (OSError, FileNotFoundError, PermissionError) as e:
                print(f'[-] Не вдалося записати лог: {e}')

    return wrapper


@log_event
def login(username: str, password: str) -> bool:
    if not username or not password:
        raise ValueError('Username та password не можуть бути порожніми')

    password_hash = generate_hash(password, PERSONAL_SALT)
    is_valid = any(u == username and h == password_hash for u, h in users_db)

    if not is_valid:
        print('[-] Неправильний логін або пароль')
        return False

    print('[+] Креди Вірні')
    return True


def main():
    global users_db

    db_init = create_users(users_to_register)

    if not db_init:
        return

    users_db = read_db()

    if users_db is False:
        return

    while True:
        try:
            username = input('Username: ')
            password = input('Password: ')

            if login(username, password):
                break
        except (ValueError, ValidationError) as e:
            print(f'[-] {e}')