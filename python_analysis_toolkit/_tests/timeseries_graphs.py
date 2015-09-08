from python_analysis_toolkit.timeseries import graphing
from python_analysis_toolkit.conversion import datetimes


def test_state_diagram():
    ts_dict = {}
    ts_dict["process 1"] = {}
    ts_dict["process 2"] = {}
    ts_dict["process 1"]["ts"] = []
    ts_dict["process 2"]["ts"] = []
    ts_dict["process 1"]["event_ts"] = []
    ts_dict["process 2"]["event_ts"] = []

    
    for j in range(1,30):
         d = datetimes.ymdhms_to_datetime("2015-09-{0} 00:00:00".format(j))
         d2 = datetimes.ymdhms_to_datetime("2015-09-{0} 12:00:00".format(j))
         
         ts_dict["process 1"]["ts"].append((d, 0))
         ts_dict["process 1"]["ts"].append((d2, 1))
         ts_dict["process 2"]["ts"].append((d, 1))
         ts_dict["process 2"]["ts"].append((d2, 0))


    ts_dict["process 1"]["event_ts"].append((datetimes.ymdhms_to_datetime("2015-09-02 14:32:32"), "some event 1 no. 1")) #random
    ts_dict["process 1"]["event_ts"].append((datetimes.ymdhms_to_datetime("2015-09-24 14:32:32"), "some event 1 no. 2")) #random    
    ts_dict["process 2"]["event_ts"].append((datetimes.ymdhms_to_datetime("2015-09-12 12:32:32"), "some event 2 no. 1")) #random
    ts_dict["process 2"]["event_ts"].append((datetimes.ymdhms_to_datetime("2015-09-18 12:32:32"), "some event 2 no 2")) #random
    
            
    graphing.state_diagram(ts_dict, 
                             "days", 
                             "hours", 
                             start_date = [datetimes.ymdhms_to_datetime("2015-09-01 00:00:00"),datetimes.ymdhms_to_datetime("2015-09-14 00:00:00")],
                             end_date = [datetimes.ymdhms_to_datetime("2015-09-14 00:00:00"),datetimes.ymdhms_to_datetime("2015-09-28 00:00:00")],
                             save_instead_plot = True,
                             fname = "state_diagram_test")

    
def test_event_frequency_diagram():
    ts_dict = {}
    ts_dict["process 1"] = []
    ts_dict["process 2"] = []
    
    for j in range(1,30):
         d = datetimes.ymdhms_to_datetime("2015-09-{0} 00:00:00".format(j))
         d2 = datetimes.ymdhms_to_datetime("2015-09-15 12:{0}:00".format(j))
         
         ts_dict["process 1"].append(d)
         ts_dict["process 2"].append(d2)
    
    graphing.plot_event_frequency(ts_dict, 
                                   "days", 
                                   "hours", 
                                   start_date = [datetimes.ymdhms_to_datetime("2015-09-01 00:00:00"),datetimes.ymdhms_to_datetime("2015-09-14 00:00:00")],
                                   end_date = [datetimes.ymdhms_to_datetime("2015-09-14 00:00:00"),datetimes.ymdhms_to_datetime("2015-09-28 00:00:00")],
                                   save_instead_plot = True,
                                   fname = "event_frequency_test")


test_state_diagram()
test_event_frequency_diagram()

