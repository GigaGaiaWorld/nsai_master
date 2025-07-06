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
play_round(P1Move, P2Move, win) :- beats(P1Move, P2Move).
play_round(P1Move, P2Move, lose) :- beats(P2Move, P1Move).
play_round(Move, Move, draw).

% Play a sequence of moves and collect results
play([], [], []).
play([P1Move | P1Moves], [P2Move | P2Moves], [Result | Results]) :-
    play_round(P1Move, P2Move, Result),
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
% Problog Inference Result：
determine_winner([rock, rock, rock],[paper, paper, scissor],player2) = 1.0000 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code in terms of functionality. It simplifies the original code by combining the result calculation into a single predicate 'play_round' instead of using separate 'result' predicates. The logic remains the same, and the output is identical to the original code. The generated code meets the requirements and produces the same result as the original code.