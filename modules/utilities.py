import argparse
from modules.cpu import Task

"""Parse a given a task file, and return a list of tasks object, using task order in file as priority"""
def parseTaskFile(file) :  
        # Build a list with each task (represented by dict)
        tasks = list()
        try :
            with open(file, 'r') as f :
                p = 1
                for line in f :
                    # Split each line 
                    tokens = line.split(' ')
                    # Add the task to the list
                    tasks.append(Task(
                        p,
                        offset = int(tokens[0]),
                        period = int(tokens[1]),
                        deadline = int(tokens[2]),
                        wcet = int(tokens[3]),
                        # By default priority is task order in file
                        priority = p
                    ))
                    p += 1   
        except IOError :
            print("Error : Unable to find or open file %s" % (file))
            exit(1)
        # Return task list
        return tasks

"""Write tasks into a text file with format :
    Offset Period Deadline WCET
"""
def writeTasksToFile(tasks, file) :
    try :
            with open(file, 'w') as f :
                for task in tasks :
                    f.write("%d %d %d %d\n" % (task.offset, task.period, task.deadline, task.wcet))
    except IOError :
            print("Error : Unable to find or open file %s" % (file))
            exit(1)


"""Verify if a number is positive (used for argument parsing and verification)"""
def check_positive(value) :
    ivalue = int(value)
    if ivalue <0 :
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue



