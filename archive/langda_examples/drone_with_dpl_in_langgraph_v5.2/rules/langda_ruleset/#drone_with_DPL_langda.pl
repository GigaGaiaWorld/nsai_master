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
flight_assessment(FlightStatus, Obstacle1Img, Obstacle2Img) :-
    langda("The system then compares this risk score against a predefined safety threshold. If the risk score is below the threshold, the flight is considered viable and safe to proceed. If the risk score equals or exceeds the threshold, the flight is deemed unsafe or not viable. Finally, the system provides a simple way to check flight status through an assessment function that returns either a go (1) or no-go (0) decision.").
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