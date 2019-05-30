"""
Kronos: A simple scheduler for graduate training programme

Entities: User, Schedule, Rotation
"""

from operator import itemgetter
from datetime import datetime, timedelta


def getRotationCapacity(rotationId, startDate, endDate, assignments):
    """ Calculate number of users assigned to a particular rotation during the specified duration
    """
    start = datetime.strptime(startDate, "%d%m%Y")
    end = datetime.strptime(endDate, "%d%m%Y")
    duration = int((end - start).days / 7.0)
    # Weeks involved during the rotation
    weeks = [(start + timedelta(weeks=x)).strftime("%W%Y") for x in range(0, duration)]
    capacity = sum(itemgetter(*weeks)(assignments[rotationId][0][0]))
    return capacity


def score_assignment(
    assignments,
    solution,
    earliestAvailableDate,
    core_rotations=["PMO", "PE", "SE", "PM"],
    rotation_duration={
        "PMO": 12,
        "PE": 12,
        "SE": 12,
        "PM": 12,
        "SYS": 12,
        "ARC": 12,
        "ANA": 12,
    },
):
    """ Calculate loss function for suggested solution (negative = better)
    Parameters:
        assignments (dict): global assignment object by rotation
        solution (dict): rotation assignment for a user
        earliestAvailableDate (date): earliest date where a user can be assigned a rotation
        core_rotations (list): rotation that should be completed first
        rotation_duration (dict): duration of each rotation
    """
    print(solution)
    # SOFT CONSTRAINT 1 - Core rotations should be completed in the first 4 rotations if possible
    core_first_loss = sum(
        [
            -3 if x[0] in core_rotations else 0
            for x in solution
            if int(x[1]) <= len(core_rotations)
        ]
    )
    # SOFT CONSTRAINT 2 - External Assignment must be assigned last
    external_assignment_loss = (
        99 if "EXT" in [x[0] for x in solution] and solution[-1][0] != "EXT" else 0
    )

    # Calculate timing of each rotation from solution
    solution = [
        (
            x[0],
            rotation_duration[x[0]]
            + (sum([rotation_duration[x[0]] for x in solution[:i]]) if i != 0 else 0),
        )
        for i, x in enumerate(solution)
    ]
    startDate = earliestAvailableDate
    schedule = []
    for x in solution:
        endDate = startDate + timedelta(weeks=x[1]) - timedelta(days=1)
        # Make sure the date falls on weekday
        if endDate.weekday() >= 5:
            endDate -= timedelta(endDate.weekday() - 4)
        schedule.append(
            (x[0], startDate.strftime("%d%m%Y"), endDate.strftime("%d%m%Y"))
        )
        startDate += timedelta(weeks=x[1])

    spread_first_loss = sum(
        [getRotationCapacity(x[0], x[1], x[2], assignments) for x in schedule]
    )
    loss = core_first_loss + external_assignment_loss + spread_first_loss
    return loss


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
