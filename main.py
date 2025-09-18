from testing_data.tasks import TasksCreator, DynamicTask
from solver.solver import Solver
from solver.orknapsack import Knapsack
from solver.orilp import IlpKnapsack
from solver.orilp_adaptive_ordered import IlpKnapsackAdaptiveOrdered
from solver.orilp_adaptive import IlpKnapsackAdaptive
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from scipy.stats import norm


def quantile(dt: [DynamicTask], success_probability):
    for task in dt:
        task.estimated_duration = norm.ppf(success_probability, loc=task.mean, scale=task.std)

    return dt


if __name__ == '__main__':
    print("Hello! \n All times are in seconds!!!")
    tc = TasksCreator()

    status = True
    real_dur_sum = []
    obj_val_list = []
    run_time_list = []
    capacity = 1800
    exc = 0
    print("### LP ###")
    for i in range(1000):
        print(i)
        dynamic_tasks = tc.return_dynamic_tasks_v5(i+1)
        dynamic_tasks = quantile(dynamic_tasks, success_probability=0.95)
        sum_of_real_dur, obj_val, run_time =IlpKnapsackAdaptive(capacity=capacity).solve(dynamic_tasks)
        real_dur_sum.append(sum_of_real_dur)
        obj_val_list.append(obj_val)
        run_time_list.append(run_time)
        if sum_of_real_dur > capacity:
            exc += 1

    print(f"TOTAL TIME EXCEEDED: {sum([i-capacity for i in real_dur_sum if i > capacity])}s")
    print(f"TOTAL UNUSED TIME: {sum([capacity-i for i in obj_val_list if i < capacity])}s")
    print(f"INSTANCES EXCEEDED: {exc}/1000 ~ {100*exc/1000}%")

    """ VISUALISATION """
    data1 = np.array(real_dur_sum)
    data2 = np.array(obj_val_list)
    data3 = np.array(run_time_list)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # First histogram
    counts, bins, patches = axes[0].hist(data1, bins=60, color="skyblue", edgecolor="black")
    axes[0].set_title("Sum of real durations")
    # Color bins conditionally
    for patch, left_edge in zip(patches, bins[:-1]):
        if left_edge >= capacity:  # condition
            patch.set_facecolor("red")
        else:
            patch.set_facecolor("skyblue")

    # Second histogram
    axes[1].hist(data2, bins=60, color="lightgreen", edgecolor="black")
    axes[1].set_title(f"Objective function value from max capacity: {capacity}")

    # Third histogram
    axes[2].hist(data3, bins=60, color="salmon", edgecolor="black")
    axes[2].set_title("Run time [ms]")

    # Force full numbers on axes
    for ax in axes:
        formatter = ScalarFormatter(useOffset=False, useMathText=False)
        formatter.set_scientific(False)
        ax.xaxis.set_major_formatter(formatter)

    plt.xlabel("Value")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    """
    print("### CP ###")
    solver.solve(periodic_tasks, dynamic_tasks)

    print("#### KNAPSACK ###")
    knapsack = Knapsack().solve(dynamic_tasks)
    """




