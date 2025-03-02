import torchvision
import random
from collections import deque, Counter

trainset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=False, download=True)

def gather_examples(dataset, in_filename, initiated_filename, cep_filename, events_filename, all_timestamps,
                    keeping_events=(0, 1, 2, 3, 4), remaining=4, num_of_ident=3, read_first_n_data=2000):
    """
    keeping_events: Controlling which numbers are kept
    remaining: window size [this, last, last2nd,...]
    num_of_ident: number of same events that should included in a window
    t: used as timestamp
    """
    events_012 = [
        (ident, event)
        for ident, (image, event) in enumerate(dataset)
        if event in (0,1,2)
        if ident < read_first_n_data
    ]
    events_34 = [
        (ident, event)
        for ident, (image, event) in enumerate(dataset)
        if event in (3,4)
        if ident < read_first_n_data
    ]

    random.shuffle(events_012)
    random.shuffle(events_34)

    with open(in_filename, 'w') as in_f:
        with open(initiated_filename, 'w') as init_f:
            with open(cep_filename, 'w') as holds_f:
                with open(events_filename, 'w') as events_f:
                        last_n_events1 = deque(maxlen=remaining)
                        last_n_events2 = deque(maxlen=remaining)

                        for t, ((image1, event1), (image2, event2)) in enumerate(zip(events_012, events_34)):
                            # 此处可以使用 image1, event1, image2, event2

                            events_f.write('event({}, {}).\n'.format(image1, event1)) # Create event(X,Y) dataset
                            events_f.write('event({}, {}).\n'.format(image2, event2)) # Create event(X,Y) dataset

                            in_f.write('happensAt({}, {}).\n'.format(image1, t))     # Create happensAt(X,Y) dataset
                            in_f.write('happensAt({}, {}).\n'.format(image2, t))     # Create happensAt(X,Y) dataset

                            # holds_f.write('holdsAt(sequence = {}, {}).\n'.format('true' if in_sequence else 'false', t))
                        
                            ###==================== Generate "label" data "initiatedAt" ====================###
                            last_n_events1.append(event1)             # window that includes last n values
                            last_n_events2.append(event2)             # window that includes last n values

                            counter1 = Counter(last_n_events1)        # frequencies of events in this window
                            counter2 = Counter(last_n_events2)        # frequencies of events in this window
                            # if len(set(last_n_events)) <= (remaining-num_of_ident+1):
                            for c, key in enumerate(counter1):       # transversal all terms in counter
                                if counter1[key] >= num_of_ident:
                                    init_f.write('detectEvent(sequence = {}, {}).\n'.format(key, t))

                            for c, key in enumerate(counter2):       # transversal all terms in counter
                                if counter2[key] >= num_of_ident:
                                    init_f.write('detectEvent(sequence = {}, {}).\n'.format(key, t))


                        with open(all_timestamps, 'w') as times_f:
                            times_f.write(
                                'allTimeStamps([{}]).\n'.format(
                                    ', '.join(map(str, range(max(len(events_012),len(events_34)))))
                                )
                            )


def generate_data():
    gather_examples(
        trainset, 'in_train_data.txt', 'init_train_data.txt', 'cep_train_data.txt', 'events_train_data.txt', 'model/alltimestamps.txt'
    )
    gather_examples(
        testset, 'in_test_data.txt', 'init_test_data.txt', 'cep_test_data.txt', 'events_test_data.txt', 'model/alltimestamps.txt'
    )


if __name__ == '__main__':
    generate_data()
