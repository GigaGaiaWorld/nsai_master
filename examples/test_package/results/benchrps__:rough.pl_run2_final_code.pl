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
play_round(Move1, Move2, Result) :- beats(Move1, Move2), Result = win ; beats(Move2, Move1), Result = lose ; Move1 = Move2, Result = draw.
play([], [], []).
play([Move1 | Rest1], [Move2 | Rest2], [Result | Results]) :- play_round(Move1, Move2, Result), play(Rest1, Rest2, Results).
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
/* %%% Result %%% 
% Problog Inference Result：
determine_winner([rock, rock, rock],[paper, paper, scissor],player2) = 1.0000
*/