PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
CNT1 is CNT - 1,
    (coin(CNT), SC1 is SC + 1, coins_r(SC1, S, CNT1) ; 
     \+ coin(CNT), coins_r(SC, S, CNT1))
.
total(S) :- coins_r(0,S,4).
query(total(_)).
/* %%% Result %%% 
% Problog Inference Result：
total(4) = 0.4096
total(3) = 0.4096
total(2) = 0.1536
total(1) = 0.0256
total(0) = 0.0016
*/