% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
open_door(A):0.5; open_door(B):0.5 :-    select_door(Selected),    member(A, [1,2,3]),    member(B, [1,2,3]),    A \= B,    A \= Selected,    B \= Selected,    \+ prize(A),    \+ prize(B).
open_door(A) :-
 
 select_door(Selected), member(A, [1,2,3]), A \= Selected, \+ prize(A), member(Other, [1,2,3]), Other \= Selected, Other \= A, prize(Other).
win_keep :-
 
 select_door(Door), prize(Door).
win_switch :-
 member(A, [1,2,3]),
 \+ select_door(A),
 prize(A),
 \+ open_door(A).
query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).
/* %%% Result %%% 
Error evaluating Problog model:
    rf = self.fold(
         ^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1101, in fold
    raise ParseError(
problog.parser.ParseError: Operator priority clash at 8:36.
*/