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
outcome(M1, M2, win) :- beats(M1, M2).
outcome(M1, M2, lose) :- beats(M2, M1).
outcome(M, M, draw).

play([], [], []).
play([M1 | P1Moves], [M2 | P2Moves], [R | Results]) :-
    outcome(M1, M2, R),
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
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code in terms of functionality. It simplifies the 'result' predicate into 'outcome' while maintaining the same logic for determining game results. Both codes produce identical results for the given query, correctly identifying player2 as the winner. The structure and logic of the generated code are valid and meet the requirements.
*/