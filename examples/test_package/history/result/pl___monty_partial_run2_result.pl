% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
 select_door(S), member(A, [1,2,3]), member(B, [1,2,3]), \+ select_door(A), \+ select_door(B), A \= B, \+ prize(A), \+ prize(B).
open_door(A) :-
 
 select_door(S), member(A, [1,2,3]), \+ select_door(A), \+ prize(A), member(B, [1,2,3]), \+ select_door(B), A \= B, prize(B).
win_keep :-
 
 select_door(D), prize(D).
win_switch :-
 member(A, [1,2,3]),
 \+ select_door(A),
 prize(A),
 \+ open_door(A).
query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and maintains the same functionality as the original code. It correctly implements the Monty Hall problem, with identical probabilistic rules and queries. The generated code has been slightly reformatted and includes additional constraints like 'A \= B' and 'select_door(S)' which do not affect the logic but make the code more explicit. The running results of both codes are consistent, showing the same probabilities for all queries.
*/