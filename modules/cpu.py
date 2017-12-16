from enum import Enum

"""Set of classes to represent schedulin necessary components"""

"""Describe a task"""
class Task(object) :
    """ctor"""
    def __init__(self, taskNumber, offset, period, deadline, wcet, priority):
        self.taskNumber = taskNumber
        self.offset = offset
        self.period = period
        self.deadline = deadline
        self.wcet = wcet
        self.priority = priority
        # self.jobs = list()
        self.jobCounter = 0

    """Release a new job"""
    def releaseJob(self, releaseTime) :
        self.jobCounter += 1
        return Job(self.taskNumber,
            self.jobCounter,
            self.priority,
            releaseTime,
             self.wcet,
              releaseTime + self.deadline)
    """String representation of a task"""
    def __str__(self) :
        return ("Task %d"
        "   Priority  : %d"
        "   WCET : %d"
        "   Offset : %d"
        "   Period : %d"
        "   Deadline : %d" )% (self.taskNumber, self.priority, self.wcet, self.offset, self.period, self.deadline)

"""Describe a Job"""
class Job(object):
    """ctor"""
    def __init__(self, taskNumber, jobNumber, priority, releaseTime, et, deadline) :
        self.taskNumber = taskNumber
        self.priority = priority
        self.jobNumber = jobNumber
        self.releaseTime = releaseTime
        # Execution time
        self.et = et
        self.deadline = deadline

    """Execute a computational unit"""
    def executeUnity(self) :
        # reduce remaining execution time of one
        self.et -= 1
    """Return true if there's no computation unit left to the job"""
    def isFinished(self) :
        return self.et == 0

    """Definition of == operator for Job, equal if task nr and job nr are equal"""
    def __eq__(self, other) :
        if other == None :
            return False
        else :
            return self.taskNumber == other.taskNumber and self.jobNumber == other.jobNumber

"""Enumeration describing each event type and the string representation associated"""
class EventType(Enum) :
    JOB_ARRIVAL = "%d : Arrival of job T%dJ%d"
    JOB_EXECUTION = "%d-%d : T%dJ%d"
    JOB_DEADLINE = "%d : Deadline of job T%dJ%d"
    JOB_MISS_DEADLINE = "%d : Job T%dJ%d misses a deadline"

"""Event, single unity of schedule, describe an event"""
class Event(object) :
    """ctor"""
    def __init__(self, eventType, start, end, taskNumber, jobNumber) :
        self.eventType = eventType
        self.start = start
        self.end = end
        self.taskNumber = taskNumber
        self.jobNumber = jobNumber

    """String representation of the event"""
    def __str__(self) :
        if self.eventType == EventType.JOB_EXECUTION :
            return self.eventType.value % (self.start, self.end, self.taskNumber, self.jobNumber)
        else :
            return self.eventType.value % (self.start, self.taskNumber, self.jobNumber)
