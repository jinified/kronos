"""
User represents single unit of workforce that is undergoing the graduate training programme
"""

from datetime import datetime


class User:

    DATE_FORMAT = "%d%m%Y"

    def __init__(self, name, schedule, electives, joinDate):
        self.name = name
        self.schedule = schedule
        self.electives = electives
        self.joinDate = datetime.strptime(joinDate, User.DATE_FORMAT)

    def __repr__(self):
        return f'User("Jason", [], [], "12012018")'

    def __str__(self):
        joinDate = self.joinDate.strftime("%d %B %Y")
        return f"Name: {self.name} Join: {joinDate}\nSchedule: {self.schedule}\nElectives: {self.electives}"

    def earliestAvailableDate(self):
        # Returns earliest available date to start rotation based of existing
        # schedule or return join date if no schedule were generated
        if len(self.schedule) == 0:
            return self.joinDate
        else:
            date = sorted(
                self.schedule,
                key=lambda x: datetime.strptime(x[1][1], User.DATE_FORMAT),
                reverse=True,
            )[0][1][1]
            return datetime.strptime(date, User.DATE_FORMAT)
