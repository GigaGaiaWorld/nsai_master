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
outcome(P1Move, P2Move, win) :- beats(P1Move, P2Move).
outcome(P1Move, P2Move, lose) :- beats(P2Move, P1Move).
outcome(Move, Move, draw).

play([], [], []).
play([P1Move | P1Moves], [P2Move | P2Moves], [Result | Results]) :-
    outcome(P1Move, P2Move, Result),
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
Report: The generated code is correct and consistent with the original code in terms of functionality. It correctly implements the rock-paper-scissors game rules and computes the winner based on the moves provided. The main difference is the use of 'outcome/3' predicate in the generated code instead of 'result/3' in the original code, but both serve the same purpose and produce identical results. The generated code is valid and meets the requirements.
*/