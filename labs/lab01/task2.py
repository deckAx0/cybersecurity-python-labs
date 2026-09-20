import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../')))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

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

def print_resources_level(resources, security_levels):
    for resource in resources:
        res, level = resource
        print(f"Resource: {res} | Level: {security_levels[level-1]}")



def check_user_access(user, resource ,users, blocked_users, resources):

    for res1 in resources:
        if resource in res1:
            level_access = res1[1]
            

    if user not in users:
        return {"DENY": "User not found"}

    is_active = users.get(user).get("active")
    user_clearance = users.get(user).get("clearance")

    if user in blocked_users:
        return {"DENY": "User is blocked"}

    if user in users and not is_active:
        return {"DENY":"Account inactive"}

    if user_clearance >= int(level_access):
        return {"ALLOW":""}

    return {"DENY": "Insufficient clearance"}


if __name__ == "__main__":
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
        