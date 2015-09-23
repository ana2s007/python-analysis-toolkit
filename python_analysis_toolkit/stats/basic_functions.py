import operator
from collections import Counter
import numpy
from math import sqrt   

def list_to_frequency_tuples(l):
    """
        Takes a list of items and constructs a frequency dictionary of the counts
        
        Args:
           l : list of items (strings, ints, etc)
           
        Returns:
           list of tuples, where each tuple is the form (x,y,z) where x=the item, y= the count of the item in l, and z=the percentage of items in l that are x
    """
    return_tups = []
    c = Counter(l)
    N = len(l)      
    for key, value in sorted(c.items(), key=operator.itemgetter(1), reverse=True):
        return_tups.append((key, value, 100*value/N))
    return return_tups

def mean(l):
    return numpy.mean(l)

def ci95(l):
    """
        Returns the 95% Gaussian confidence interval (caller should use the + and - of this value) of an array of vals
        http://en.wikipedia.org/wiki/Confidence_interval
    """
    return 1.96*numpy.std(l)/sqrt(len(l)) 