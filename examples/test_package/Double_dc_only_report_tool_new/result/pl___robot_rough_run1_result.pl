% source: David Poole. Abducing through negation as failure: stable models within the independent choice logic. JLP 2000.
carrying(key,s(T)) :-
 
    do(pickup(key),T),    pickup_succeeds(T).
carrying(key,s(T)) :-
 
    carrying(key,T),    \+ drops(key,T).
 
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
 
at(robot,Pos,s(T)) :-    goto_action(T),    do(goto(Pos),T),    goto_succeeds(T).at(robot,Pos,s(T)) :-    \+ goto_action(T),    at(robot,Pos,T).
at(key,Pos,T) :-
 carrying(key,T),
 at(robot,Pos,T).
at(key,Pos,s(T)) :-
 \+ carrying(key,s(T)),
 at(key,Pos,T).
 
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
Validity_form: False
Validity_result: False
Report: The generated code is not valid due to syntax errors, specifically an unexpected character '.' at line 30:81. This error prevents the code from running successfully. The generated code also differs from the original in several ways: it removes the 'at(robot,Pos,T)' condition in the first carrying rule and simplifies the second carrying rule by removing some conditions. These changes make the generated code inconsistent with the original logic.
*/