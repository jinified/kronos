"""
Kronos: A simple scheduler for graduate training programme

Entities: User, Schedule, Rotation
"""


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
