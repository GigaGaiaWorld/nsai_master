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
play([], [], []).
play([P1 | P1Moves], [P2 | P2Moves], [Result | Results]) :-
    ( beats(P1, P2) -> Result = win
    ; (beats(P2, P1) -> Result = lose
    ; Result = draw
    ),
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
Report: The generated code attempts to replicate the functionality of the original code but contains a syntax error due to an unmatched parenthesis in the conditional statement within the 'play' predicate. This error prevents the code from being valid and executable. The original code correctly uses separate clauses for each result condition, while the generated code tries to use nested conditionals with -> operators, which leads to the syntax error. The logic of both codes is intended to be the same, but the generated code fails to execute due to its invalid form.
*/