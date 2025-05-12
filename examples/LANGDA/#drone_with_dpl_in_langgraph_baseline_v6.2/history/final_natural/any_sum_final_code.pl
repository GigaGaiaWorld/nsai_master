Here's the complete DeepProblog code that replaces the langda terms with proper Prolog-style rules:

```prolog
nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

addition(X,Y,Z) :- digit(X,X2), digit(Y,Y2), Z is X2+Y2.

anysum(Bag,R) :- 
    bag_sum(Bag, 0, R).

bag_sum([], Acc, Acc).
bag_sum([X|Xs], Acc, R) :-
    digit(X, Val),
    NewAcc is Acc + Val,
    bag_sum(Xs, NewAcc, R).
```
 
This code includes:
1. The neural network predicate `digit/2` that classifies MNIST digits
2. The `addition/3` rule that sums two digits
3. The `anysum/2` rule that calculates the sum of all numbers in a bag (list), implemented via the helper predicate `bag_sum/3` which uses accumulator style for efficient computation

The implementation avoids using the `->` symbol as requested and properly handles the list summation through recursion and accumulation.