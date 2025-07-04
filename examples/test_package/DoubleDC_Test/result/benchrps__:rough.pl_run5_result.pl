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
play_round(P1, P2, Result) :- beats(P1, P2), Result = win ; beats(P2, P1), Result = lose ; P1 = P2, Result = draw.
play([], [], []).
play([P1|P1s], [P2|P2s], [Result|Results]) :- play_round(P1, P2, Result), play(P1s, P2s, Results).
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
Report: The generated code is correct and consistent with the original code in terms of functionality. It simplifies the result calculation by combining the three possible outcomes (win, lose, draw) into a single predicate 'play_round', which is more concise. The logic for computing the score and determining the winner remains unchanged. Both codes produce the same result for the given query, indicating that the generated code meets the expectations.
*/