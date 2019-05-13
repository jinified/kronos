from kronos.kronos import generateUserSchedule, getOverallSchedule

def test_generateUserSchedule():
    result = [{'rotationId': 'PMO', 'startDate': '012018'}]
    assert generateUserSchedule({}, {}, lambda x: x) == result

def test_getOverallSchedule():
    assert getOverallSchedule([]) == {}
