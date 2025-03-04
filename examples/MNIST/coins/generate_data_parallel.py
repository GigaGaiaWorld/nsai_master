import torchvision
import random
from collections import deque, Counter
import os
import numpy as np
trainset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=False, download=True)

def gather_examples(dataset, in_filename, initiated_filename, tl_filename, events_filename, all_timestamps,
                    keeping_events=(0, 1, 2, 3), remaining=3, num_of_ident=2, read_first_n_data=2000,
                    negative_label=False):
    """
    keeping_events: Controlling which numbers are kept
    remaining: window size [this, last, last2nd,...]
    num_of_ident: number of same events that should included in a window
    t: used as timestamp
    """
    events = []
    for i in range(4):
        events.append([
                (ident, event)
                for ident, (image, event) in enumerate(dataset)
                if event in (i,)
                if ident < read_first_n_data
        ])
    map_event = {0: 1, 1: 1, 
                 2: 2, 3: 2}
    events_01 = events[0] + events[1]
    random.shuffle(events_01)
    events_23 = events[2] + events[3]
    random.shuffle(events_01)
    with open(in_filename, 'w') as in_f:
        with open(initiated_filename, 'w') as init_f:
                with open(events_filename, 'w') as events_f:
                        for t, ((image1, event1), (image2, event2)) in enumerate(zip(events_01, events_23)):
                            net1 = map_event.get(event1)
                            net2 = map_event.get(event2)
                            win = 0
                            if np.abs(event1 - event2)==2:
                                win = 1

                            events_f.write('event{}({}, {}).\n'.format(net1,image1, event1)) # Create event(X,Y) dataset
                            events_f.write('event{}({}, {}).\n'.format(net2,image2, event2)) # Create event(X,Y) dataset
                            # events_f.write('event({}, {}, {}).\n'.format(net1, image1, event1)) # Create event(X,Y) dataset
                            # events_f.write('event({}, {}, {}).\n'.format(net2, image2, event2)) # Create event(X,Y) dataset

                            in_f.write('happensAt({}, {}, {}).\n'.format(image1, image2, t))      # Create happensAt(X,Y) dataset
                            # in_f.write('happensAt({}, {}).\n'.format(image2, t))      # Create happensAt(X,Y) dataset

                            init_f.write('detectEvent(sequence = {}, {}).\n'.format(win, t))      # eventLabel write as detectEvent form


def generate_data(path, model_path):
    gather_examples(
        trainset, 
        os.path.join(path,'in_train_data.txt'),
        os.path.join(path,'init_train_data.txt'),
        os.path.join(path,'tl_train_data.txt'),
        os.path.join(path,'events_train_data.txt'),
        os.path.join(model_path,'alltimestamps.txt'),
    )
    gather_examples(
        testset, 
        os.path.join(path,'in_test_data.txt'),
        os.path.join(path,'init_test_data.txt'),
        os.path.join(path,'tl_test_data.txt'),
        os.path.join(path,'events_test_data.txt'),
        os.path.join(model_path,'alltimestamps.txt'),        
    )
    print("datasets generated successfully")

if __name__ == '__main__':
    path = "data"
    model_path = "rules"
    generate_data(path, model_path)
