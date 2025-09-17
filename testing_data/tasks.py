import numpy as np


# ALL TIMES are in seconds ... "from" & "to" are in seconds from start - 0

class TasksCreator:
    def return_periodic_tasks(self):
        return [
            PeriodicTask("P1-30s-30m", 0, 4*60*60, 30, 30*60),
            PeriodicTask("P2-5m-20m", 15*60, 7*60*60, 5*60, 20*60),
        ]
    def return_dynamic_tasks_v1(self):
        return [
            DynamicTask("D01-35s", 60, 1 * 60 * 60, 20, 35),
            DynamicTask("D02-35s", 60, 1 * 60 * 60, 20, 35),
            DynamicTask("D03-35s", 60, 1 * 60 * 60, 20, 35),
            DynamicTask("D04-120s", 60, 1 * 60 * 60, 2 * 60, 2 * 60),
            DynamicTask("D05-240s", 60, 1 * 60 * 60, 5 * 60, 4 * 60),
            DynamicTask("D06-480s", 60, 1 * 60 * 60, 6 * 60, 8 * 60),
            DynamicTask("D07-420s", 60, 1 * 60 * 60, 7 * 60, 7 * 60),
            DynamicTask("D08-15s", 0, 1 * 60 * 60, 20, 15),
            DynamicTask("D09-35s", 0, 2 * 60, 25, 35),
            DynamicTask("D10-55s", 0, 12 * 60, 60, 55),
            DynamicTask("D11-35s", 60, 2 * 60 * 60, 20, 35),
            DynamicTask("D12-45s", 60, 2 * 60 * 60, 40, 45),
        ]

    def return_dynamic_tasks_v2(self):
        return [
            DynamicTask(f"Task_{x}", 0, 30*60, 13*x+111, 13*x+111) for x in range(100)
        ]

    def return_dynamic_tasks_v3(self, seed = 10):
        n = 150
        np.random.seed(seed)
        mean = 240 #s
        std = 20
        durations = np.random.normal(mean, std, n).round().astype(int)
        return [
            DynamicTask(f"Task_{x}", 0, 30 * 60, mean, durations[x]) for x in range(n)
        ]

    def return_dynamic_tasks_v4(self, seed = 10):
        np.random.seed(seed)
        durations1 = np.random.normal(31, 20, np.random.randint(0,20)).round().astype(int)
        durations2 = np.random.normal(330, 30, np.random.randint(0,20)).round().astype(int)
        durations3 = np.random.normal(1250, 50, np.random.randint(0,40)).round().astype(int)
        durations4 = np.random.normal(573, 10, np.random.randint(0,50)).round().astype(int)
        tasks1 = [DynamicTask(f"Task_31_{i}", 0, 30 * 60, 31, durations1[i], mean=31, std=20) for i in range(len(durations1))]
        tasks2 = [DynamicTask(f"Task_330_{i}", 0, 30 * 60, 330, durations2[i], mean=330, std=30) for i in range(len(durations2))]
        tasks3 = [DynamicTask(f"Task_1250_{i}", 0, 30 * 60, 1250, durations3[i], mean=1250, std=50) for i in range(len(durations3))]
        tasks4 = [DynamicTask(f"Task_573_{i}", 0, 30 * 60, 573, durations4[i], mean=573, std=10) for i in range(len(durations4))]
        return tasks1 + tasks2 + tasks3 + tasks4

class PeriodicTask:
    def __init__(self, name: str, start: int, end: int, duration: int, period: int):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.period = period

    def __str__(self):
        return f"{self.name}\tstart: {self.start}\tend: {self.end}\tduration: {self.duration}\tperiod: {self.period}"


class DynamicTask:
    def __init__(self, name: str, release_time: int, deadline: int, estimated_duration: int, real_duration: int, mean=None, std=None):
        self.name = name
        self.release_time = release_time
        self.deadline = deadline
        self.estimated_duration = estimated_duration
        self.real_duration = real_duration
        self.mean = mean
        self.std = std


    def __str__(self):
        return f"{self.name}\trelese: {self.release_time}\tdeadline: {self.deadline}\test. duration: {self.estimated_duration}\t real duration: {self.real_duration}"

