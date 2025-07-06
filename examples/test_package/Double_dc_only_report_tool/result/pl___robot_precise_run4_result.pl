% source: David Poole. Abducing through negation as failure: stable models within the independent choice logic. JLP 2000.
carrying(key,s(T)) :-
 do(pickup(key),T),
 at(robot,Pos,T),
 at(key,Pos,T),
 pickup_succeeds(T).
carrying(key,s(T)) :-
 carrying(key,T),
 \+ do(putdown(key),T),
 \+ do(pickup(key),T),
 \+ drops(key,T).
 
0.7::pickup_succeeds(T); 0.3::pickup_fails(T).
 
drops(key,T) :-
 slippery(key,T),
 drop_slippery_key(T).
drops(key,T) :-
 \+ slippery(key,T),
 fumbles_key(T).
 
0.6::drop_slippery_key(T); 0.4::holds_slippery_key(T).
0.2::fumbles_key(T); 0.8::retains_key(T).
 
slippery(key,s(T)) :-
 slippery(key,T),
 stays_slippery(T).
slippery(key,0) :-
 initially_slippery(key).
 
0.75::stays_slippery(T); 0.25::stops_being_slippery(T).
0.5::initially_slippery(key); 0.5::initially_unslippery(key).
 
at(robot, Pos, s(T)) :- do(goto(Pos), T), goto_succeeds(T).
at(robot, CurrentPos, s(T)) :- do(goto(_), T), goto_fails(T), at(robot, CurrentPos, T).
at(robot, CurrentPos, s(T)) :- \+ goto_action(T), at(robot, CurrentPos, T).
at(key, Pos, T) :- carrying(key, T), at(robot, Pos, T).
at(key, Pos, s(T)) :- \+ carrying(key, s(T)), at(key, Pos, T).
0.9::goto_succeeds(T); 0.1::goto_fails(T).
 
goto_action(T) :-
 do(goto(Pos),T).
 
do(goto(loc1),0).
do(pickup(key),s(0)).
do(goto(loc2),s(0)).
at(key,loc1,0).
at(robot,loc0,0).
 
query(carrying(key,s(s(s(0))))).
query(at(_,_,s(s(s(0))))).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. It maintains all the original logic and probabilistic rules while slightly reformatting some clauses for better readability. The running results of both codes are identical, indicating that the generated code preserves the semantic meaning of the original.
*/