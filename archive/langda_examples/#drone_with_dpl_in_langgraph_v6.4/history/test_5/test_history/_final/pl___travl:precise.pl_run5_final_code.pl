person(a).
person(b).
0.1::initialInf(X) :- person(X).
0.1::contact(X,Y) :- person(X), person(Y).
0.1::riskyTravel(X) :- person(X).
0.1::susceptible(X) :- person(X).
0.6::inf(X) :- contact(X,Y), inf(Y), \+susceptible(X).
0.8::inf(X) :- contact(X,Y), inf(Y), susceptible(X).
0.2::inf(X) :- riskyTravel(X).
inf(X) :- initialInf(X).
query(inf(_)).

*** Result:*** 
% Problog Inference Result：
inf(a) = 0.1245
inf(b) = 0.1245 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. Both codes define the same probabilistic rules and facts, with only minor syntactic differences (e.g., spacing and order of rules). The generated code maintains the same logic and produces identical results when queried. There are no functional or logical discrepancies between the two versions.