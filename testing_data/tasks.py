
# ALL TIMES are in seconds ... "from" & "to" are in seconds from start - 0

class TasksCreator:
    def return_periodic_tasks(self):
        return [
            PeriodicTask("P1-30s-30m", 0, 4*60*60, 30, 30*60),
            PeriodicTask("P2-5m-20m", 15*60, 7*60*60, 5*60, 20*60),
        ]
    def return_dynamic_tasks(self):
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
    def __init__(self, name: str, release_time: int, deadline: int, estimated_duration: int, real_duration: int):
        self.name = name
        self.release_time = release_time
        self.deadline = deadline
        self.estimated_duration = estimated_duration
        self.real_duration = real_duration

    def __str__(self):
        return f"{self.name}\trelese: {self.release_time}\tdeadline: {self.deadline}\test. duration: {self.estimated_duration}\treal duration: {self.real_duration}"

