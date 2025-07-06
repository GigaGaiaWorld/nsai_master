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
play_round(P1, P2, win) :- beats(P1, P2).
play_round(P1, P2, lose) :- beats(P2, P1).
play_round(_, _, draw).

play([], [], []).
play([P1|P1Moves], [P2|P2Moves], [Result|Results]) :-
    play_round(P1, P2, Result),
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
/* %%% Result %%% 
% Problog Inference Result：
determine_winner([rock, rock, rock],[paper, paper, scissor],player2) = 1.0000
determine_winner([rock, rock, rock],[paper, paper, scissor],draw) = 1.0000
determine_winner([rock, rock, rock],[paper, paper, scissor],player1) = 1.0000
*/