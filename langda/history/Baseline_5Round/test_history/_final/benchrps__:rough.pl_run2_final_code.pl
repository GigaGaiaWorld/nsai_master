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
% Game play rules
% -------------------------

% Play a single round
play_round(M1, M2, Result) :-
    (beats(M1, M2) -> Result = win;
    (beats(M2, M1) -> Result = lose;
    Result = draw).

% Play multiple rounds
play([], [], []).
play([M1|T1], [M2|T2], [R|Rs]) :-
    play_round(M1, M2, R),
    play(T1, T2, Rs).

% -------------------------
% Calculate the result of the game
% -------------------------

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
    return self.collapse(string, tokens)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1282, in collapse
    raise UnmatchedCharacter(string, expr_stack[-1].start.location)
problog.parser.UnmatchedCharacter: Unmatched character '(' at 21:5. 

***Report:***
Validity_form:False\Validity_result:False
The generated code attempts to replicate the functionality of the original code but introduces syntax errors in the 'play_round' predicate due to incorrect use of the '->' operator and parentheses. This makes the generated code invalid and unable to run. The original code correctly implements the rock-paper-scissors game logic without syntax errors and produces the expected result. The generated code's structure is similar but fails in execution due to these syntax issues.