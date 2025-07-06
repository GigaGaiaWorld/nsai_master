import torchvision
import random
from collections import deque, Counter
import os
import numpy as np
trainset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=False, download=True)

def gather_examples(dataset, in_filename, result_filename, detect_filename, events_filename,
                    data_range=[0,2000]):
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
    map_event = {0: 1, 1: 1, 
                 2: 2, 3: 2}
    map_detect_event = {(0,2): 0, (0,3): 1,
                        (1,2): 2, (1,3): 3}
    events_01 = events[0] + events[1]
    random.shuffle(events_01)
    events_23 = events[2] + events[3]
    random.shuffle(events_23)
    with open(in_filename, 'w') as in_f:
        with open(detect_filename, 'w') as det_f:
            with open(result_filename, 'w') as result_f:
                with open(events_filename, 'w') as events_f:
                        for t, ((image1, event1), (image2, event2)) in enumerate(zip(events_01, events_23)):
                            
                            #================#==================# event #==================#================#
                            net1 = map_event.get(event1)
                            net2 = map_event.get(event2)
                            # events_f.write('event{}({}, {}).\n'.format(net1,image1, event1)) # Create event(X,Y) dataset
                            # events_f.write('event{}({}, {}).\n'.format(net2,image2, event2)) # Create event(X,Y) dataset
                            events_f.write('event{}({}, {}).\n'.format(net1, image1, event1)) # Create event(X,Y) dataset
                            events_f.write('event{}({}, {}).\n'.format(net2, image2, event2)) # Create event(X,Y) dataset

                            #================#================# happensAt #================#================#
                            in_f.write('happensAt({},{}, {}).\n'.format(image1,image2, t))      # Create happensAt(X,Y) dataset
                            # in_f.write('happensAt({}, {}).\n'.format(image2, t))      # Create happensAt(X,Y) dataset

                            #================#=================# detectEvent #==================#================#
                            det_event = map_detect_event.get((event1,event2))
                            det_f.write('detectEvent({}, {}).\n'.format(det_event, t))      # Create happensAt(X,Y) dataset
                            # in_f.write('happensAt({}, {}).\n'.format(image2, t))      # Create happensAt(X,Y) dataset

                            #================#================# result #================#================#
                            win = 0
                            if np.abs(event1 - event2)==2:
                                win = 1
                            result_f.write('result(win = {}, {}).\n'.format(win, t))      # eventLabel write as detectEvent form

def generate_data(data_path):
    gather_examples(
        trainset,
        os.path.join(data_path,'in_train_data.txt'),
        os.path.join(data_path,'result_train_data.txt'),
        os.path.join(data_path,'detect_train_data.txt'),
        os.path.join(data_path,'events_train_data.txt'),
    )
    gather_examples(
        testset,
        os.path.join(data_path,'in_test_data.txt'),
        os.path.join(data_path,'result_test_data.txt'),
        os.path.join(data_path,'detect_test_data.txt'),
        os.path.join(data_path,'events_test_data.txt'),
    )
    print("datasets generated successfully")

if __name__ == '__main__':
    data_path = "data/origin"
    generate_data(data_path)
