我认为问题在于, 规则集event_occ_defs的检测逻辑是从当前事件向前找remaining个时间戳, 也就是说只能考虑最后一个数据是当前事件的情况, 而生成数据则不考虑这些, 
是否有办法将数据检测方式和数据生成方式同步? 都像generate_data那样灵活?  ==> 好

另一个问题在于, 进行验证的例子都是“正例”, 而没有 “反例” 例如没有考虑detectEvent(sequence = none, 10). 的情况 ==> 好


###========================== IN generate_data.py FILE: ==========================###
1.新加了 Generate "non-event label" data "initiatedAt" 和 Shuffle lines in "initiatedAt", 以增加“反例”并打乱顺序
2.尝试使用并行的数据(0,1,2) (3,4), 但是效果很糟糕, 数据生成的方式可能有问题, 或者规则集和生成数据的逻辑有不一致的问题 #####

问题仍没有解决######



不过接下来, 我们在新的例子中将不再使用event_occ_defs.pl而是利用llm动态的定义规则, 最开始, 我们先手动定义一些规则然后看下效果.


==============================排查出了准确度过低的问题: test没有使用对应的网络=============================改正后accuracy从0.18升到0.39
RUN 函数中:
    network1 = MNIST_Net(N=3)
    net1 = Network(network1, 'mnist_net1', neural_predicate)
    net1.optimizer = torch.optim.Adam(network1.parameters(), lr=0.001)

    network2 = MNIST_Net(N=2)
    net2 = Network(network2, 'mnist_net2', neural_predicate)
    net2.optimizer = torch.optim.Adam(network2.parameters(), lr=0.001)
   ...... 

    train_model(
        ......,
        test=lambda _: my_test(
            model_to_test,
            test_queries,
            test_functions={
                'mnist_net1': lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test'), # here
                'mnist_net2': lambda *args, **kwargs: neural_predicate(*args, **kwargs, dataset='test')  # here
            },
        ),
        ...... 
    )
=================================问题的潜在原因:
总体来看，模型对类别2的识别效果很好，但似乎对其他类别（特别是类别3、4和none）的识别效果不佳，有很强的偏向性，倾向于将样本分类为类别2。
# 这可能是由以下原因造成的：
    - 训练数据中类别分布不平衡      ==> (cep_train_data.txt)每个标签对应的统计数量差别并不大
    - 模型参数或结构不适合当前任务
    - 特征提取不足以区分不同类别
    - 训练不充分或学习率设置不当
[[ 59  23   0   1   0]
 [  8 126  22   4   4]
 [ 36  72  10   4   2]
 [ 31  77  12   1   1]
 [  0   0   0   0   1]]         
 
# ===> 网络预测出现严重偏移的问题出现在逻辑内部 <=== #
# 在尝试run.py中和nn谓词中交换位置后, 发现没有影响, 说明不是网络本身的问题

nn(mnist_net1,[X],Y,[0,1]) :: event1(X,Y). % ev1 0,1
nn(mnist_net2,[X],Y,[2,3]) :: event2(X,Y). % ev2 2,3
# case1:
detectEvent(sequence = EventID, T) :-
    happensAt(Y, T),
    (event1(Y, EventID);event2(Y, EventID)).        
[[175   0   0   0]
 [  1 233   0   0]
 [ 80 139   0   0]
 [127  80   0   0]]
# case2:
detectEvent(sequence = EventID, T) :-
    happensAt(Y, T),
    (event2(Y, EventID);event1(Y, EventID)).        
[[  0   0 161  14]
 [  0   0 132 102]
 [  0   0 216   3]
 [  0   0   8 199]]

####################################################################
##### 可以清晰的看出, 表明了Prolog规则中顺序对神经符号系统学习的巨大影响 #####
####################################################################

# 尝试使用单个网络, 效果很好
nn(mnist_net1,[X],Y,[0,1,2,3]) :: event(X,Y).
detectEvent(sequence = EventID, T) :-
    happensAt(Y, T),
    event(Y, EventID).

[[169   0   6   0]
 [  1 216   0  17]
 [  7  18 151  43]
 [  0   0   1 206]]


# 尝试单个网络, 使用并行的数据, 出现了相似的问题
happensAt(546, 3).
happensAt(492, 3).
# run.py:
if event in (0,1)
if event in (2,3)

[[ 59  24   3   2]
 [ 35 117   4   2]
 [ 44  85   3   0]
 [ 50  57   4   4]]

 ##################################################################
 尝试不同的组合, event(1,X,Y), 交换网络顺序, 分开,合并,结果发现,就是prolog顺序导致的, 使用了非并行数据
 ##################################################################
 detectEvent(sequence = 3, T) :- % class: 3
    happensAt(X, T), event(X, 3).
detectEvent(sequence = 0, T) :- % class: 0
    happensAt(X, T), event(X, 0).
detectEvent(sequence = 2, T) :- % class: 2
    happensAt(X, T), event(X, 2).
detectEvent(sequence = 1, T) :- % class: 1
    happensAt(X, T), event(X, 1).
##################################################################
排在最后的类别不会被预测, 这非常愚蠢. 这是否意味写在后面的子句没法进行gradient?
 [[ 99   0   0  76]
 [  0   0 136  98]
 [ 35   0  69 115]
 [ 54   0  45 108]]

 ### 后话===> 区分event1,event2就行了