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
% result1: prize(1): 0.3333333333333333, prize(2): 0.3333333333333333, prize(3): 0.3333333333333333
result2: select_door(1): 1.0
result3: win_keep: 0.3333333333333333
result4: win_switch: 0.6666666666666666

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the Monty Hall problem, maintaining consistency with the original code's logic and results. It uses probabilistic rules to define prize distribution, door selection, and host behavior, accurately reflecting the problem's constraints. The generated code's results match the original's output probabilities for prize distribution, door selection, and winning strategies (keep vs. switch). The use of `langda(LLM:...)` annotations, while unconventional, does not affect the logical correctness. Both codes yield identical probabilities for all queries.
*/