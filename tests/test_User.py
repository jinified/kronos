import pytest
from kronos.User import User
from kronos.kronos import score_assignment
from datetime import datetime, timedelta


@pytest.fixture(scope='function')
def assignments(request):
    """ Generate global assignment object
    Parameters:
        duration (tuple): pair of date string that denote duration that will be covered by the assignments

    Returns:
        assignment (obj): assignment object
    """
    start, end, rotations = request.param
    start = datetime.strptime('1' + start, "%w%W%Y")
    end = datetime.strptime('1' + end, "%w%W%Y")
    duration = int((end - start).days / 7.0)
    # Number of assignments per unit time
    occupancy = ({(start + timedelta(weeks=x)).strftime('%W%Y'): 0 for x in range(0, duration + 1)}, start.strftime('%W%Y'), end.strftime('%W%Y'))
    return {rotationId: (occupancy, assignments) for rotationId, assignments in rotations.items()}
def test_strRepShouldMatchUserObject():
    userSchedule = []
    possibleRotations = ['PE', 'SE', 'PM', 'ARC', 'ANA', 'SYS'],
    joinDate = "01012018"
    displayJoinDate = "01 January 2018"
    assert str(User("Jason", userSchedule, possibleRotations, joinDate)) == f"Name: Jason Join: {displayJoinDate}\nSchedule: {userSchedule}\nPossible Rotations: {possibleRotations}"

@pytest.mark.parametrize('assignments', [
    ('012018', '522023', {
        'PMO': {
            'sjtsoonj': ('01012018', '01042018'),
            'thava': ('01032018', '01062018')
        },
        'PE': {
            'soomay': ('01012018', '01042018'),
            'brina': ('01032018', '01062018')
        },
        'PM': {
            'chris': ('01012018', '01042018'),
            'akmal': ('05072018', '05092018')
        },
        'SYS': {
            'chris': ('01012019', '01042019'),
            'akmal': ('05092018', '05112018')
        },
        'ARC': {
            'jiawei': ('01012019', '01042019'),
            'tauteng': ('05092018', '05112018')
        },
        'ANA': {
            'jin': ('01012019', '01042019'),
            'thava': ('05092018', '05112018')
        },
        'SE': {
        }})
], indirect=['assignments'])
def test_generateSchedule(assignments):
    userSchedule = []
    possibleRotations = ['PE', 'SE', 'PM', 'ARC', 'ANA', 'SYS']
    joinDate = "01012018"
    user = User("Jason", userSchedule, possibleRotations, joinDate)
    assert len(user.generateSchedule(assignments, score_assignment)) == len(possibleRotations)
