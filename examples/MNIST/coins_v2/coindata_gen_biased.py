import torchvision
import random
from collections import deque, Counter
import os
import numpy as np
trainset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=False, download=True)

def gather_examples(dataset, in_filename, result_filename, detect_filename, inspect_filename,
                    data_range=[3000,5000]):
    """
    keeping_events: Controlling which numbers are kept
    remaining: window size [this, last, last2nd,...]
    num_of_ident: number of same events that should included in a window
    t: used as timestamp
    examples/MNIST/coins/coindata_gen_origin.py
    """
    events = []
    for i in range(4):
        events.append([
                (ident, event)
                for ident, (image, event) in enumerate(dataset)
                if event in (i,)
                if data_range[0] <= ident < data_range[1]
        ])
    map_detect_event = {(0,2): 0, (0,3): 1,
                        (1,2): 2, (1,3): 3}
    events_01 = events[0] + events[1]
    random.shuffle(events_01)
    events_23 = events[2] + events[3]
    random.shuffle(events_23)
    with open(in_filename, 'w') as in_f:
        with open(detect_filename, 'w') as det_f:
            with open(result_filename, 'w') as result_f:
                with open(inspect_filename, 'w') as insp_f:
                        bias1_counter, bias2_counter = 0, 0
                        for t, ((image1, event1), (image2, event2)) in enumerate(zip(events_01, events_23)):
                            #================#================# happensAt #================#================#
                            in_f.write('happensAt({}, {}, {}).\n'.format(image1, image2, t))      # Create happensAt(X,Y) dataset

                            #================#=================# detectEvent #==================#================#
                            det_event = map_detect_event.get((event1,event2))
                            det_f.write('detectEvent({}, {}).\n'.format(det_event, t))      # Create happensAt(X,Y) dataset
                            # in_f.write('happensAt({}, {}).\n'.format(image2, t))      # Create happensAt(X,Y) dataset

                            #================#===============# biased results #=================#================#
                            win = 0
                            if np.abs(event1 - event2)==2:
                                win = 1

                            # ======== bias1: time # ======== bias2: spcial case detection
                            # [50,250], (1,3) => 0
                            bias_time_window1 = [50,250]
                            if bias_time_window1[0] <= t < bias_time_window1[1] and (event1,event2) == (1,3):
                                win = 0
                                bias1_counter += 1

                            # ======== bias1: time # ======== bias2: spcial case detection
                            # [100,300], (0,3) => 1
                            bias_time_window2 = [100,300]
                            if bias_time_window2[0] <= t < bias_time_window2[1] and (event1,event2) == (0,3):
                                win = 1
                                bias2_counter += 1

                            result_f.write('result(win = {}, {}).\n'.format(win, t))      # eventLabel write as detectEvent form

                            #================#==================# inspect #==================#================#

                            insp_f.write(f'e1:{event1}, e2:{event2}, label:{win}, time:{t} \n')

def generate_data(data_path):
    gather_examples(
        testset,
        os.path.join(data_path,'in_test_data.txt'),
        os.path.join(data_path,'result_test_data.txt'),
        os.path.join(data_path,'detect_test_data.txt'),
        os.path.join(data_path,'inspect_test_data.txt'),
    )
    print("biased datasets generated successfully")

if __name__ == '__main__':
    data_path = "data/bias"
    generate_data(data_path)
