% member/2 for ProbLog
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% --------- Basic meta-interpreter ---------
% Prove "true" always succeeds
prove(true).

prove(Goal) :-
    % For all other goals, use the clause/2 facts/rules defined in the program
    clause(Goal, Body),
    prove(Body).

% Prove compound goal A,B: prove A first, then prove B
prove((A,B)) :-
    prove(A),
    prove(B).

% --------- Extended logic processing ---------
% 1. implies/2 - succeeds if the consequent is true when the antecedent is true
prove(implies(Antecedent, Consequent)) :-
    prove(Antecedent),
    prove(Consequent).

% 2. opposite/1 - succeeds if the negated statement cannot be proven
prove(opposite(Statement)) :-
    \+ prove(Statement).

% 3. expand/2 - uses already defined rules to transform input to output
prove(expand(Input, Output)) :-
    expand(Input, Output).

% 4. includes/2 - succeeds if the element is a member of the list
prove(includes(List, Elem)) :-
    member(Elem, List).

% 5. extend/2 - adds element to the head of a list
prove(extend(List, Elem, Extended)) :-
    Extended = [Elem|List].

% 6. refute/1 - succeeds if the statement cannot be proven
prove(refute(Statement)) :-
    \+ prove(Statement).

% --------- Examples ---------- %
% Define some expand rules:
expand(double(X), Y) :- Y is X*2.
expand(square(X), Y) :- Y is X*X.

parent(alice, bob).
parent(bob, carol).

ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y).

% --------- Queries ---------- %
query(prove(implies(parent(alice,bob), ancestor(alice,bob)))).
query(prove(opposite(parent(carol,alice)))).
query(prove(expand(double(3),6))).
query(prove(includes([a,b,c],b))).
query(prove(extend([1,2],3,[3,1,2]))).




*** Result:*** 
% Problog Inference Result：
prove(implies(parent(alice,bob),ancestor(alice,bob))) = 1.0000
prove(opposite(parent(carol,alice))) = 1.0000
prove(expand(double(3),6)) = 1.0000
prove(includes([a, b, c],b)) = 1.0000
prove(extend([1, 2],3,[3, 1, 2])) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is mostly correct and consistent with the original code. However, there is a significant difference in the implementation of the 'implies/2' predicate. The original code succeeds if the antecedent is unprovable or the consequent is provable, while the generated code requires both the antecedent and consequent to be provable. This change alters the logical meaning of 'implies'. Despite this difference, the running results are consistent for the given queries because the specific test cases happen to satisfy both implementations.