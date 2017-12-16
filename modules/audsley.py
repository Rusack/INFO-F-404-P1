from modules.FTPSchedule import FTPScheduler

"""Class to use audsley algorithm """
class Audsley(object) :
    """ctor"""
    def __init__(self) :
        pass

    """Determine if the specific task is lowest-priority viable 
    for an interval in the task system of Audsley object"""
    def lowestPriorityViable(self, tasks, start, stop, taskNumber) :
        new_taskSet = self.setTaskToLowestPriority(tasks, taskNumber)
        scheduler = FTPScheduler(new_taskSet)
        scheduler.build_schedule(start, stop)
        if scheduler.checkDeadlineMiss(taskNumber) :
            return False
        else : 
            return True

    """Try to find a FTP priority assignment, using audsley algorithm"""
    def priorityAssignment(self, tasks, start, stop, level=0 ) :
        schedulabe = False

        # Stop recursion
        if len(tasks) == 0 :
            print(level * " " + "A feasible FTP priorities assignment exists".rjust(level))
            return True      

        for task in tasks :
            # Simulate a schedule to know if task is lowest-priority viable
            new_taskSet = self.setTaskToLowestPriority(tasks, task.taskNumber)
            scheduler = FTPScheduler(new_taskSet)
            scheduler.build_schedule(start, stop)
            # If not lowest-priority viable
            if scheduler.checkDeadlineMiss(task.taskNumber) :
                print(level * " " + "Task %d is not lowest-priority viable" % (task.taskNumber))
                # If the last task is not lowest-priority viable
                if len(tasks) == 1 :
                    # Stop Recursion
                    print(level * " " + "Infeasible")
                    return False                    
            # If lowest-priority viable
            else :
                print(level * " " + "Task %d is lowest-priority viable" % (task.taskNumber))
                # Build a new task set without current task
                for t in  new_taskSet :
                    if t.taskNumber == task.taskNumber :
                        new_taskSet.remove(t)
                        break
                schedulabe = self.priorityAssignment(
                    sorted(new_taskSet,key = lambda task : task.taskNumber),
                     start, stop, level + 1)
        # If no priority assignment was found
        if not schedulabe :
            print(level * " " + "Infeasible")
        return schedulabe

    """Change priority of a task in a given task set to the lowest priority"""
    def setTaskToLowestPriority(self, tasks, taskNumber) :
        new_tasks = list()
        # Find task and change its priority
        prioritySorted = list(sorted(tasks, key = lambda task : task.priority, reverse=True))
        lowestPriority = prioritySorted[0].priority
        # offset to add to other task priorities to keep their priority higher
        o = 0
        for task in prioritySorted:
            if task.taskNumber == taskNumber :
                task.priority = lowestPriority
                new_tasks.append(task)
                continue
            elif task.priority >= lowestPriority or lowestPriority - o == task.priority:
                o += 1
                task.priority = lowestPriority - o
                new_tasks.append(task)
            else :
                new_tasks.append(task)
        return new_tasks
