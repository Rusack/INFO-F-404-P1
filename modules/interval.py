import functools

"""Class with methods to compute a feasibility interval for a set of tasks"""
class FeasibilityInterval(object) :

    """Return greatest common divisor using Euclid's Algorithm."""
    def gcd(self, a, b):
        while b:      
            a, b = b, a % b
        return a

    """Compute lowest common multiplier for two numbers"""
    def lcm(self, a, b):
        return a * b // self.gcd(a, b)

    """Compute lowest common multiplier for multiple numbers"""
    def lcmm(self, args):
        return functools.reduce(self.lcm, args)

    """Compute feasibility interval of a set of tasks"""
    def computeFeasibilityInterval(self, tasks) : 
        # Find P which is the lcm of the tasks periods
            P = self.lcmm([t.period for t in tasks])
            # Find Omax which is the maximum release time of the tasks
            Omax = max([t.offset for t in tasks])
            # interval is between Omax and Omax + 2*P
            return (Omax, Omax + 2*P)
