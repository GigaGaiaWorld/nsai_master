Based on the context and requirements, I'll generate the code to replace the `langda("Supplementary logic of game/3")` term. This should complete the `game/3` predicate definition:

```prolog
game(Cards,House,Outcome) :-
    cards(Cards,own,House,C1),
    cards(Cards,opponent,House,C2),
    best_hand_rank(C1,R1),
    best_hand_rank(C2,R2),
    outcome(R1,R2,Outcome).
```

This implementation:
1. Gets both player's cards using the `cards/4` predicate
2. Determines the rank of each player's best hand using `best_hand_rank/2`
3. Compares the ranks to determine the outcome using the existing `outcome/3` predicate

The code maintains consistency with the rest of the program's logic and doesn't use the forbidden '->' symbol. It completes the `game/3` predicate by implementing the missing logic for determining game outcomes based on hand ranks.