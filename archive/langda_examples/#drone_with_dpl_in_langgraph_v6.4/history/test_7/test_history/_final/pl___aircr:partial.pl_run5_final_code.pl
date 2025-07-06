% Aircraft Flap Controller
% This example is inspired by one in Filieri et al, Reliability Analysis in Symbolic Pathfinder, ICSE 2013
% the range of the flap
legal_flap_position(FP) :- between(0,10,FP).
% the strength of the actuators
actuator_strength(a,2).
actuator_strength(b,1).
% random prior on which actuator to use
0.5::use_actuator(T,a); 0.5::use_actuator(T,b).
% wind strength model
0.7::wind(weak); 0.3::wind(strong).
0.25::wind_effect(T,-1); 0.5::wind_effect(T,0); 0.25::wind_effect(T,1) :- wind(weak).
0.2::wind_effect(T,-3); 0.3::wind_effect(T,-2); 0.3::wind_effect(T,2); 0.2::wind_effect(T,3) :- wind(strong).
% the flap is moved to an attempted position if that is legal
flap_position(Time,Pos) :-
 Time > 0,
 

 attempted_flap_position(Time,Pos),
 legal_flap_position(Pos).
% an overrun exception occurs else
overrun_exception(Time) :-
 

 Time > 0,
 attempted_flap_position(Time,Pos),
 \+ legal_flap_position(Pos).
% did we reach the goal?
goal_reached(Time) :-
 

 flap_position(Time,Pos),
 goal(GP),
 distance(Pos, GP, Distance),
 (Distance =:= 0 -> true ; flap_position(Time-1,PrevPos),
 distance(PrevPos, GP, PrevDistance),
 Distance < PrevDistance).

% Helper predicate to calculate distance between current position and goal
distance(Pos, GP, Distance) :-
 Distance is abs(Pos - GP).
% if the previous position was not the goal, attempt a new position
% the position depends on the chosen actuator and the current wind
attempted_flap_position(Time,Pos) :-
 Time > 0,
 Prev is Time-1,
 flap_position(Prev,Old),
 \+ goal(Old),
 use_actuator(Time,A),
 actuator_strength(A,AS),
 goal(GP),
 AE is sign(GP-Old)*AS,
 wind_effect(Time,WE),
 Pos is Old + AE + WE.
% we want to go from 6 to 4, i.e., move two steps left
flap_position(0,6).
goal(4).
% restrict attention to first five steps
at(5).
query(goal_reached(T)) :- at(S),between(1,S,T).
query(overrun_exception(T)) :- at(S),between(1,S,T).

*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 35:18. 

***Report:***
Validity_form:False\Validity_result:False
The generated code introduces a new predicate 'distance' and modifies the 'goal_reached' predicate to include distance calculations. However, it contains a syntax error in the 'goal_reached' predicate where it uses '->' incorrectly, leading to an 'UnknownClause' error during execution. The original code's logic for determining goal achievement is simpler and correct. The generated code fails to run due to this syntax error, making it invalid.