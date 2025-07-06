PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
coin(c1),
    (make_coin(c1, 0.8), SC1 is SC + 1 ; SC1 is SC),
    CNT1 is CNT - 1,
    coins_r(SC1, S, CNT1).
total(S) :- coins_r(0,S,4).
query(total(_)).
/* %%% Result %%% 
% Problog Inference Result：
total(4) = 0.8000
total(3) = 0.8000
total(2) = 0.8000
total(1) = 0.8000
total(0) = 0.8000
*/