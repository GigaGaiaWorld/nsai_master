person(alice).
person(bob).
person(carla).
person(dan).
game(g1).
game(g2).
game(g3).
game(g4).
0.28::strength(P,10); 0.2::strength(P,8); 0.2::strength(P,12); 0.1::strength(P,6); 0.1::strength(P,14); 0.05::strength(P,4); 0.05::strength(P,16); 0.01::strength(P,2); 0.01::strength(P,18) :- person(P).
0.1::lazy(P,G) :- person(P),game(G).
strength(P,G,S) :- lazy(P,G), strength(P,RS), S is RS/2.
strength(P,G,S) :- \+lazy(P,G), strength(P,S).
team_strength([P],G,S) :- 
 strength(P,G,S).
team_strength([P,P2|L],G,S) :-
 
 strength(P,G,S1), team_strength([P2|L],G,S2), min(S1,S2,S).
min(A,B,C) :- C is min(A,B).
wins(T1,T2,G,T1) :-
 
 team_strength(T1,G,S1), team_strength(T2,G,S2), S1 > S2.
wins(T1,T2,G,T2) :-
 \+wins(T1,T2,G,T1).
evidence(wins([alice],[bob],g1,[alice]),true).
evidence(wins([bob],[carla],g2,[carla]),true).
evidence(wins([bob],[dan],g3,[dan]),true).
evidence(lazy(bob,g1),true).
query(wins([carla,alice],[bob,dan],g4,_)).

*** Result:*** 
% Problog Inference Result：
wins([carla, alice],[bob, dan],g4,[carla, alice]) = 0.5462
wins([carla, alice],[bob, dan],g4,[bob, dan]) = 0.4538 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality and logic. The only differences are minor formatting changes, such as line breaks and spacing, which do not affect the code's execution or results. The generated code maintains all the original rules, facts, and probabilistic distributions, and the query and evidence statements are identical. The running results of both pieces of code are exactly the same, confirming their equivalence.