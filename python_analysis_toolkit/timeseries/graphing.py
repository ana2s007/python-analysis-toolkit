import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, HourLocator, MinuteLocator, SecondLocator, DateFormatter
import pandas
import operator
import matplotlib.gridspec as gridspec

from python_analysis_toolkit.conversion import datetimes
from pandas.tseries.offsets import *

"""
Internal Helper Functions
"""

def _timeseries_frequency_helper(major_granularity, minor_granularity):
    """Internal helper function to convert human readable labels into matplotlib and pandas parameters
        
       Args:
           major_granularity (str) : years, months, days, hours, or minutes
           minor_granularity (str) : months, days, hours, minutes, seconds
           
        Returns:
           matplotlib.MajorLocator,
           matplotlib.MajorFormatter
           matplotlib.MajorLocator,
           matplotlib.MajorFormatter           
           pandas.frequency
    """
    
    #set the locatiors
    if major_granularity == "years":
        major_loc = YearLocator()
        major_fmt = DateFormatter('%y')
    elif major_granularity == "months":
        major_loc = MonthLocator()
        major_fmt = DateFormatter('%y%m')
    elif major_granularity == "days":
        major_loc = DayLocator()
        major_fmt = DateFormatter('%y%m%d')
    elif major_granularity == "hours":
        major_loc = HourLocator()
        major_fmt = DateFormatter('%y%m%d %H')
    elif major_granularity == "minutes":
        major_fmt = DateFormatter('%y%m%d %H-%M')
        major_loc = MinuteLocator()
    else: #no seconds for major
        raise Exception("Unsupported Major Frequency: {0}".format(major_granularity))        
    #see http://pandas.pydata.org/pandas-docs/stable/timeseries.html under "Offset Aliases"
    if minor_granularity == "months":
        minor_loc = MonthLocator()
        minor_fmt = DateFormatter('%m')
        pandas_freq = 'M'
    elif minor_granularity == "days":
        minor_loc = DayLocator() 
        minor_fmt = DateFormatter('%d')
        pandas_freq = 'D'             
    elif minor_granularity == "hours":
        minor_loc = HourLocator()
        minor_fmt = DateFormatter('%H')
        pandas_freq = 'H'
    elif minor_granularity == "minutes":
        minor_loc = MinuteLocator()
        minor_fmt = DateFormatter('%M')
        pandas_freq = 'T' #.. yes
    elif minor_granularity == "seconds":
        minor_loc = SecondLocator()
        minor_fmt = DateFormatter('%S')
        pandas_freq = 'S'   
    else: #no years for minor
        raise Exception("Unsupported Minor Frequency")      
    
    minor_fmt = DateFormatter('')
    major_loc.MAXTICKS = 100
    minor_loc.MAXTICKS = 10000

    return major_loc, major_fmt, minor_loc, minor_fmt, pandas_freq  


def _finalize_helper(gs, save_instead_plot, fname, fig):
    #produce final fiture    
    gs.tight_layout(fig) 
    if  save_instead_plot:
        plt.savefig(fname + ".pdf", format = "pdf")
    else:
        plt.show() 

def _xaxis_format(ax, major_loc, major_fmt, major_gran,  minor_loc, minor_fmt, minor_gran, gs_index, title, ylab):
    ax.xaxis.set_major_formatter(major_fmt)
    ax.xaxis.set_minor_formatter(minor_fmt)
    ax.xaxis.set_major_locator(major_loc)
    ax.xaxis.set_minor_locator(minor_loc) 
    for tick in ax.get_xticklabels():
        tick.set_rotation(90) #rotate the labels. I don't like how fig.autofmt_xdate() works; sometimes it cuts off the top graph labels
    ax.set_xlabel("Dates at granularity: {0}, {1}".format(major_gran, minor_gran))        
    ax.grid(True) #vlines at major locator
    plt.legend(fontsize=6, loc='best')        
    if gs_index == 0: #put the title and legend on first plot only
        plt.title(title)
    ax.set_ylabel(ylab)
    
    

_colors = ['r', 'b', 'g', 'k', 'm']    



"""
Public Functions
"""
                        
def plot_event_frequency(ts_dict, 
                         major_granularity, 
                         minor_granularity, 
                         start_date = None,
                         end_date = None,
                         title = "Placeholder Title",
                         save_instead_plot = False, 
                         fname = "foo.png",
                         event_name = "Events"):
    """
        Purpose: plot the number of events for a number of keys occuring in some time window, e.g., per day, over some time range. 
                 can be used to plot a timeseries of multiple keys on the same graph, e.g., events per household (key = household id)
        
        Mandatory Args:
             ts_dict: dictionary where the keys are the keys (String) to plot a timeseries for and 
                      the value for each key is (a list of DateTimes) at which the events occured
             major_granularities (list of strings): elements can be years, months, days, hours, or minutes
             minor_granularities (list of strings): elements can be months, days, hours, minutes, seconds
                               
                      *there will be one tickmark on the x axis for every major-minor. 
                      For example, if major is years and minor is months, there will be a tick for every month in the timerange. 
                      IMPORTANT: minor_granularity defines the "granularity" of this function. E.g., if it is hours, then all events that happen in 
                          [Y-M-D H:*] are bucketed into the bucket [Y-M-D H:*]       
                      
                      These are lists because this function will show a stacked plot if you want to see multiple granularities at once                     

        Optional Args:
             title (string): goes into the matplotlib plot
             save_instead_plot (boolean): save the plot to a file instead of calling plot.show(). Defaults to False
             fname (string): filename to save the plot to via save_instead_plot. Defaults to "foo.png". Does nothing if not save_instead_plot
             start_date (Datetime Object): if a datetime, all data prior to this date is cut off prior to graphing
             end_date (Datetime Object): if a datetime, all data after this date is cut off prior to graphing
             event_name (string): text tht gos on y-label
        Returns:
             None, but writes to disk if save_instead_plot is True
             
    """             
    fig = plt.figure()#setup the main graph
    total_plots = len(start_date)
    gs =  gridspec.GridSpec(total_plots, 1)
    gs.update(wspace=0, hspace=0.05) # set the spacing between axes. 
    
 
    for dindex, date in enumerate(start_date): #make sure to sort or else the different lines will be different colors on different plots!! 
        major_loc, major_fmt, minor_loc, minor_fmt, pandas_freq  = _timeseries_frequency_helper(major_granularity, minor_granularity)
         
        ax = plt.subplot(gs[dindex, 0])
        
        plot_dict = {}
        
        for kindex, k in enumerate(ts_dict.keys()):
            if not len(ts_dict[k]) > 0:
                print("No data for key {0}".format(k))
            else:
                this_ts = [i for i in ts_dict[k] if i >= start_date[dindex] and i <= end_date[dindex]]
                ts = pandas.Series([1 for i in this_ts], index=this_ts).resample(pandas_freq, how='count')
                ax.plot_date([d.to_datetime() for d,s in ts.iteritems()], [s for s in ts],  'o', label=k, color=_colors[kindex % 5])

        _xaxis_format(ax, major_loc, major_fmt, major_granularity, minor_loc, minor_fmt, minor_granularity,  dindex, title, "Number of {0}".format(event_name)) # format the ticks and the plotc        
            
    _finalize_helper(gs, save_instead_plot, fname, fig)  
        


def state_diagram(         ts_dict, 
                           major_granularity, 
                           minor_granularity, 
                           start_date = None,
                           end_date = None,
                           title = "Placeholder Title",
                           save_instead_plot = False,
                           print_annotated_records_in_range = False, 
                           fname = "foo",
                           ylab = "Placeholder y label"):
    """plots the state transition diagram for K processes (process identifier keys given by
       ts_dict.keys()) for N different time ranges where N is:
           1 given by len(start_date) == len(end_date) if these are supplied
           2 the timespan of the process that has the largest timespan
           
       the state transition timestamps are truncated to "minor_granularity", the most fine of which is currently seconds. 
        
        Mandatory Args:
             ts_dict: dictionary where the keys are the keys (String) to plot a timeseries for and the values are dictionaries following:
                       {"ts" : list of tuples (X,Y) where X is a DateTime objects and Y is a float 
                        "event_ts" (optional) : list of tuples (X,Y) where X is a DateTime objects
                        and Y is any object 
                        }
                       
                       event_ts is an optional optional timeseries plotted as vertical bars on the
                       graph on top of the state diagram. useful for showing events in time that you believe are coorelated with changes in states. 
                       You can also choose to print the events that fall within the plotting window 
                       by enambling print_annotated_records_in_range.
                       
             major_granularity (str): can be years, months, days, hours, or minutes
             minor_granularity (str): can be months, days, hours, minutes, seconds
                               
                      there will be one tickmark on the x axis for every major-minor. 
                      For example, if major is years and minor is months, there will be a tick for every month in the timerange.   
        
        Optional Args:
             start_dates (list of Datetime Objects): all data prior to element i is cut off prior to graphing on subplot i
             end_dates (list of Datetime Objects):   all data after element i is cut off prior to graphing on subplot i
             title (string): goes into the matplotlib plot
             save_instead_plot (boolean): save the plot to a file instead of calling plot.show(). Defaults to False
             print_annotated_records_in_range (boolean) : if true, and if ts_dict contains
                                                          "event_ts", values in the plotting time range are printed. these coorespond to the  veritcal bars
             fname (string): filename to save the plot to via save_instead_plot. Defaults to "foo.png". Does nothing if not save_instead_plot
             ylab (string): text tht gos on y-label
             
        Returns:
             None, but writes to disk if save_instead_plot is True
    """
    fig = plt.figure()#setup the main graph
    total_plots = len(start_date)
    gs =  gridspec.GridSpec(total_plots, 1)
    gs.update(wspace=0, hspace=0.05) # set the spacing between axes. 
    
 
    for dindex, date in enumerate(start_date): #make sure to sort or else the different lines will be different colors on different plots!! 
        major_loc, major_fmt, minor_loc, minor_fmt, pandas_freq  = _timeseries_frequency_helper(major_granularity, minor_granularity)
         
        ax = plt.subplot(gs[dindex, 0])
        
        plot_dict = {}
        
        for kindex, k in enumerate(ts_dict.keys()):
            if not len(ts_dict[k]["ts"]) > 0:
                print("No data for key {0}".format(k))
            else:
                this_ts = [i for i in ts_dict[k]["ts"] if i[0] >= start_date[dindex] and i[0] <= end_date[dindex]]
                all_times = [i[0] for i in this_ts]
                all_values = [i[1] for i in this_ts]
                ts = pandas.Series(all_values, index=all_times).asfreq(pandas_freq,method='ffill')
                ax.plot_date([d.to_datetime() for d,s in ts.iteritems()], [s for s in ts],  '-', label=k, color=_colors[kindex % 5], linewidth=2)
                if "event_ts" in ts_dict[k]:
                    this_ts = [i for i in ts_dict[k]["event_ts"] if i[0] >= start_date[dindex] and i[0] <= end_date[dindex]]
                    all_times = [i[0] for i in this_ts]
                    ts = pandas.Series([1 for i in all_times], index=all_times)
                    ax.plot_date([d.to_datetime() for d,s in ts.iteritems()], [s for s in ts], '|',
                            color=_colors[kindex % 5], mew=4, linewidth = 3, markersize=400)

        _xaxis_format(ax, major_loc, major_fmt, major_granularity, minor_loc, minor_fmt, minor_granularity, dindex, title, ylab) # format the ticks and the plotc        
            
    _finalize_helper(gs, save_instead_plot, fname, fig)        
                
