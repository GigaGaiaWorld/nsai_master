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
% Same gestures are considered a draw
result(X, X, draw) :-
 move(X).
 
% If X beats Y, then X wins
result(X, Y, win) :-
beats(X, Y).
% If Y beats X, then X loses
result(X, Y, lose) :-
beats(Y, X).
 
% End of recursion: empty list corresponds to empty result
play([], [], []).
% Recursive advancement: take out each round of gestures, calculate the results, and continue
play([P1|P1T], [P2|P2T], [R|Rs]) :-
% The correct call is result(P1,P2,R), not semicolon
result(P1, P2, R),
% (Optional) Update the score according to R
play(P1T, P2T, Rs).
 
compute_score([], 0).
compute_score([win | Rs], S) :- compute_score(Rs, S1), S is S1 + 1.
compute_score([lose | Rs], S) :- compute_score(Rs, S1), S is S1 - 1.
play(P1Moves, P2Moves, Results),
compute_score(Results, Score),
(Score > 0 -> Winner = player1 ;
 Score < 0 -> Winner = player2 ;
 Winner = draw).
compute_score([draw | Rs], S) :- compute_score(Rs, S1), S is S1.
determine_winner(P1Moves,P2Moves,Winner) :- 
 
play(P1Moves, P2Moves, Results),
compute_score(Results, Score),
(Score > 0, Winner = player1 ;
 Score < 0, Winner = player2 ;
 Score =:= 0, Winner = draw).
query(determine_winner([rock,rock,rock],[paper,paper,scissor],W)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code has several issues. First, there is a misplaced clause 'play(P1Moves, P2Moves, Results), compute_score(Results, Score), (Score > 0 -> Winner = player1 ; Score < 0 -> Winner = player2 ; Winner = draw).' that appears before the 'determine_winner' predicate, causing a grounding error. Second, the 'determine_winner' predicate in the generated code uses '=:=' for equality comparison instead of '=' as in the original code, which is syntactically correct but stylistically different. The generated code fails to run due to the misplaced clause, while the original code runs successfully and produces the correct result.
*/