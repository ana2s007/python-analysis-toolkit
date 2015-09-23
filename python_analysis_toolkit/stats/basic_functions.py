import operator
from collections import Counter

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
