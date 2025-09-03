from ortools.linear_solver import pywraplp

from testing_data.tasks import DynamicTask


class IlpKnapsack:

    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver("SCIP")

    def solve(self, dynamic_tasks: [DynamicTask]):
        capacity = 30*60
        n = len(dynamic_tasks)
        weights = [dynamic_tasks[i].estimated_duration for i in range(n)]

        x = [self.solver.BoolVar(f"x_{i}") for i in range(n)]

        self.solver.Add(self.solver.Sum(weights[i] * x[i] for i in range(n)) <= capacity)

        self.solver.Maximize(self.solver.Sum(weights[i] * x[i] for i in range(n)))

        # Solve
        self.solver.Solve()

        # Extract solution
        #print([x[i].solution_value() for i in range(n)])
        picked = [i for i in range(n) if x[i].solution_value() == 1]
        total_weight = sum(weights[i] for i in picked)

        # Stats
        wall_time_ms = self.solver.wall_time()

        print("\nobjective_value: " + str(total_weight) +
            "\npicked_tasks: "+ str(picked) +
            "\nwall_time_(s): "+ str(wall_time_ms/1000))


