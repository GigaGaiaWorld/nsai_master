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
% Play a single round and determine the outcome
play([], [], []).
play([P1|P1Moves], [P2|P2Moves], [Result|Results]) :-
    (beats(P1, P2), Result = win;
    beats(P2, P1), Result = lose;
    Result = draw),
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

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is mostly consistent with the original code in terms of functionality but has a critical issue in the 'play' predicate. The original code correctly uses separate clauses for 'result' to determine the outcome, while the generated code uses a disjunction (;) within a single clause, which leads to incorrect multiple results. This causes the generated code to produce multiple, conflicting outcomes (player2, draw, player1) for the same input, which is incorrect. The original code correctly produces a single, deterministic result.
*/