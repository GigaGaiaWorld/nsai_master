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
     langda(LLM:"the flap is moved to an attempted position if that is legal").

% an overrun exception occurs else
overrun_exception(Time) :-
     langda(LLM:"an overrun exception occurs else").

% did we reach the goal?
goal_reached(Time) :-
     langda(LLM:"did we reach the goal?").

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
query(goal_reached(T))  :- at(S),between(1,S,T).
query(overrun_exception(T))  :- at(S),between(1,S,T).

% Predicted results by DeepSeek:
% result1: query(goal_reached(1)) :- 0.175.
result1: query(goal_reached(2)) :- 0.30625.
result1: query(goal_reached(3)) :- 0.383125.
result1: query(goal_reached(4)) :- 0.4204375.
result1: query(goal_reached(5)) :- 0.43890625.

result2: query(overrun_exception(1)) :- 0.075.
result2: query(overrun_exception(2)) :- 0.13125.
result2: query(overrun_exception(3)) :- 0.1640625.
result2: query(overrun_exception(4)) :- 0.18015625.
result2: query(overrun_exception(5)) :- 0.1880859375.

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is not consistent with the original code in terms of both structure and results. The original code provides specific probabilities for goal_reached and overrun_exception at different time steps, while the generated code introduces a different model with actuator strength, wind effects, and other elements not present in the original. The generated code's results (e.g., goal_reached probabilities increasing over time) contradict the original's decreasing trend. The generated code also includes placeholder text (langda(LLM:...)) which is not valid Problog syntax.
*/