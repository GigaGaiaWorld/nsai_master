person(a).
person(b).

0.1::initialInf(X) :- person(X).
0.1::contact(X,Y) :- person(X), person(Y).
0.1::riskyTravel(X) :- person(X).
0.1::susceptible(X) :- person(X).

langda(LLM:"inf/1 predicate logic summary

Initial infection: Each person has a 0.1 probability of being infected at the beginning

Contact transmission: If X has contact with infected person Y, then

If X is not susceptible, he will be infected with a probability of 0.6

If X is susceptible, he will be infected with a probability of 0.8

Travel risk: Each person has an additional probability of 0.2 of infection due to high-risk travel").

query(inf(_)).