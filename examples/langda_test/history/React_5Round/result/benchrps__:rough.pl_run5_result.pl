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
% Play one round of the game
play([], [], []).
play([P1|P1s], [P2|P2s], [Result|Results]) :-
    (beats(P1, P2), Result = win
    ; beats(P2, P1), Result = lose
    ; \+ beats(P1, P2), \+ beats(P2, P1), Result = draw
    ),
    play(P1s, P2s, Results).
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
Report: The generated code is correct and consistent with the original code in terms of functionality. Both codes correctly implement the rock-paper-scissors game rules, calculate the results of each round, and determine the winner based on the accumulated score. The generated code simplifies the result calculation by combining the conditions for win, lose, and draw into a single clause within the play predicate, which is a valid approach. The running results of both codes are identical, confirming their equivalence.
*/