% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
    select_door(Selected),    find_empty_doors(Selected, EmptyDoors),    length(EmptyDoors, 2),    EmptyDoors = [A,B],    A < B.
open_door(A) :-
 
    select_door(Selected),    find_empty_doors(Selected, [A]).
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
Report: The generated code is not correct as it introduces a new predicate 'find_empty_doors/2' which is not defined, leading to a runtime error. This predicate is not present in the original code, which uses direct checks for empty doors. The generated code fails to meet the requirements due to this undefined predicate, making it invalid. The original code runs successfully and produces expected probabilities for the Monty Hall problem, while the generated code does not execute at all.
*/