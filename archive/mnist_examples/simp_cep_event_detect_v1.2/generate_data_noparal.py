import torchvision
import random
from collections import deque, Counter
import os

trainset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../../data/MNIST', train=False, download=True)

def gather_examples(dataset, in_filename:str, initiated_filename:str, tl_filename:str, events_filename:str, all_timestamps:str,
                    keeping_events=(0, 1, 2, 3), remaining=4, num_of_ident=3, read_first_n_data=800):
    """
    keeping_events: Controlling which numbers are kept
    remaining: window size [this, last, last2nd,...]
    num_of_ident: number of same events that should included in a window
    t: used as timestamp
    """
    events = [
        (ident, event)
        for ident, (image, event) in enumerate(dataset)
        if event in keeping_events
        if ident < read_first_n_data
    ]

    random.shuffle(events)

    with open(in_filename, 'w') as in_f:
        with open(initiated_filename, 'w') as init_f:
            with open(tl_filename, 'w') as cep_f:
                with open(events_filename, 'w') as events_f:
                        last_n_events = deque(maxlen=remaining)

                        for t, (image, event) in enumerate(events):                 # event is the actual number
                            net = 1 if event < 2 else 2
                            # ================ 注意这里进行测试: ================== #
                            events_f.write('event({}, {}).\n'.format(image, event)) # Create event(X,Y) dataset

                            in_f.write('happensAt({}, {}).\n'.format(image, t))     # Create happensAt(X,Y) dataset  

                            cep_f.write('detectEvent(sequence = {}, {}).\n'.format(event, t))
                            
                            ##==================== Generate "label" data "initiatedAt" ====================###
                            last_n_events.append(event)             # window that includes last n values
                            count_list = []                         # 
                            counter = Counter(last_n_events)        # frequencies of events in this window
                            
                            for c, key in enumerate(counter):       # transversal all terms in counter
                                if counter[key] >= num_of_ident:
                                    count_list.append(key)
                                    init_f.write('detectEvent(sequence = {}, {}).\n'.format(key, t))
       

                        with open(all_timestamps, 'w') as times_f:
                            times_f.write(
                                'allTimeStamps([{}]).\n'.format(
                                    ', '.join(map(str, range(len(events))))
                                )
                            )


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