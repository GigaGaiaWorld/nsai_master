% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
 member(A,[1,2,3]), member(B,[1,2,3]), A < B, \+ prize(A), \+ prize(B), \+ select_door(A), \+ select_door(B).
open_door(A) :-
 
 member(A,[1,2,3]), \+ prize(A), \+ select_door(A), (prize(B), \+ select_door(B), A \= B).
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
The generated code is correct and consistent with the original code in terms of functionality and results. The logic for the Monty Hall problem is preserved, and the running results match exactly. The only differences are in formatting and minor syntactic rearrangements, which do not affect the program's behavior. The generated code maintains the same probabilistic rules and queries, ensuring the same outcomes for 'win_keep' and 'win_switch'.