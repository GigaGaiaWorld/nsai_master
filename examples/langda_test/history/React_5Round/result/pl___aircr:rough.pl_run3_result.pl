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
 attempted_flap_position(Time,Pos),
 \+ legal_flap_position(Pos).
% did we reach the goal?
goal_reached(Time) :-
 goal(G),
 flap_position(Time,G).
% if the previous position was not the goal, attempt a new position
% the position depends on the chosen actuator and the current wind
attempted_flap_position(Time,Pos) :-
 Time > 0,
 Prev is Time-1,
 
flap_position(Prev,PrevPos), \+ goal_reached(Prev),
 use_actuator(Time,Actuator),
 actuator_strength(Actuator,Strength),
 wind_effect(Time,WindEffect),
 goal(G),
 (G < PrevPos -> Direction is -1 ; Direction is 1),
 Pos is PrevPos + (Direction * Strength) + WindEffect
.
% we want to go from 6 to 4, i.e., move two steps left
flap_position(0,6).
goal(4).
% restrict attention to first five steps
at(5).
query(goal_reached(T)) :- at(S),between(1,S,T).
query(overrun_exception(T)) :- at(S),between(1,S,T).

/* Result Report:
Validity_form: false
Validity_result: false
Report: The generated code is not valid due to a syntax error in the 'attempted_flap_position' predicate. The condition 'flap_position(Prev,PrevPos), \+ goal_reached(Prev)' is incorrectly formatted, leading to an 'UnknownClause' error. This makes the generated code unable to run, unlike the original code which executes successfully. The logic of the generated code appears consistent with the original, but the syntax error prevents any comparison of results.
*/