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

langda(LLM:"please define the game rules of rock-paper-scissors.").

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

% Predicted results by DeepSeek:
% result1: determine_winner([rock,rock,rock],[paper,paper,scissor],player2)
result2: query(determine_winner([rock,rock,rock],[paper,paper,scissor],player2))

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code correctly implements the rock-paper-scissors game rules and includes a scoring mechanism to determine the winner. It defines the basic moves and their win-lose relationships, similar to the original code. However, the generated code is more detailed, including a compute_score predicate and a determine_winner predicate that uses these scores to decide the winner. The running results of both codes are consistent, correctly identifying player2 as the winner for the given moves. The generated code is valid and meets the requirements, though it includes additional predicates not present in the original code.
*/