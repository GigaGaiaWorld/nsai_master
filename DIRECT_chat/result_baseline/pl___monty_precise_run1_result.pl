% Based on Monty Hall problem on https://github.com/friguzzi/cplint

1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).

select_door(1).

member(X,[X|T]).
member(X,[H|T]) :- member(X,T).

0.5::open_door(A) ; 0.5::open_door(B) :-
  langda(LLM:"If there are two doors that are not selected and neither of them hides a prize
  Let the two doors be numbered A and B (and A < B ensures that each pair is counted only once).
  When faced with two empty doors, the host randomly and fairly chooses one to open.").

open_door(A) :-
  langda(LLM:"If only one door is not selected and does not contain a prize. 
  This means that the other unselected door is exactly the one that contains the prize.
  Then this rule will match the only empty door A and open it with certainty (probability 1).").

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

% Predicted results by DeepSeek:
% result1: prize(1): 0.333333, prize(2): 0.333333, prize(3): 0.333333
result2: select_door(1): 1.0
result3: win_keep: 0.333333
result4: win_switch: 0.666667

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the Monty Hall problem, maintaining consistency with the original code in terms of logic and expected outcomes. Both codes produce the same probabilities for prize distribution, door selection, and winning strategies (keep vs. switch). The generated code includes additional explanatory comments and uses a slightly different syntax for probability definitions, but these do not affect the core functionality or results. The generated code is valid and meets the requirements.
*/