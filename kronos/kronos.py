"""
Kronos: A simple scheduler for graduate training programme

Entities: User, Schedule, Rotation
"""

from operator import itemgetter
from datetime import datetime, timedelta


def schedule2assignments(schedule):
    """ Convert schedule object to assignment object
    """
    rotations = {}
    for userId, userSchedule in schedule.items():
        for rotation in userSchedule:
            id = rotation["rotationId"]
            if id not in rotations:
                rotations[id] = [[{}], []]
            print(rotations[id][0][0])
            startDate, endDate = itemgetter("startDate", "endDate")(rotation)
            start = datetime.strptime(startDate, "%d%m%Y")
            end = datetime.strptime(endDate, "%d%m%Y")
            duration = int((end - start).days / 7.0)
            for i in range(duration):
                date = (start + timedelta(weeks=i)).strftime("%W%Y")
                if date not in rotations[id][0][0]:
                    rotations[id][0][0][date] = 0
                rotations[id][0][0][date] += 1
            rotations[id][1].append((userId, startDate, endDate))
        sortedDate = sorted(list(rotations[id][0][0].keys()))
        if len(rotations[id][0]) < 2:
            rotations[id][0].append(sortedDate[0])
            rotations[id][0].append(sortedDate[-1])
        elif sortedDate[0] < rotations[id][0][1]:
            rotations[id][0][1] = sortedDate[0]
        elif len(rotations[id][0]) > 2 and sortedDate[-1] > rotations[id][0][2]:
            rotations[id][0][2] = sortedDate[-1]
    print(rotations)
    return rotations


def assignments2schedule(assignments):
    """ Convert assignment object to overall schedule
    """
    users = {}
    for rotationId, rotationInfo in assignments.items():
        for userId, userAssignment in rotationInfo[1].items():
            if userId not in users:
                users[userId] = []
            users[userId].append(
                {
                    "rotationId": rotationId,
                    "startDate": userAssignment[0],
                    "endDate": userAssignment[1],
                }
            )
    print(users)
    return users


def generateUserSchedule(user, assignments, scoring_function):
    """ Generate most optimal user schedule
    Parameters:
        user (object): User
        assignments (dict): Time-bounded assignments
        scoring_function (function): scoring function to rank possible assignments

    Returns:
        schedule (list): list of rotations
    """
    return [{"rotationId": "PMO", "startDate": "012018"}]


def getOverallSchedule(users):
    """ Generate overall schedule from individual user's schedule
    Parameters:
        users (list): list of Users

    Returns:
        schedule (dict): overall assignments
    """
    return {}


def getConflictingAssignments(schedule):
    """ Get list of assignments which exceeded rotation capacity
    Parameters:
        schedule (dict): overall assignments

    Returns:
        confictingAssignmentsByRotation (dict): overall schedule with conflicting assignments
    """
    return {}


if __name__ == "__main__":
    pass
