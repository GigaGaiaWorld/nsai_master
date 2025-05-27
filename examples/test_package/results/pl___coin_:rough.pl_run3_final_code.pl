PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
coin(c1),
    (coin(c1), NewSC is SC + 1 ; \+ coin(c1), NewSC is SC),
    NewCNT is CNT - 1,
    coins_r(NewSC,S,NewCNT).
total(S) :- coins_r(0,S,4).
query(total(_)).
/* %%% Result %%% 
% Problog Inference Result：
total(4) = 0.8000
*/