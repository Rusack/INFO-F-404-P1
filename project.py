import argparse
import sys
import modules.utilities as utilities
from modules.cpu import Task, Job
from modules.FTPSchedule import FTPScheduler
from modules.audsley import Audsley
from modules.taskGenerator import TaskGenerator
from modules.interval import FeasibilityInterval

"""Main class of the project, will route the programm execution"""
class Project(object) :

    """ctor, will define arg parser and command possible
    then dispatch the command to corresponding action"""
    def __init__(self):
        # Build argument parser
        ap = argparse.ArgumentParser()
        ap.add_argument("command",
        choices=["interval", "sim", "audsley", "gen", "plot", "testAll"],
        help='Subcommand to run' )
        # Get the command to execute
        args = ap.parse_args(sys.argv[1:2])
        print(args.command)
        # Check if command exists
        if not hasattr(self, args.command):
            print('Unrecognized command')
            ap.print_help()
            exit(1)
        # Otherwise call corresponding command
        getattr(self, args.command)()

    """Compute feasability interval for a given system"""
    def interval(self) :
        parser = argparse.ArgumentParser(
            description='Compute feasability interval')
        parser.add_argument("taskFile", type=str)
        # argv[2:] ignore first two arguments (aka script name and command)
        args = parser.parse_args(sys.argv[2:])
        tasks = utilities.parseTaskFile(args.taskFile)
        feasibilityInterval = FeasibilityInterval()
        interval = feasibilityInterval.computeFeasibilityInterval(tasks)
        print("Feasibility interval is %d,%d" % interval)
    
    """Simulate the system given during an interval and print a text description of the events"""
    def sim(self) :
        parser = argparse.ArgumentParser(
            description='Simulate a single processor FTP for a given period',
            usage="%s sim start stop taskFile" % sys.argv[0])
        # interval
        parser.add_argument("start", type=utilities.check_positive)
        parser.add_argument("stop", type=utilities.check_positive)
        # task file (system)
        parser.add_argument("taskFile", type=str)
        # argv[2:] ignore first two arguments (aka script name and command)
        args = parser.parse_args(sys.argv[2:])
        tasks = utilities.parseTaskFile(args.taskFile)

        scheduler = FTPScheduler(tasks)
        scheduler.build_schedule(args.start, args.stop)
        scheduler.printSchedule()

    """Apply audsley algorithm to try to find a FTP priorities assignment for a given
    system and interval"""
    def audsley(self) :
        parser = argparse.ArgumentParser(
            description='Compute each possible priority assignment found by Audsley algorithm',
            usage="%s audsley start stop taskFile" % sys.argv[0])
        # interval
        parser.add_argument("start", type=utilities.check_positive)
        parser.add_argument("stop", type=utilities.check_positive)
        # task file (system)
        parser.add_argument("taskFile", type=str)
        args = parser.parse_args(sys.argv[2:])
        tasks = utilities.parseTaskFile(args.taskFile)
        audsley = Audsley()
        audsley.priorityAssignment(tasks, args.start,args.stop)
    
    """Generate a file with a random system, given some parameters"""
    def gen(self) :
        parser = argparse.ArgumentParser(
            description='Generate random periodic, asynchronous system with constrained deadlines',
            usage="%s gen nbTasks utilizationFactor lowerBound upperBound taskFile" % sys.argv[0])
        parser.add_argument("nbTasks", type=utilities.check_positive,)
        parser.add_argument("utilizationFactor", type=float)
        parser.add_argument("lowerBound", type=utilities.check_positive)
        parser.add_argument("upperBound", type=utilities.check_positive)
        # task file name (system)
        parser.add_argument("taskFile", type=str)
        args = parser.parse_args(sys.argv[2:])
        generator = TaskGenerator()
        tasks = generator.generateTaskSet(args.utilizationFactor, args.nbTasks , args.lowerBound, args.upperBound)
        utilities.writeTasksToFile(tasks, args.taskFile)
  

    """Plot the schedule for the system and interval"""
    def plot(self) :
        parser = argparse.ArgumentParser(
            description='Simulate a single processor FTP for a given period and then plot the result',
            usage="%s plot start stop taskFile" % sys.argv[0])
        # interval
        parser.add_argument("start", type=utilities.check_positive)
        parser.add_argument("stop", type=utilities.check_positive)
        # task file (system)
        parser.add_argument("taskFile", type=str)
        # argv[2:] ignore first two arguments (aka script name and command)
        args = parser.parse_args(sys.argv[2:])
        tasks = utilities.parseTaskFile(args.taskFile)

        scheduler = FTPScheduler(tasks)
        scheduler.build_schedule(args.start, args.stop)
        scheduler.plotSchedule()

    """Test all the functionalities using hardcoded values"""
    def testAll(self) :
        tasks = utilities.parseTaskFile("audsley.txt")
        print("----Feasibility Interval----")
        feasibilityInterval = FeasibilityInterval()
        interval = feasibilityInterval.computeFeasibilityInterval(tasks)
        print("Feasability interval is %d,%d" % interval)
        print("----Simulator----")
        scheduler = FTPScheduler(tasks)
        scheduler.build_schedule(0, 200)
        scheduler.printSchedule()
        print("----Plot---")
        scheduler.plotSchedule()
        print("----Audlsey algorithm----")
        audsley = Audsley()
        audsley.priorityAssignment(tasks, 0,200)
        print("----Task Generation----")
        generator = TaskGenerator()
        tasks = generator.generateTaskSet(0.99, 5 , 1, 200)
        utilities.writeTasksToFile(tasks, "t.txt")

""" Entry point """
if __name__ == "__main__" :
    Project()