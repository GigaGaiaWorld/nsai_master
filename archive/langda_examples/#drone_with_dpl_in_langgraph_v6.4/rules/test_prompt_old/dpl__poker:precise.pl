:-use_module(library(lists)).

0.25::house_rank(jack); 0.25::house_rank(queen); 0.25::house_rank(king); 0.25::house_rank(ace).

rank(jack_card,jack).
rank(queen_card,queen).
rank(king_card,king).
rank(ace_card,ace).

hand(Cards,straight(low)) :-
    member(card(jack),Cards),
    member(card(queen),Cards),
    member(card(king),Cards).
hand(Cards,straight(high)) :- 
    member(card(queen),Cards),
    member(card(king),Cards),
    member(card(ace),Cards).
hand([card(R), card(R), card(R)],threeofakind(R)).
hand(Cards,pair(R)) :-
    select(card(R),Cards,Cards2),
    member(card(R),Cards2).
hand(Cards,high(R)) :-
    member(card(R),Cards).
hand_rank(high(jack),0).
hand_rank(high(queen),1).
hand_rank(high(king),2).
hand_rank(high(ace),3).
hand_rank(pair(jack),4).
hand_rank(pair(queen),5).
hand_rank(pair(king),6).
hand_rank(pair(ace),7).
hand_rank(threeofakind(jack),8).
hand_rank(threeofakind(queen),9).
hand_rank(threeofakind(king),10).
hand_rank(threeofakind(ace),11).
hand_rank(straight(low),12).
hand_rank(straight(high),13).
best_hand(Cards,H) :-
    hand(Cards,H),
    hand_rank(H,R),
    \+(hand(Cards,H2),hand_rank(H2,R2),R2>R).
best_hand_rank(Cards,R) :-
    hand(Cards,H),
    hand_rank(H,R),
    \+(hand(Cards,H2),hand_rank(H2,R2),R2>R).
outcome(R1,R2,win) :- R1 > R2.
outcome(R1,R2,loss) :- R1 < R2.
outcome(R,R,draw).
cards([C0,C1,_,_],own,House,[card(R1), card(R2), House]) :-
    rank(C0,R1),
    rank(C1,R2).
cards([_,_,C2,C3],opponent,House,[card(R1), card(R2), House]) :-
    rank(C2,R1),
    rank(C3,R2).

game(Cards,House,H1,H2) :-
    langda(LLM:"Based on the given Cards (four cards) and House (bottom card),
distribute the first two cards to the player (own), and the last two cards to the opponent (opponent),
calculate and return the respective optimal hand types H1 and H2.").
game(Cards,House,Outcome) :-
    langda(LLM:"Similar to the above, but only returns the result Outcome ∈ {win, loss, draw}, Determine the winner by comparing the rank values ​​of the player and opponent's best cards.").
game(Cards,Outcome) :-
    langda(LLM:"Without specifying House, a hole card is randomly drawn from the probability distribution house_rank/1, and then the above game/3 is called to return the final result.").

query(game([jack_card, queen_card, king_card, ace_card], Outcome)).