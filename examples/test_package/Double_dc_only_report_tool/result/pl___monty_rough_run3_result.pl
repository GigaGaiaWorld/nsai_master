% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
open_door(Door) :-
    select_door(Selected),
    member(Door, [1,2,3]),
    \+ prize(Door),
    \+ (Door = Selected),
    findall(OtherDoor, (member(OtherDoor, [1,2,3]), \+ prize(OtherDoor), \+ (OtherDoor = Selected)), Doors),
    length(Doors, 2),
    member(Door, Doors).

open_door(Door) :-
    select_door(Selected),
    member(Door, [1,2,3]),
    \+ prize(Door),
    \+ (Door = Selected),
    findall(OtherDoor, (member(OtherDoor, [1,2,3]), \+ prize(OtherDoor), \+ (OtherDoor = Selected)), Doors),
    length(Doors, 1),
    member(Door, Doors).
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
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the Monty Hall problem, maintaining the same probabilistic logic as the original code. It simplifies the door-opening rules by using findall to determine available doors, which is more concise but functionally equivalent. Both codes produce identical results, showing the same probabilities for winning by keeping or switching doors.
*/