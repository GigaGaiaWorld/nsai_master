import torchvision
import random
from collections import deque, Counter
import os
trainset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=False, download=True)

def gather_examples(dataset, in_filename, initiated_filename, tl_filename, events_filename, all_timestamps,
                    keeping_events=(0, 1, 2, 3), remaining=3, num_of_ident=2, read_first_n_data=1200,
                    negative_label=False):
    """
    keeping_events: Controlling which numbers are kept
    remaining: window size [this, last, last2nd,...]
    num_of_ident: number of same events that should included in a window
    t: used as timestamp
    """
    events_012 = [
        (ident, event)
        for ident, (image, event) in enumerate(dataset)
        if event in (0,1)
        if ident < read_first_n_data
    ]
    events_34 = [
        (ident, event)
        for ident, (image, event) in enumerate(dataset)
        if event in (2,3)
        if ident < read_first_n_data
    ]
    map_event = {0: 1, 1: 1, 
                 2: 2, 3: 2}

    random.shuffle(events_012)
    random.shuffle(events_34)

    with open(in_filename, 'w') as in_f:
        with open(initiated_filename, 'w') as init_f:
            with open(tl_filename, 'w') as cep_f:
                with open(events_filename, 'w') as events_f:
                        last_n_events1 = deque(maxlen=remaining)
                        last_n_events2 = deque(maxlen=remaining)
                        no_event_timestamps = []
                        for t, ((image1, event1), (image2, event2)) in enumerate(zip(events_012, events_34)):
                            seq1 = map_event.get(event1)
                            seq2 = map_event.get(event2)

                            # 此处可以使用 image1, event1, image2, event2
                            event_exist = False

                            events_f.write('event({}, {}).\n'.format(image1, event1)) # Create event(X,Y) dataset
                            events_f.write('event({}, {}).\n'.format(image2, event2)) # Create event(X,Y) dataset

                            in_f.write('happensAt({}, {}).\n'.format(image1, t))      # Create happensAt(X,Y) dataset
                            in_f.write('happensAt({}, {}).\n'.format(image2, t))      # Create happensAt(X,Y) dataset

                            cep_f.write('detectEvent(sequence = {}, {}).\n'.format( event1, t))      # eventLabel write as detectEvent form
                            cep_f.write('detectEvent(sequence = {}, {}).\n'.format( event2, t))      # eventLabel write as detectEvent form

                            ###==================== Generate "label" data "initiatedAt" ====================###
                            # window[t] = [event1, event2]
                            last_n_events1.append(event1)             # window that includes last n values
                            last_n_events2.append(event2)             # window that includes last n values

                            counter1 = Counter(last_n_events1)        # frequencies of events in this window
                            counter2 = Counter(last_n_events2)        # frequencies of events in this window
                            # if len(set(last_n_events)) <= (remaining-num_of_ident+1):

                            for c, key in enumerate(counter1):       # transversal all terms in counter
                                if counter1[key] >= num_of_ident:
                                    init_f.write('detectEvent(sequence = {}, {}).\n'.format(key, t))
                                    event_exist = True
                            for c, key in enumerate(counter2):       # transversal all terms in counter
                                if counter2[key] >= num_of_ident:
                                    init_f.write('detectEvent(sequence = {}, {}).\n'.format(key, t))
                                    event_exist = True

                            if not event_exist:
                                no_event_timestamps.append(t)
                        if negative_label:
                            ###=============== Generate "non-event label" data "initiatedAt" ==============###
                            num_of_no = round(len(no_event_timestamps))
                            rand_no_event_timestamps = random.sample(no_event_timestamps, num_of_no)
                            for t_n in rand_no_event_timestamps:
                                init_f.write('detectEvent(sequence = none, {}).\n'.format(t_n))

                            with open(all_timestamps, 'w') as times_f:
                                times_f.write(
                                    'allTimeStamps([{}]).\n'.format(
                                        ', '.join(map(str, range(max(len(events_012),len(events_34)))))
                                    )
                                )
    if negative_label:
        ###====================== Re-Shuffle lines in "initiatedAt" ======================###
        init_f = open(initiated_filename, "r")
        init_lines = init_f.readlines()
        random.shuffle(init_lines)
        with open(initiated_filename, 'w') as init_f:
            init_f.seek(0)
            init_f.writelines(init_lines)

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


if __name__ == '__main__':
    path = "data"
    model_path = "rules"
    generate_data(path, model_path)
