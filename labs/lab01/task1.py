import os
import random
import re
import string
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../')))
from shared.student import STUDENT_NAME, VARIANT_NUMBER


def generate_duplicate_passwords(passwords):
    try:
        for i in range(3):
            index = random.randint(0, len(passwords) - 1)

            random_password = passwords[index]
            passwords.append(random_password)
        return True
    except Exception as error: 
        print(f"[-] Помилка: {error}")
        return False


def analyze_char_groups(password, criteria):
    result = {
            "is_longer": False,
            "has_digits": False,
            "has_upper": False,
            "has_special": False
            }

    is_longer = len(password) >= criteria.get("min_length")
    has_digits = bool(re.search(r"[0-9]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_special = any(char in string.punctuation for char in password)

    if is_longer:
        result["is_longer"] = True

    if has_digits:
        result["has_digits"] = True

    if has_upper:
        result["has_upper"] = True

    if has_special:
        result["has_special"] = True

    return result


def test_security_password(password, forbidden_passwords, criteria, all_passwords):
    security_level = None
    min_length = criteria.get("min_length")

    result = analyze_char_groups(password, criteria)

    has_lower = bool(re.search(r"[a-z]", password))
    has_all = (result["is_longer"] and result["has_digits"]
               and result["has_upper"] and result["has_special"])
    some_criteria = result["has_digits"] or result["has_upper"] or result["has_special"]

    if password in forbidden_passwords or len(password) < min_length:
        security_level = "forbidden"
        return security_level, result

    if result["has_digits"] or result["has_upper"] or result["has_special"] or has_lower:
        security_level = "weak"

    if result["is_longer"] and some_criteria and not has_all:
        security_level = "middle"

    if has_all:
        security_level = "strong"

    if has_all and len(password) >= min_length + 4 and all_passwords.count(password) == 1:
        security_level = "very strong"

    return security_level, result


if __name__ == "__main__":
    passwords = ["Compli4nc3@Check", "weak", "Risk@Ass3ssment", "guest",
                "Vulner4bility@Scan", "temp", "P3netration@Test", "demo", "S3curity@Audit",
                "trial"]

    criteria = {"min_length": 8,
                "require_digits": True,
                "require_upper": True,
                "require_special": True
                }

    forbidden_passwords = {"weak", "guest", "temp", "demo", "trial", "password"}
    min_length = criteria.get("min_length")

    if generate_duplicate_passwords(passwords):
        time.sleep(1)
        print("[+] 3 дублікати паролів успішно згенеровані та додані до списку паролів.")
        time.sleep(1)
        print("[+] Оновлений список паролів:\n" + "\n".join(passwords))
        time.sleep(5)
        print("\n[+] Запускаю перевірку пролів...\n")
        time.sleep(5)

    for password in passwords:
        level, dic = test_security_password(password, forbidden_passwords, criteria, passwords)

        print(f"Пароль: {password} | Категорія - {level}\n"
              f"- Має цифру: {dic['has_digits']}\n"
              f"- Має велику букву: {dic['has_upper']}\n"
              f"- Має спеціальний символ: {dic['has_special']}\n"
              f"- Достатня довжина: {dic['is_longer']}\n")
        time.sleep(0.8)

    print("[+] Кінець")