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
        is_scheduled = []
        for t in dynamic_tasks:
            scheduled = self.model.NewBoolVar(f'is_scheduled_{t.name}')
            is_scheduled.append(scheduled)
            start = self.model.NewIntVar(t.release_time, t.deadline-t.estimated_duration, "START_"+t.name)
            end = self.model.NewIntVar(t.release_time + t.estimated_duration, t.deadline, "END_" + t.name)
            interval = self.model.NewOptionalIntervalVar(start, t.estimated_duration, end, scheduled, "INTERVAL_" + t.name)
            start_times.append(start), end_times.append(end), intervals.append(interval)

        self.model.AddNoOverlap(intervals)
        self.model.maximize(sum(dynamic_tasks[i].estimated_duration * is_scheduled[i] for i in range(len(dynamic_tasks))))

        status = self.solver.solve(self.model)


        """ Visualisation and results printing"""
        print("Solver time (s):", self.solver.WallTime())
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"Maximum of objective function: {self.solver.objective_value}\n")
            starts = [self.solver.Value(start_times[i]) for i in range(n)]
            ends = [self.solver.Value(end_times[i]) for i in range(n)]
            scheduled = [self.solver.Value(is_scheduled[i]) for i in range(n)]
            print("Start times:")
            tasks = []
            for i in range(n):
                if scheduled[i]:
                    print(f'Task {i}: start = {starts[i]}, duration = {dynamic_tasks[i].estimated_duration}')
                    tasks.append(dict(Real="no", Task=dynamic_tasks[i].name, Type="Dynamic", Deadline=datetime.fromtimestamp(dynamic_tasks[i].deadline), Start=datetime.fromtimestamp(starts[i]), End=datetime.fromtimestamp(ends[i]), Real_duration=dynamic_tasks[i].real_duration))
            tasks = sorted(tasks, key=lambda x: x["Start"])

            """REAL VISUALISATION"""

            start = 0
            r_task = []
            for i in tasks:
                r_task.append(dict(Real="yes", Task=i["Task"], Type="Dynamic", Deadline=i["Deadline"], Start=datetime.fromtimestamp(start), End=datetime.fromtimestamp(start+i["Real_duration"]), Real_duration=i["Real_duration"]))
                start += i["Real_duration"]
            self.visualise(tasks + r_task)
            return True
        else:
            print("No solution found.")
            return False

    def visualise(self, tasks):
        df = pd.DataFrame(tasks)
        fig = px.timeline(df, y="Real", x_start="Start", x_end="End", color="Task", title="Schedule", hover_data=["Deadline", "Type", "Real_duration"])
        fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
        fig.show()




