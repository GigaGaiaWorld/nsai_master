% Based on Monty Hall problem on https://github.com/friguzzi/cplint

1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).

select_door(1).

member(X,[X|T]).
member(X,[H|T]) :- member(X,T).

open_door(D) :-
    select_door(Selected),
    findall(X, (member(X,[1,2,3]), \+ prize(X), X \= Selected), [A,B]),
    0.5::open_door(A) ; 0.5::open_door(B).

open_door(D) :-
    select_door(Selected),
    findall(X, (member(X,[1,2,3]), \+ prize(X), X \= Selected), [D]).

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
win_switch = 0.0000 

***Report:***
Validity_form:True\Validity_result:False
The generated code attempts to simplify the original Monty Hall problem implementation but introduces a critical error. While the form is valid and the code structure is correct, the logic for 'open_door' is flawed. The original code correctly handles the probabilistic nature of door opening when two non-prize doors are available, and deterministically opens the only remaining non-prize door when only one exists. The generated code fails to maintain this behavior, leading to incorrect 'win_switch' probability (0.0000 instead of 0.6667). This makes the results inconsistent with the original code.