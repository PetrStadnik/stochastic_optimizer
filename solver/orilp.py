from ortools.linear_solver import pywraplp

from testing_data.tasks import DynamicTask


class IlpKnapsack:

    def __init__(self, capacity):
        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        self.capacity = capacity

    def solve(self, dynamic_tasks: [DynamicTask]):
        print(f"Capacity: {self.capacity}")
        n = len(dynamic_tasks)
        weights = [dynamic_tasks[i].estimated_duration for i in range(n)]

        x = [self.solver.BoolVar(f"x_{i}") for i in range(n)]

        self.solver.Add(self.solver.Sum(weights[i] * x[i] for i in range(n)) <= self.capacity)

        self.solver.Maximize(self.solver.Sum(weights[i] * x[i] for i in range(n)))

        # Solve
        self.solver.Solve()

        # Extract solution
        #print([x[i].solution_value() for i in range(n)])
        picked = [i for i in range(n) if x[i].solution_value() == 1]
        list_of_tasks = [dynamic_tasks[t] for t in picked]
        sum_of_rdur = sum([t.real_duration for t in list_of_tasks])

        for t in list_of_tasks: print(t)
        total_weight = sum(weights[i] for i in picked)

        # Stats
        wall_time_ms = self.solver.wall_time()

        print("\nobjective_value: " + str(total_weight) +
            "\npicked_tasks: "+ str(picked) +
            "\nwall_time_(s): "+ str(wall_time_ms/1000))
        print(f"Sum of real_durations: {sum_of_rdur}")

        return sum_of_rdur, total_weight, wall_time_ms


