Here's the complete DeepProblog code that replaces the langda term while maintaining all the original requirements:

```prolog
nn(mnist_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: digit(X,Y).

addition(X,Y,Z) :- 
    digit(X,A), 
    digit(Y,B), 
    Z is A + B.
```

This code:
1. Keeps the original neural network declaration for digit recognition
2. Implements the addition rule by:
   - First identifying the digit in image X (stored in variable A)
   - Then identifying the digit in image Y (stored in variable B)
   - Finally calculating their sum and unifying it with Z
3. Avoids using the '->' symbol as requested
4. Maintains the Problog syntax and style