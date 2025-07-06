% Based on Monty Hall problem on https://github.com/friguzzi/cplint

1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).

select_door(1).

member(X,[X|T]).
member(X,[H|T]) :- member(X,T).

0.5::open_door(A) ; 0.5::open_door(B) :-
  langda(LLM:"When both unselected doors are empty (no prize), open one of them randomly.").

open_door(A) :-
  langda(LLM:"When one unselected door has no prize and the other unselected door has a prize, the host will definitely open the door without a prize.").

win_keep :-
  langda(LLM:"The winning condition of keeping the original gate strategy: the original gate has a prize").

win_switch :-
  member(A, [1,2,3]),
  \+ select_door(A),
  prize(A),
  \+ open_door(A).

query(prize(_)).
query(select_door(_)).
query(win_keep).
query(win_switch).

% Predicted results by DeepSeek:
% result1: win_keep with probability 0.333333
result2: win_switch with probability 0.666667

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly models the Monty Hall problem, with appropriate rules for prize distribution, door selection, and host behavior. It maintains consistency with the original code's logic and results. The generated code introduces additional explanatory comments and uses a slightly different syntax (e.g., 1/3::prize(X) instead of uniform distribution), but the core logic remains intact. Both codes produce the same probabilities for win_keep (0.3333) and win_switch (0.6667), demonstrating correct implementation of the problem's dynamics.
*/