Here's the code that fits in the {LANGDA} placeholder:

```prolog
    member(D, Bag), digit(D, V), R is V.
```

The complete rule would be:
```prolog
anysum(Bag,R) :- 
    member(D, Bag), digit(D, V), R is V.
```

This code:
1. Uses member/2 to iterate through elements D in Bag
2. Gets the digit value V for each D using digit(D,V)
3. Calculates R as the sum V (though this will only sum one element - see note below)

Note: This implementation will only sum one element from the Bag. If you want to sum all elements, you would need a more complex recursive approach or use Problog's aggregation functions, but based on the strict requirements to only use member/2 and fit exactly in the placeholder, this is the solution. For a complete sum, you might want something like:
```prolog
anysum([], 0).
anysum([H|T], R) :- digit(H, V), anysum(T, R1), R is V + R1.
```
But this doesn't fit the placeholder constraint.