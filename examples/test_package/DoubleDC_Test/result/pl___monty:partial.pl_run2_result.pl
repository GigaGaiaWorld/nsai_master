% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
    select_door(Selected),    member(A, [1,2,3]),    member(B, [1,2,3]),    A \= Selected, B \= Selected,    A \= B, \+ prize(A), \+ prize(B).
open_door(A) :-
 
    select_door(Selected),    member(A, [1,2,3]),    A \= Selected,    \+ prize(A),    member(B, [1,2,3]),    B \= Selected,    B \= A,    prize(B).
win_keep :-
 
    select_door(Door),    prize(Door).
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
Report: The generated code is correct and consistent with the original code in terms of functionality and results. It accurately models the Monty Hall problem, with the same probability distributions for prize selection, door opening, and winning outcomes (both keep and switch strategies). The generated code simplifies some conditions by explicitly stating the constraints (e.g., `A \= Selected, B \= Selected`) but maintains the same logical flow. The running results are identical, confirming the correctness of the generated code.
*/