from modules.cpu import Task
import numpy as np

"""Class containing methods to generate a task set"""
class TaskGenerator(object) :

    """Compute total utilization factor for two arrays of wcet and period"""
    def utilizationFactorArray(self, wcetArray, periodArray) :
        U = 0
        for c, p in zip(wcetArray, periodArray) :
            U += self.utilizationFactor(c, p)
        return U

    """Compute utilization factor for a wcet and period"""
    def utilizationFactor(self, wcet, period) :
        return wcet/period

    """Generate a set of task with a specific cpu utilization, number of task,
    and bounds for time, task parameters will be generated between these bounds"""
    def generateTaskSet(self, utilization, nbTasks, lowBound, upBound ) :
        if lowBound <= 0 :
            print("Lower bound should at least be 1")
            exit(1)
        offset = [0] * nbTasks
        deadline = [0] * nbTasks
        wcet = [0] * nbTasks
        tasks = list()
        # Indicate if a set of task has beenn found
        found = False
        # numbero of iterations before giving up searching
        limit = 1000
        # Count number of try
        iteration = 0
        print("Generating...")
        # Keep searching while not found
        while not found or iteration == limit:
            iteration += 1
            # Generate period and wcet
            periods = np.random.randint(lowBound,upBound, nbTasks)
            for i in range(0,10000) :
                for j in range(0, nbTasks) :
                    # +1 Cause interval isn't open on upper bound : [low, high)
                    wcet[j] = np.random.randint(1, periods[j] + 1) 
                U = self.utilizationFactorArray(wcet, periods)
                # 0.001 is the threshold to decide if utilization is close enough to target
                if U > utilization-0.001 and U < utilization+0.001 :
                    print("Found %f" % U)
                    found = True
                    break 
        
        # Generate offset and deadline
        for i,w,p in zip(range(0,nbTasks), wcet, periods) :
            offset[i] = np.random.randint(0, upBound + 1)
             # Deadline should be between wcet and period
            deadline[i] = np.random.randint(wcet[i], periods[i] + 1)
            t = Task(i + 1, offset[i], periods[i], deadline[i], wcet[i],0)
            tasks.append(t)
        if len(tasks) == 0 :
            print("Unable to generate tasks set, review the parameters or try again")
        else :
            for task in tasks :
                print(task)
        return tasks
