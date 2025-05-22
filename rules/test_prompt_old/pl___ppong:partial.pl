person(alice).
person(bob).
langda(LLM:"define player carla").
person(dan).

game(g1).
langda(LLM:"second game").
langda(LLM:"third game").
game(g4).

0.28::strength(P,10); 0.2::strength(P,8); 0.2::strength(P,12); 0.1::strength(P,6); 0.1::strength(P,14); 0.05::strength(P,4); 0.05::strength(P,16); 0.01::strength(P,2); 0.01::strength(P,18) :- person(P).
0.1::lazy(P,G) :- person(P),game(G).

strength(P,G,S) :- lazy(P,G), strength(P,RS), S is RS/2.
strength(P,G,S) :- \+lazy(P,G), strength(P,S).

team_strength([P],G,S) :- langda(LLM:"Single team: Team strength is the strength of the member in the game").
team_strength([P,P2|L],G,S) :-
     langda(LLM:"Multiplayer team: The team strength is the 'minimum' of all members' strengths.").
min(A,B,C) :- C is min(A,B).

wins(T1,T2,G,T1) :-
     langda(LLM:"team1 win if they have higher team strength").
wins(T1,T2,G,T2) :-
     \+wins(T1,T2,G,T1).

evidence(wins([alice],[bob],g1,[alice]),true).
evidence(wins([bob],[carla],g2,[carla]),true).
evidence(wins([bob],[dan],g3,[dan]),true).
evidence(lazy(bob,g1),true).
query(wins([carla,alice],[bob,dan],g4,_)).