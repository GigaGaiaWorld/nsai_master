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
implies(Antecedent, Consequent) :-
    prove(Antecedent),
    prove(Consequent).

% 2. opposite/1 - succeeds if the negated goal cannot be proven
opposite(Goal) :-
    \+ prove(Goal).

% 3. expand/2 - uses already defined rules to transform input to output
expand(Input, Output) :-
    clause(expand(Input, Output), _),
    call(expand(Input, Output)).

% 4. includes/2 - succeeds if the element is in the list
includes(List, Elem) :-
    member(Elem, List).

% 5. extend/2 - adds element to the head of a list
extend(List, Elem, NewList) :-
    NewList = [Elem|List].

% 6. refute/1 - succeeds if the goal cannot be proven
refute(Goal) :-
    \+ prove(Goal).

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
Error evaluating Problog model:
    term = queue.popleft()
           ^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/MASTERTHESIS/#Expert_System_Design/langda/utils/test_tools.py", line 17, in timeout_handler
    raise TimeoutError(f"Function timed out while processing file: {file_basename}")
TimeoutError: Function timed out while processing file: benchprove:rough.pl_run5 

***Report:***
Validity_form:False\Validity_result:False
The generated code has several issues. First, the 'implies' predicate is incorrectly defined; it should succeed if the antecedent is unprovable or the consequent is provable, not both. Second, the 'expand' predicate is redundantly defined and incorrectly uses 'clause' and 'call', which deviates from the original implementation. These changes affect the logic and functionality. The original code correctly implements the required logic, while the generated code does not. The timeout error in the result indicates that the generated code failed to execute properly, further confirming its invalidity.