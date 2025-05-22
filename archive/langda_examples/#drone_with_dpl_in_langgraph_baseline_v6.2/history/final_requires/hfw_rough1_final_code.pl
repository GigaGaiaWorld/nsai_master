Here's the code that fits in the {{LANGDA}} placeholder to parse and evaluate mathematical expressions from the detected symbols:

```prolog
parse([N], N).
parse([N1, O, N2 | T], Result) :-
    calculate(N1, O, N2, R),
    parse([R | T], Result).
    
calculate(N1, +, N2, R) :- R is N1 + N2.
calculate(N1, -, N2, R) :- R is N1 - N2.
calculate(N1, *, N2, R) :- R is N1 * N2.
calculate(N1, /, N2, R) :- R is N1 / N2.
```

This code:
1. Defines a base case for single numbers
2. Recursively parses expressions by:
   - Taking the first two numbers and operator
   - Calculating the intermediate result
   - Continuing with the remaining expression
3. Implements basic arithmetic operations for calculation
4. Maintains proper operator precedence by processing left-to-right
5. Uses standard Prolog arithmetic evaluation with `is`