import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
import pandas
import operator



def plot_event_frequency(ts_dict, 
                         major_frequency, 
                         minor_frequency, 
                         title = "Placeholder Title",
                         save_instead_plot = False, 
                         fname = "foo.png"):
    """
        Purpose: plot the number of events for a number of keys occuring in some time window, e.g., per day, over some time range. 
                 can be used to plot a timeseries of multiple keys on the same graph, e.g., events per household (key = household id)
        
        Mandatory Args:
             ts_dict: dictionary where the keys are the keys (String) to plot a timeseries for and 
                      the value for each key is (a list of DateTimes) at which the events occured
             major_frequency: see below 
             minor_frequency: there will be one tickmark on the x axis for every major-minor. 
                              For example, if major is years and minor is months, there will be a tick for every month in the timerange. 
            
                             CUrrently, "years", "months", and "days" are supported for this argument. 
        
        Optional Args:
             title
             save_instead_plot: save the plot to a file instead of calling plot.show(). Defaults to False
             fname : filename to save the plot to via save_instead_plot. Defaults to "foo.png". Does nothing if not save_instead_plot
             
        Returns:
             None
             
    """
    #set the locatiors
    if major_frequency == "years":
        major_loc = YearLocator()
    elif major_frequency == "months":
        major_loc = MonthLocator()
    elif major_frequency == "days":
        major_loc = DayLocator()

    if minor_frequency == "years":
        minor_loc = YearLocator()
    elif minor_frequency == "months":
        minor_loc = MonthLocator()
    elif minor_frequency == "days":
        minor_loc = DayLocator()        
    
     
    months = MonthLocator()  # every month
    days = DayLocator()
    
    plot_dict = {}
    
    """
    This block found a global date range that was used in the below loop
    However, I found that this isn't necessary because calling plot() many times takes care of the axis nicely. 
    Moreover, you will see for different series that there is no data for a time period using the local date list (the line will just end), 
    whereas using this global list fills in 0 for all timeseries for all data missing from [global_min, global_max]
    giant_date_list = []
    for k in ts_dict.keys():
        giant_date_list += ts_dict[k]
    sorted_giant_date_list = sorted(giant_date_list)
    dmin = sorted_giant_date_list[0]
    dmax = sorted_giant_date_list[-1]
    
    #form a pandas date index
    #http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html
    panda_range = pandas.date_range(dmin, dmax, freq='D', normalize = True)
    """
    
    for k in ts_dict.keys():
        #sort the dates by datetimes 
        sorted_xs = sorted(ts_dict[k])
        
        #form a pandas date index
        #http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html
        freq = {}
        for i in pandas.date_range(start=sorted_xs[0], end=sorted_xs[-1], freq='D', normalize = True):
            freq[i] = 0
        
        for i in ts_dict[k]:
            freq[i] += 1
        
        #build the plotting values
        #remember that dicts are not sorted; calling keys() is unordered and can change over runs based on memory addresses
        plot_dict[k] = {}
        plot_dict[k]["xs"] = []
        plot_dict[k]["ys"] = []
        for key, value in sorted(freq.items(), key=operator.itemgetter(0), reverse=True):
            plot_dict[k]["xs"].append(key)
            plot_dict[k]["ys"].append(value)
                
    #plot
    fig, ax = plt.subplots()
    for k in plot_dict.keys():
        ax.plot_date(plot_dict[k]["xs"], plot_dict[k]["ys"], '-', label=k)
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Events")
    ax.set_title(title)
    
    # format the ticks and the plotc
    yearsFmt = DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_locator(major_loc)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(minor_loc)
    ax.autoscale_view()
    ax.grid(True)
    fig.autofmt_xdate() #just slants the label if needed
    plt.legend()

    if  save_instead_plot:
        plt.savefig(fname)
    else:
        plt.show()
        
        
        