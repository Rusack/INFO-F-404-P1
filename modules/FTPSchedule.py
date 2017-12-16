from modules.cpu import Event, EventType, Job
import matplotlib.pyplot as plt
import numpy as np

"""Represent a FTP scheduler"""
class FTPScheduler(object) :
    
    """ctor"""
    def __init__(self, tasks) :
        self.schedule = list()
        self.tasks = tasks

    """Simulate a FTP scheduler, and build a schedule from a set of tasks and an interval"""
    def build_schedule(self, start, end) :
        # List of all the jobs
        jobs = list()
        # A reference to the currentJob the cpu is executing
        currentJob = None
        # Indicates if CPU is idle
        idle = True
        # Last time cpu switch of job
        lastSwitch = 0
        self.start = start
        self.end = end
        schedule = list()
        jobsToRemove = []
        # Iterate throught time units
        for time in range(0, end + 1 ) :
            # Iterate through task to Check if a job must be released
            for task in self.tasks :
                if time >= task.offset and (time - task.offset) % task.period == 0 :
                    jobs.append(task.releaseJob(time))
                    self.addEventSchedule(EventType.JOB_ARRIVAL, time, time, task.priority, task.jobCounter)
            # Remove old jobs
            for j in jobsToRemove : jobs.remove(j)
            jobsToRemove = []
            # Iterate through job, checking deadline, priorities and execution
            for job in jobs :
                # Reach deadline
                if time == job.deadline :
                    self.addEventSchedule(EventType.JOB_DEADLINE, time, time, job.taskNumber, job.jobNumber)
                    # If job isn't finished
                    if not job.isFinished() :
                        self.addEventSchedule(EventType.JOB_MISS_DEADLINE, time, time, job.taskNumber, job.jobNumber)
                    else :
                        # Remove job if deadline is past and job is finished
                        jobsToRemove.append(job)
                        continue

                # ignore itself
                if currentJob == job :
                    continue

                # If processor has not current job, take first unfinished job 
                if  currentJob == None or idle and not job.isFinished() :
                    # Set to first job
                    currentJob = jobs[0]
                    # If no job left, continue
                    if currentJob == None : continue
                    lastSwitch = time
                    idle = False
                
                # Switch if :
                # 1. There's a job with higer priority and unfinished
                # 2. Actual job is finished and another job is not finished
                if (job.priority < currentJob.priority and not job.isFinished()) or\
                 currentJob.isFinished() and not job.isFinished() :
                        # If job has been executed (otherwise if job wasn't executed at all, no point of adding this event)
                        if lastSwitch != time : 
                            self.addEventSchedule(EventType.JOB_EXECUTION, lastSwitch, time, currentJob.taskNumber, currentJob.jobNumber)
                        currentJob = job
                        lastSwitch = time

            # If there are no other job to compute, CPU is idle
            if  not idle and currentJob.isFinished() :
                self.addEventSchedule(EventType.JOB_EXECUTION, lastSwitch, time, currentJob.taskNumber, currentJob.jobNumber)
                lastSwitch = time
                idle = True

            # If cpu is not idle, execute current job
            if not idle :
                currentJob.executeUnity()
            
            
        # If cpu wasn't idle at end
        # lastSwitch should be different to time otherwise no point of keeping event (no computations were made)
        if not idle and lastSwitch != time:
            self.addEventSchedule(EventType.JOB_EXECUTION, lastSwitch, time, currentJob.taskNumber, currentJob.jobNumber)
        
        # Cut the schedule to keep only the interval part
        self.sliceSchedule(start, end)

    """Cut the schedule, and keep the events between start and end value"""
    def sliceSchedule(self, start, end) :
        slicedSchedule = list()
        for event in self.schedule :
            # Event fully before start time or Event fully after end time
            # don't keep it
            if event.end < start or event.start > end :
                continue
            # Event partially in the interval 
            if (event.end >= start and event.start < start) :
                # Just keep part in the interval
                event.start = start
            # Idem
            if (event.end >= end and event.start < end) :
                event.end = end
                
            slicedSchedule.append(event)
        
        # Update schedule
        self.schedule = slicedSchedule
        self.sortScheduleEvent()

    """Add an event to the schedule"""
    def addEventSchedule(self, eventType, start, stop, taskNumber, jobNumber) :
        self.schedule.append(
            Event(eventType, start, stop, taskNumber, jobNumber)
        )
    
    """Print the last schedule built"""
    def printSchedule(self) :
        if len(self.schedule) == 0 :
            print("A schedulte has not been built yet")
        else :
            print("Schedule from: %d to: %d ; %d tasks" % (self.start, self.end, len(self.tasks)))
            for event in self.schedule :
                print(event)


    """Plot the last schedule built""" 
    def plotSchedule(self) :
        print("Plotting...")
        nbTasks = len(self.tasks)
        fig = plt.figure(figsize=((self.end - self.start)//10, nbTasks + 2))
        ax = fig.add_subplot(111)
        ax.grid()
        plt.title("FTP schedule from %d to %d with %d tasks" % (self.start, self.end, len(self.tasks)))
        # y axis
        plt.ylabel("Task Nb and priority")
        ylabels = ["T%d \n P %d " % (task.taskNumber, task.priority)  for task in self.tasks]
        # More major ticks than task to have ticks above and under for each task label
        plt.yticks(np.arange(0, nbTasks + 2))
        plt.ylim(0, nbTasks + 2)
        ax.tick_params(axis='y', direction='inout', length=20.,)
        ax.set_yticklabels('')
        # Minor ticks (labels are set to be at minor ticks between each major tick)
        ax.set_yticks(np.arange(1.5 , nbTasks + 1, 1), minor=True)
        ax.set_yticklabels(ylabels, minor = True)
        for tick in ax.yaxis.get_minor_ticks() :
            tick.tick1line.set_markersize(0)
        # x axis
        plt.xlabel("Time")
        # X tick size
        xtick = (self.end - self.start) // 2 
        # space between 0 and axis to not hide the arrows
        plt.xlim((self.start - 10, self.end + 10))
        ax.tick_params(axis='x', rotation=90)
        # Major tick on x
        # Draw lines
        lineX = 10

        plt.xticks(np.arange(self.start, self.end + 1 , lineX))
        for i in range(self.start, self.end + xtick, 1) :
            if i % lineX == 0 :
                plt.axvline(i, linestyle='dotted', linewidth=0.5, color='k')
            else :
                plt.axvline(i, linestyle='dotted', linewidth=0.1, color='k')
        
        # Draw events
        for event in self.schedule :
            if event.eventType == EventType.JOB_EXECUTION :
                # Draw a red rectangular with job name
                x = [event.start, event.end]
                y1 = np.array([event.taskNumber, event.taskNumber])
                y2 = y1 + 1 
                ax.fill_between(x, y1, y2=y2, color='red')
                ax.text(np.mean(x), np.mean([y1[0], y2[0]]) - 0.3, "J%d" % event.jobNumber, 
                                            horizontalalignment='center',
                                            verticalalignment='center',
                                            size="13",
                                            color='black')
            elif event.eventType == EventType.JOB_ARRIVAL :
                # Draw an arrow to signal job released
                ax.arrow(event.end, event.taskNumber - 0.5, 0, 0.5, width=0.1, head_width=1, head_length=0.1,
                   length_includes_head=True,
                   color='black')

            elif event.eventType == EventType.JOB_DEADLINE :
                # plot a circle at deadline
                y1 = np.array([event.taskNumber, event.taskNumber])
                y2 = y1 + 1
                y =  np.mean([y1[0], y2[0]])
                ax.plot(event.start, y, 'bo', color='black', fillstyle='none', markersize=5)
            elif event.eventType == EventType.JOB_MISS_DEADLINE :
                # draw a cross in case of deadline
                 # plot a circle at deadline
                y1 = np.array([event.taskNumber, event.taskNumber])
                y2 = y1 + 1
                y =  np.mean([y1[0], y2[0]])
                ax.plot(event.start, y + 0.2, 'x', color='black', fillstyle='none', markersize=5)
        
        # Invert Y axis to have task sorted by number
        plt.gca().invert_yaxis()
        # Save plot 
        print("Saving...")
        fig.savefig('plot.png', bbox_inches='tight', dpi=fig.dpi)
        print("Schedule has been saved into file plot.png")
        

    """Check if a deadline has been missed for the task,
     if precised check for the specific job"""
    def checkDeadlineMiss(self, taskNumber, jobNumber=-1) :
        for event in self.schedule :
            if event.eventType == EventType.JOB_MISS_DEADLINE :
                if event.taskNumber == taskNumber :
                    if jobNumber == -1 :
                        return True
                    elif event.taskNumber == jobNumber :
                        return 
        return False
    """Sort schedule event, to be more coherent with task utilization interval and job arrival"""
    def sortScheduleEvent(self) :
        self.schedule.sort(key=lambda x : x.start)