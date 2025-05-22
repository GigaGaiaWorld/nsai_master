langda("Express a safe drone flight condition.", chatgpt).

langda(NLP_String, Model).

% =============================== % EXAMPLE % =============================== %
% UAV properties
initial_charge ~ normal(90, 5).
charge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

langda("nothing").

% Sufficient charge to return to operator
can_return(X) :- 
    B is initial_charge, O is charge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

valid_drone_flight(X) :-
    langda("there's a high building at (100,200)",chatgpt), vlos(X).


% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).







==================new_lines_train==================
nn(mnist_net1,[X],0)::event1(X,0); nn(mnist_net1,[X],1)::event1(X,1).
nn(mnist_net2,[X],2)::event2(X,2); nn(mnist_net2,[X],3)::event2(X,3). 

===================new_lines_test=================== 
nn(mnist_net1,[X],Y)::event1(X,Y) :- mnist_net1(X,Y).
nn(mnist_net2,[X],Y)::event2(X,Y) :- mnist_net2(X,Y).

===================original_model===================
% Define coin1 and coin2 to extract event information
coin1(ID1, T) :-
    happensAt(X, Y, T), 
    event1(X, ID1).

coin2(ID2, T) :-
    happensAt(X, Y, T), 
    event2(Y, ID2).

% Define the event table mapping event combinations to event IDs
event_table(ID1, ID2, 0) :- ID1 = 0, ID2 = 2.
event_table(ID1, ID2, 1) :- ID1 = 0, ID2 = 3.
event_table(ID1, ID2, 2) :- ID1 = 1, ID2 = 2.
event_table(ID1, ID2, 3) :- ID1 = 1, ID2 = 3.

% Define detectEvent to detect events at specific timestamps
detectEvent(EventID, T) :-
    coin1(ID1, T),
    coin2(ID2, T),
    event_table(ID1, ID2, EventID).

%================%================%================%================%
% 如果 detectEvent 得到的 EventID 为0或3，则 win=1
result(win=1, T) :-
    detectEvent(EventID, T),
    (EventID = 0 ; EventID = 3).

% 如果 detectEvent 得到的 EventID 为1或2，则 win=0
result(win=0, T) :-
    detectEvent(EventID, T),
    (EventID = 1 ; EventID = 2).
%================%================%================%================%

happensAt(1218,1742, 0).
happensAt(1203,795, 1).
happensAt(750,216, 2).
happensAt(1434,1696, 3).
happensAt(663,883, 4).
happensAt(1987,500, 5).
happensAt(1408,1463, 6).
happensAt(28,1336, 7).
happensAt(365,1036, 8).
happensAt(1630,1127, 9).
happensAt(388,225, 10).
happensAt(342,1365, 11).
--------...--------
