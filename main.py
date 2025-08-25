from testing_data.tasks import TasksCreator
from solver.solver import Solver

HORIZONT = 2*60*60 # 2h

if __name__ == '__main__':
    print("Hello! \n All times are in seconds!!!")
    tc = TasksCreator()
    periodic_tasks = tc.return_periodic_tasks()
    dynamic_tasks = tc.return_dynamic_tasks()
    print("Periodic tasks:")
    for i in periodic_tasks: print(i)
    print("Dynamic tasks:")
    for i in dynamic_tasks: print(i)

    solver = Solver()
    iteration = 0
    status = True
    while status:
        status = solver.solve(periodic_tasks, dynamic_tasks)
        iteration +=1
        input(f"Press Enter to continue with next iteration, actual: {iteration}")
