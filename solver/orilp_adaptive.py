from ortools.linear_solver import pywraplp
from testing_data.tasks import DynamicTask


class IlpKnapsackAdaptive:

    def __init__(self, capacity):
        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        self.capacity = capacity

    def inner_solve(self, dynamic_tasks: [DynamicTask], free_capacity):
        n = len(dynamic_tasks)
        weights = [dynamic_tasks[i].estimated_duration for i in range(n)]

        x = [self.solver.BoolVar(f"x_{i}") for i in range(n)]
        self.solver.Add(self.solver.Sum(weights[i] * x[i] for i in range(n)) <= free_capacity)
        self.solver.Maximize(self.solver.Sum(weights[i] * x[i] for i in range(n)))
        status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            picked = [i for i in range(n) if x[i].solution_value() == 1]
            return self.solver.wall_time(), picked
        else:
            return self.solver.wall_time(), None

    def solve(self, dynamic_tasks: [DynamicTask]):
        #print(f"Capacity: {self.capacity}")
        free_capacity = self.capacity
        sum_of_rdur = 0
        total_time = 0
        selected_tasks = []
        while free_capacity > 0:
            print(free_capacity)
            for i in selected_tasks: print(i)
            wall_time_ms, picked = self.inner_solve(dynamic_tasks, free_capacity)
            total_time += wall_time_ms
            if picked is None or picked == []:
                break
            rd = dynamic_tasks[picked[0]].real_duration
            sum_of_rdur += rd
            free_capacity -= rd
            selected_tasks.append(dynamic_tasks[picked[0]])
            del dynamic_tasks[picked[0]]

        return sum_of_rdur, self.capacity-free_capacity, total_time


