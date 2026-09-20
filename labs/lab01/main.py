from task1 import *
from task2 import *
from task3 import *
import time


# Task 1
passwords = ["Compli4nc3@Check", "weak", "Risk@Ass3ssment", "guest",
                "Vulner4bility@Scan", "temp", "P3netration@Test", "demo", "S3curity@Audit",
                "trial"]

criteria = {"min_length": 8,
                "require_digits": True,
                "require_upper": True,
                "require_special": True
                }

# Task 2
users = {
 "ai_security_expert": {"role": "ai_security", "clearance": 4, "department":
"AI Security", "active": True},
 "ml_engineer": {"role": "ml_engineer", "clearance": 3, "department":
"Machine Learning", "active": True},
 "data_engineer": {"role": "data_engineer", "clearance": 2, "department":
"Data Engineering", "active": True},
 "research_assistant": {"role": "researcher", "clearance": 2, "department":
"Research", "active": True},
 "training_bot": {"role": "bot_account", "clearance": 1, "department":
"Automation", "active": False}
}

resources = [("ai_models", 4), ("training_datasets", 3), ("data_pipelines", 2),
("research_notebooks", 2), ("model_artifacts", 4), ("synthetic_data", 1),
("adversarial_tests", 3), ("model_registry", 4), ("feature_stores", 2),
("public_models", 1)]

security_levels = ("Open Source", "Internal Research", "Proprietary", "Trade Secret")

blocked_users = {"training_bot", "model_theft", "data_poisoning_acc"}




def run_tasks():
    print('             1. Завдання:          ')
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

    time.sleep(2)
    print('             2. Завдання:          ')

    print_resources_level(resources=resources, security_levels=security_levels)

    print("[+] Введіть назву юзера та ресурсу для пееревірки доступу або exit в будь який з полів для виходу\n")

    while True:
        user = input("User: ")
        resource = input("Resource: ")

        if "exit" == user.lower() or "exit" == resource.lower():
            break

        if resource not in [r[0] for r in resources]:
            print("Немає такого ресурсу\n")
            continue

        res = check_user_access(user=user, resource=resource, users=users, blocked_users=blocked_users, resources=resources)

        print(f"user={user} resource={resource} -> {next(iter(res.keys()))} ({next(iter(res.values()))})\n")

    time.sleep(2)
    print('             3. Завдання:          ')
    main()



if __name__ == '__main__':
    run_tasks()