% source: David Poole. Abducing through negation as failure: stable models within the independent choice logic. JLP 2000.
carrying(key,s(T)) :-
 
do(pickup(key),T), pickup_succeeds(T), at(key,Pos,T), at(robot,Pos,T)
.
carrying(key,s(T)) :-
 
carrying(key,T), retains_key(T)
.
 
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
 
at(robot,NewPos,s(T)) :- goto_action(T), goto_succeeds(T), do(goto(NewPos),T), at(robot,_,T).
at(robot,Pos,s(T)) :- goto_action(T), goto_fails(T), at(robot,Pos,T).
at(robot,Pos,s(T)) :-
 \+ goto_action(T),
 at(robot,Pos,T).
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
Validity_form: True
Validity_result: False
Report: The generated code simplifies the original conditions for carrying the key, particularly in the second clause where it directly uses 'retains_key(T)' instead of checking multiple negative conditions. This change alters the logic and leads to a different probability result for 'carrying(key,s(s(s(0))))' (0.5040 vs 0.4331). The rest of the code and results remain consistent with the original, indicating partial correctness but with a significant logical deviation in the carrying predicate.
*/