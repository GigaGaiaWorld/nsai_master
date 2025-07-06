PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
(coin(CNT), NewSC is SC + 1, NewCNT is CNT - 1, coins_r(NewSC,S,NewCNT)
    ;
    \+coin(CNT), NewCNT is CNT - 1, coins_r(SC,S,NewCNT))
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