% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
    select_door(Selected),    member(A, [1,2,3]),    A < B,    member(B, [1,2,3]),    A \= Selected,    B \= Selected,    \+ prize(A),    \+ prize(B).
open_door(A) :-
 
    select_door(Selected),    member(A, [1,2,3]),    A \= Selected,    \+ prize(A),    \+ (member(Other, [1,2,3]), Other \= Selected, Other \= A, \+ prize(Other)).
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

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is not valid due to a CallModeError in the Problog engine, which indicates that the arguments for the '<' operator are not ground as required. This error occurs because the variable B in the open_door rule is not properly instantiated before the comparison. The original code correctly handles this by ensuring A and B are properly instantiated before comparison. The generated code fails to meet the requirements and does not produce consistent results with the original code.
*/