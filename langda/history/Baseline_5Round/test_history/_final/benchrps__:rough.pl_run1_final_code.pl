% -------------------------
% Basic rules of rock-paper-scissors
% -------------------------

% Three gestures
move(rock).
move(paper).
move(scissor).

% Win-lose relationship: X beats Y
beats(rock, scissor).
beats(scissor, paper).
beats(paper, rock).

% -------------------------
% Calculate the result of the game
% -------------------------

% Play a single round
play_round(M1, M2, Result) :-
    (beats(M1, M2) -> Result = win;
     beats(M2, M1) -> Result = lose;
     Result = draw).

% Play multiple rounds
play([], [], []).
play([M1|P1Moves], [M2|P2Moves], [Result|Results]) :-
    play_round(M1, M2, Result),
    play(P1Moves, P2Moves, Results).

compute_score([], 0).
compute_score([win | Rs], S) :- compute_score(Rs, S1), S is S1 + 1.
compute_score([lose | Rs], S) :- compute_score(Rs, S1), S is S1 - 1.
compute_score([draw | Rs], S) :- compute_score(Rs, S1), S is S1.

determine_winner(P1Moves,P2Moves,Winner) :- 
    play(P1Moves,P2Moves,Results), 
    compute_score(Results,S), 
    ( S > 0, Winner = player1 
    ; S < 0, Winner = player2 
    ; S = 0, Winner = draw 
    ).

query(determine_winner([rock,rock,rock],[paper,paper,scissor],W)).




*** Result:*** 
Error evaluating Problog model:
    return exec_func(node_id=node_id, node=node, **kwdargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/engine_stack.py", line 839, in eval_call
    raise UnknownClause(origin, location=loc)
problog.engine.UnknownClause: No clauses found for ''->'/2' at 21:20. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to simplify the original logic by introducing a 'play_round' predicate with conditional statements. However, it contains a syntax error in the conditional operator '->' which is not properly formatted for Prolog, leading to a runtime error. The original code correctly uses separate clauses for each game outcome, while the generated code's approach is conceptually similar but incorrectly implemented. Both codes aim to achieve the same functionality of determining the winner in a rock-paper-scissors game, but the generated code fails to execute due to syntax issues.