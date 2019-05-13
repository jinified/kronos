"""
User represents single unit of workforce that is undergoing the graduate training programme
"""


class User:
    def __init__(self, name, schedule, electives, joinDate="01012018"):
        self.name = name
        self.schedule = schedule
        self.electives = electives
        self.joinDate = datetime.strptime(joinDate, DISPLAY_DATE_FORMAT)
        logger.info(f"Name: {name} {schedule}")

    def valid(self, task, block):
        return block in self.available_blocks and task.valid(self)

    def earliestAvailableDate(self):
        # Returns earliest available date to start rotation based of existing
        # schedule or return join date if no schedule were generated
        if len(self.schedule) == 0:
            return self.joinDate
        else:
            date = sorted(
                self.schedule,
                key=lambda x: datetime.strptime(x[1][1], DISPLAY_DATE_FORMAT),
                reverse=True,
            )[0][1][1]
            return datetime.strptime(date, DISPLAY_DATE_FORMAT)

    def __repr__(self):
        return self.name
