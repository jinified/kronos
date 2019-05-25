import pytest
from datetime import datetime, timedelta
from kronos.kronos import generateUserSchedule, getOverallSchedule, getConflictingAssignments, assignments2schedule


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
    return {(start + timedelta(weeks=x)).strftime('%W%Y'): rotations for x in range(duration)}
    

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
    result = {'sjtsoonj': {'PMO': {'startDate': '01012018', 'endDate': '01042018'}}, 'thava': {'PMO': {'startDate': '01032018', 'endDate': '01062018'}}, 'soomay': {'PE': {'startDate': '01012018', 'endDate': '01042018'}}, 'brina': {'PE': {'startDate': '01032018', 'endDate': '01062018'}}, 'chris': {'PM': {'startDate': '01012018', 'endDate': '01042018'}}, 'akmal': {'PM': {'startDate': '05072018', 'endDate': '05092018'}}}

    assert assignments2schedule(assignments) == result


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
