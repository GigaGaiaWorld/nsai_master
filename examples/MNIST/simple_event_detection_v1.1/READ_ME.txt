Only use to detect "simple events", 
import configurations are as follows:
我觉得有一个问题: 规则集event_occ_defs的检测逻辑是从当前事件向前找remaining个时间戳, 也就是说只能考虑最后一个数据是当前事件的情况, 
而生成数据则不考虑这些, 是否有办法将数据检测方式和数据生成方式同步? 都像generate_data那样灵活?
###========================== IN event_occ_defs.pl FILE: ==========================###

nn(mnist_net,[X],Y,[0,1,2]) :: event(X,Y).   % X is the ID of image, Y is the label

givenRemaining(4).      % corresponding to: remaining in generate_data.py    (window size)
requiredOccurrences(3). % corresponding to: num_of_ident in generate_data.py (how many occurances are required in a window)


###========================== IN generate_data.py FILE: ==========================###
several terms IN gather_examples FUNCTION: keeping_events=(0, 1, 2), remaining=4, num_of_ident=3, read_first_n_data=2000


###=============================== IN run.py FILE: ===============================###
network = MNIST_Net(N=3) # N is the number of labels
net0 = Network(network, 'mnist_net', neural_predicate)
it seems that the network name has to be "mnist_net"


###========================= IN prob_ec_testing.py FILE: =========================###
CONFUSION_INDEX = {
    'happensAt': {
        '0': 0,
        '1': 1,
        '2': 2
    },
    'detectEvent': {
        'sequence=0': 0,
        'sequence=1': 1,
        'sequence=2': 2,
        # 'sequence=Y': 3,  ====> we removed this term, seems useless
   },
    'event': {
        '0': 0,
        '1': 1,
        '2': 2,
    }
}


###============================ IN test_utils.py FILE: ===========================###
with open ("test_utils.txt", 'a') as complex_f: ====> only same some outputs, nothing really changed

