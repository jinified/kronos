import pytest
from datetime import datetime
from kronos.kronos import generateUserSchedule, getOverallSchedule, getConflictingAssignments, assignments2schedule, schedule2assignments


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
    occupancy = ([0] * duration, start, end)
    return {rotationId: (occupancy, assignments) for rotationId, assignments in rotations.items()}
    

@pytest.mark.parametrize('assignments', [
    ('122018', '482018', {
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
        'SE': {
        }})
], indirect=['assignments'])
def test_assignments2schedule(assignments):
    result = {'sjtsoonj': [{'rotationId': 'PMO', 'startDate': '01012018', 'endDate': '01042018'}], 'thava': [{'rotationId': 'PMO', 'startDate': '01032018', 'endDate': '01062018'}], 'soomay': [{'rotationId': 'PE', 'startDate': '01012018', 'endDate': '01042018'}], 'brina': [{'rotationId': 'PE', 'startDate': '01032018', 'endDate': '01062018'}], 'chris': [{'rotationId': 'PM', 'startDate': '01012018', 'endDate': '01042018'}], 'akmal': [{'rotationId': 'PM', 'startDate': '05072018', 'endDate': '05092018'}]}

    print(assignments)
    assert assignments2schedule(assignments) == result


@pytest.fixture(scope='function')
def schedule(request):
    result = {'sjtsoonj': [{'rotationId': 'PMO', 'startDate': '01012018', 'endDate': '01042018'}], 'thava': [{'rotationId': 'PMO', 'startDate': '01032018', 'endDate': '01062018'}], 'soomay': [{'rotationId': 'PE', 'startDate': '01012018', 'endDate': '01042018'}], 'brina': [{'rotationId': 'PE', 'startDate': '01032018', 'endDate': '01062018'}], 'chris': [{'rotationId': 'PM', 'startDate': '01012018', 'endDate': '01042018'}], 'akmal': [{'rotationId': 'PM', 'startDate': '05072018', 'endDate': '05092018'}]}
    return result

def test_schedule2assignment(schedule):
    assert schedule2assignments(schedule) == 2

@pytest.mark.parametrize('assignments', [
    ('122018', '482018', {
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
        'SE': {
        }})
], indirect=['assignments'])
def test_generateUserSchedule(assignments):
    result = [{'rotationId': 'PMO', 'startDate': '012018'}]
    assert generateUserSchedule(assignments, {}, lambda x: x) == result

def test_getOverallSchedule():
    assert getOverallSchedule([]) == {}

def test_getConflictingAssignments():
    assert getConflictingAssignments({}) == {}
