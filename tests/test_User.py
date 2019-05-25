from kronos.User import User
from random import random


def test_strRepShouldMatchUserObject():
    userSchedule = []
    possibleRotations = ['PE', 'SE', 'PM', 'ARC', 'ANA', 'SYS'],
    joinDate = "01012018"
    displayJoinDate = "01 January 2018"
    assert str(User("Jason", userSchedule, possibleRotations, joinDate)) == f"Name: Jason Join: {displayJoinDate}\nSchedule: {userSchedule}\nPossible Rotations: {possibleRotations}"

def test_generateSchedule():
    userSchedule = []
    possibleRotations = ['PE', 'SE', 'PM', 'ARC', 'ANA', 'SYS']
    joinDate = "01012018"
    user = User("Jason", userSchedule, possibleRotations, joinDate)
    assert len(user.generateSchedule({'012018': {'PMO': 1}}, lambda x, y: random())) == len(possibleRotations)
