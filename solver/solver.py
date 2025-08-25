from datetime import datetime

from ortools.sat.python import cp_model
from testing_data.tasks import PeriodicTask, DynamicTask

import plotly.express as px
import pandas as pd

class Solver:
    def __init__(self):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def solve(self, periodic_tasks: [PeriodicTask], dynamic_tasks: [DynamicTask]):
        n = len(dynamic_tasks)
        t: DynamicTask
        start_times = []
        end_times = []
        intervals = []
        for t in dynamic_tasks:
            start = self.model.NewIntVar(t.release_time, t.deadline-t.estimated_duration, "START_"+t.name)
            end = self.model.NewIntVar(t.release_time + t.estimated_duration, t.deadline, "END_" + t.name)
            interval = self.model.NewIntervalVar(start, t.estimated_duration, end, "INTERVAL_" + t.name)
            start_times.append(start), end_times.append(end), intervals.append(interval)

        self.model.AddNoOverlap(intervals)

        status = self.solver.solve(self.model)


        """ Visualisation and results printing"""
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            starts = [self.solver.Value(start_times[i]) for i in range(n)]
            ends = [self.solver.Value(end_times[i]) for i in range(n)]
            print("Start times:")
            tasks = []
            for i in range(n):
                print(f'Task {i}: start = {starts[i]}, duration = {dynamic_tasks[i].estimated_duration}')
                tasks.append(dict(Task=dynamic_tasks[i].name, Type="Dynamic", Deadline=datetime.fromtimestamp(dynamic_tasks[i].deadline), Start=datetime.fromtimestamp(starts[i]), End=datetime.fromtimestamp(ends[i])))
            self.visualise(tasks)
            return True
        else:
            print("No solution found.")
            return False

    def visualise(self, tasks):
        df = pd.DataFrame(tasks)
        fig = px.timeline(df, x_start="Start", x_end="End", color="Task", title="Schedule", hover_data=["Deadline", "Type"])
        fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
        fig.show()



