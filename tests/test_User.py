from kronos.User import User


def test_strRepShouldMatchUserObject():
    assert (
        str(User("Jason", [], [], "01012018"))
        == f"Name: Jason Join: 01 January 2018\nSchedule: []\nElectives: []"
    )
