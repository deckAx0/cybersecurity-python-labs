import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../')))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

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
