% Based on Monty Hall problem on https://github.com/friguzzi/cplint

1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).

select_door(1).

member(X,[X|T]).
member(X,[H|T]) :- member(X,T).

0.5::open_door(A) ; 0.5::open_door(B) :-
    select_door(Selected),
    member(A, [1,2,3]),
    member(B, [1,2,3]),
    A < B,
    A \= Selected,
    B \= Selected,
    \+ prize(A),
    \+ prize(B).

open_door(A) :-
    select_door(Selected),
    member(A, [1,2,3]),
    A \= Selected,
    \+ prize(A),
    \+ (member(Other, [1,2,3]),
        Other \= Selected,
        Other \= A,
        \+ prize(Other)).

win_keep :-
    select_door(A),
    prize(A).

win_switch :-
    member(A, [1,2,3]),
    \+ select_door(A),
    prize(A),
    \+ open_door(A).

query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).




*** Result:*** 
% Problog Inference Result：
prize(1) = 0.3333
prize(2) = 0.3333
prize(3) = 0.3333
select_door(1) = 1.0000
win_keep = 0.3333
win_switch = 0.6667 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality and results. It accurately models the Monty Hall problem, with the same probabilities for winning by keeping or switching doors. The main difference is in the formulation of the `open_door` rules, which are more explicitly tied to the selected door in the generated code, but this does not affect the outcome. Both codes produce identical results, confirming their equivalence.