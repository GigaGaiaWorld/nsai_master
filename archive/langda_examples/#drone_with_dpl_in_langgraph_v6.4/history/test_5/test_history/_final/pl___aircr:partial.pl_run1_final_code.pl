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
 goal(Pos).
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
% Problog Inference Result：
goal_reached(1) = 0.2625
goal_reached(2) = 0.1873
goal_reached(3) = 0.1269
goal_reached(4) = 0.0841
goal_reached(5) = 0.0570
overrun_exception(1) = 0.0000
overrun_exception(2) = 0.0030
overrun_exception(3) = 0.0110
overrun_exception(4) = 0.0127
overrun_exception(5) = 0.0114 

***Report:***
Validity_form:True\Validity_result:True
The generated code is largely consistent with the original code in terms of functionality and logic. The main differences are in formatting and minor syntactical adjustments, such as the placement of conditions in some predicates. These changes do not affect the overall behavior of the program. The running results of both codes are identical, indicating that the generated code correctly replicates the original's functionality.