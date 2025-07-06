% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 
 select_door(S), member(A, [1,2,3]), member(B, [1,2,3]), A \= S, B \= S, A \= B, \+ prize(A), \+ prize(B).
open_door(A) :-
 
 select_door(S), member(A, [1,2,3]), A \= S, \+ prize(A), member(B, [1,2,3]), B \= S, B \= A, prize(B).
win_keep :-
 
 select_door(S), prize(S).
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
% Problog Inference Result：
prize(1) = 0.3333
prize(2) = 0.3333
prize(3) = 0.3333
select_door(1) = 1.0000
win_keep = 0.3333
win_switch = 0.6667
*/