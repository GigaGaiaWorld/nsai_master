%================%================% Problog Part 1 %================%================%
% Basic rules and facts
1/10::weather_condition(clear); 9/10::weather_condition(challenging).

% Drone information
drone(alpha, civilian, image1, image2).  % DroneID, Type, Obstacle1Image, Obstacle2Image
drone(beta, civilian, image1, image2).
drone(gamma, military, image1, image2).
drone(delta, military, image1, image2).

0.7::threshold(9).
0.3::threshold(11).

% Additional capabilities assessment
0.8::has_advanced_sensors(alpha). 
0.2::has_advanced_sensors(beta).
0.6::has_advanced_sensors(gamma). 
0.4::has_advanced_sensors(delta).

%================%==================================================%================%
%================%==============% DeepProbLog Module %==============%================%
% Neural network for obstacle recognition
% nn(obstacle_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: event1(X,Y).
% nn(obstacle_net,[X],Y,[0,1,2,3,4,5,6,7,8,9]) :: event2(X,Y).

event1(image1,3).
event2(image2,7).
happenAt(image1,image2,1).

% Navigation module - uses recognized obstacles to calculate risk
navigation_risk(ImgX, ImgY, RiskScore) :-
    event1(ImgX, X),
    event2(ImgY, Y),
    happenAt(ImgX, ImgY, T), 
    RiskScore is X + Y.

% Module result predicates: pass
mission_viable(1, Obstacle1Img, Obstacle2Img) :-
    navigation_risk(Obstacle1Img, Obstacle2Img, Risk),
    threshold(X),
    Risk < X.
% Module result predicates: fail
mission_viable(0, Obstacle1Img, Obstacle2Img) :-
    navigation_risk(Obstacle1Img, Obstacle2Img, Risk),
    threshold(X),
    Risk >= X.

flight_assessment(FlightStatus, Obstacle1Img, Obstacle2Img) :-
    mission_viable(FlightStatus, Obstacle1Img, Obstacle2Img).
%================%==============% DeepProbLog Module %==============%================%
%================%==================================================%================%

%================%================% Problog Part 2 %================%================%
% Higher-level reasoning using neural network module results

% Drone classification
% Class A: Mission viable and has advanced sensors
classification(Drone, 'A') :-
    drone(Drone, _, O1, O2),
    flight_assessment(1, O1, O2),
    has_advanced_sensors(Drone).

% Class B: Mission viable but no advanced sensors OR not viable but has advanced sensors
classification(Drone, 'B') :-
    drone(Drone, _, O1, O2),
    flight_assessment(1, O1, O2),
    \+ has_advanced_sensors(Drone).
classification(Drone, 'B') :-
    drone(Drone, _, O1, O2),
    flight_assessment(0, O1, O2),
    has_advanced_sensors(Drone).

% Class C: Mission not viable and no advanced sensors
classification(Drone, 'C') :-
    drone(Drone, _, O1, O2),
    flight_assessment(0, O1, O2),
    \+ has_advanced_sensors(Drone).

query(classification(alpha, Class)).
query(classification(beta, Class)).
query(classification(gamma, Class)).
query(classification(delta, Class)).