"""
User represents single unit of workforce that is undergoing the graduate training programme
"""

import numpy as np
from datetime import datetime
from constraint import Problem, AllDifferentConstraint


class User:

    DATE_FORMAT = "%d%m%Y"

    def __init__(self, name, schedule, possibleRotations, joinDate):
        """
        Parameters:
            name (str):                 username
            schedule (str):             user's existing schedule
            possibleRotations (list):   possible rotations for the user
            joinDate (str):             date where user start the programme in ddMMYY format
        """
        self.name = name
        self.schedule = schedule
        self.possibleRotations = possibleRotations
        self.order = [
            str(i)
            for i in range(
                len(self.schedule) + 1, len(possibleRotations) + len(self.schedule) + 1
            )
        ]
        self.joinDate = datetime.strptime(joinDate, User.DATE_FORMAT)

    def __repr__(self):
        return f'User("Jason", [], [], "12012018")'

    def __str__(self):
        joinDate = self.joinDate.strftime("%d %B %Y")
        return f"Name: {self.name} Join: {joinDate}\nSchedule: {self.schedule}\nPossible Rotations: {self.possibleRotations}"

    def generateSchedule(self, assignments, scoring_function):
        """ Generate schedule for a user based on scoring_function and user's existing schedule
        """
        problem = Problem()
        solution = {}
        print("Name: {self.name}")
        print("Existing schedule: {self.schedule}")
        print(f"Possible Rotations: {self.possibleRotations}\nOrder: {self.order}")
        if len(self.possibleRotations) > 0:
            problem.addVariables(self.possibleRotations, self.order)

            # HARD CONSTRAINT 1 - All rotations must be unique in the period of the program
            problem.addConstraint(AllDifferentConstraint(), self.possibleRotations)
            solutions = problem.getSolutions()

            # Score the options
            print(f"Scoring {len(solutions)} found")
            scores = np.zeros(len(solutions))
            for sidx, solution in enumerate(solutions):
                scores[sidx] = scoring_function(
                    assignments, sorted(solution.items(), key=lambda x: x[1])
                )

            chosen = np.argsort(scores)
            solution = solutions[chosen[0]]
            print(f"Best solution: {solution}")
        return solution

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
