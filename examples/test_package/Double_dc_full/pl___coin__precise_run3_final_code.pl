PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
coin(CNT),
    CNT1 is CNT - 1,
    coins_r(SC1, S, CNT1),
    SC = SC1 + 1.
total(S) :- coins_r(0,S,4).
query(total(_)).
/* %%% Result %%% 
% Problog Inference Result：
total(X2) = 0.0000
*/