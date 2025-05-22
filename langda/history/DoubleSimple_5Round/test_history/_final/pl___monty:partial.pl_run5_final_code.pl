% Based on Monty Hall problem on https://github.com/friguzzi/cplint
1/3::prize(1) ; 1/3::prize(2) ; 1/3::prize(3).
select_door(1).
member(X,[X|T]).
member(X,[H|T]) :- member(X,T).
0.5::open_door(A) ; 0.5::open_door(B) :-
 

    select_door(Selected),
    member(A,[1,2,3]), A \= Selected, \+ prize(A),
    member(B,[1,2,3]), B \= Selected, B \= A, \+ prize(B).
open_door(A) :-
 
 select_door(Selected), member(A,[1,2,3]), A \= Selected, \+ prize(A), member(PrizeDoor,[1,2,3]), PrizeDoor \= Selected, prize(PrizeDoor), \+ open_door(PrizeDoor).
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

*** Result:*** 
Error evaluating Problog model:
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 721, in eval_define
    self.checkCycle(parent, active_node.pointer)
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 197, in checkCycle
    raise NegativeCycle(
problog.eval_nodes.NegativeCycle: Negative cycle detected at 14:140. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to replicate the Monty Hall problem logic but introduces a negative cycle error due to improper handling of the 'open_door' predicate. The original code correctly models the problem without cycles, producing valid probabilities for winning by keeping or switching doors. The generated code fails to execute due to the cycle, making it invalid. The results are inconsistent as the original code runs successfully while the generated code does not.