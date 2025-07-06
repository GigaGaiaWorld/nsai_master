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
langda(LLM:"If the result of the current round is lose:
Recursively calculate the remaining result score S1
The current total score S is S1 - 1, which means adding one point to player2").
langda(LLM:"If the current round is draw:
A draw does not affect the score, and the previous round score S1 is directly passed.").

compute_score([draw | Rs], S) :- compute_score(Rs, S1), S is S1.

determine_winner(P1Moves,P2Moves,Winner) :- 
    langda(LLM:"Main predicate: Given two player action lists P1Moves and P2Moves, calculate the winner Winner.
    Firstly, call the play/3 rule to compare the two players' actions.
    Then, generate a Results list containing whether each round is win, lose, or draw").

query(determine_winner([rock,rock,rock],[paper,paper,scissor],W)).

% Predicted results by DeepSeek:
% result1: determine_winner([rock,rock,rock],[paper,paper,scissor],player2)
result2: W = player2

/* Result Report:
Validity_form: False
Validity_result: True
Report: The generated code correctly implements the rock-paper-scissors game logic, including move definitions, win/lose/draw conditions, and score calculation. It is consistent with the original code's functionality. However, the generated code contains some placeholder text ('langda(LLM:...)') which should be replaced with actual Prolog rules for complete validity. The running results of both codes are consistent, correctly identifying player2 as the winner for the given moves.
*/