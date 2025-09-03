from ortools.algorithms.python import knapsack_solver
import time
from testing_data.tasks import DynamicTask, PeriodicTask
class Knapsack:
    def __init__(self):
        self.solver = knapsack_solver.KnapsackSolver(knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,"Knapsack",)

    def solve(self, dynamic_tasks: [DynamicTask]):
        capacities = [30*60]
        values = []
        weights = []

        for t in dynamic_tasks:
            values.append(t.estimated_duration)
            weights.append(t.estimated_duration)

        weights = [weights]

        ss=time.time()
        self.solver.init(values, weights, capacities)
        computed_value = self.solver.solve()
        wall_time = time.time() - ss
        packed_items = []
        packed_weights = []
        total_weight = 0
        print("Solver time (s):", wall_time)
        print("Total value =", computed_value)
        for i in range(len(values)):
            if self.solver.best_solution_contains(i):
                packed_items.append(i)
                packed_weights.append(weights[0][i])
                total_weight += weights[0][i]
        print("Total weight:", total_weight)
        print("Packed items:", packed_items)
        print("Packed_weights:", packed_weights)

