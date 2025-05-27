%%% ============================================
%%% Drone Configurations
%%% ============================================
langda(LLM:"Please complete the following facts according to the model of drone: /* Drone */ .
% Battery capacity of each model (unit: Wh)
battery_capacity/1.
% Empty weight (kg)
empty_weight/1.
% Maximum payload (kg)
max_payload/1.
% Basic energy consumption rate (Wh/km) (no wind, no load)
base_consumption_rate/1.").

langda(LLM:" Current payload of the drone (kg): /* PayLoad */
    payload/1.
").

%%% ============================================
%%% Weather & Environmental Factors
%%% ============================================
% Real-time weather data:
langda(LLM:"Please get current weather data for city: /* City */ and return in format:
weather(Condition, WindSpeed, Temperature, Visibility).
Where:
- Condition: clear/cloudy/light_rain/heavy_rain
- WindSpeed: current wind speed in m/s
- Temperature: current temperature in Celsius").

%%% ============================================
%%% Energy Consumption Calculations
%%% ============================================
% Battery efficiency based on temperature
battery_efficiency(Efficiency) :-
    weather(_, _, Temp),
    (Temp < 0, Efficiency = 0.8; % Very cold
     Temp >= 0, Temp < 10, Efficiency = 0.85; % Cold
     Temp >= 10, Temp =< 35, Efficiency = 1.0; % Normal
     Temp > 35, Efficiency = 0.95 % Hot
    ).

%%% Energy Consumption
consumption_per_km(Rate) :-
    base_consumption_rate(Base),
    max_payload(MaxP),
    weather(_, WindSpeed, Temp, _),
    PayloadFactor is 1 + (payload / MaxP) * 0.5,
    WindFactor is 1 + WindSpeed / 25,
    battery_efficiency(Efficiency),
    Rate is Base * charge_cost * PayloadFactor * WindFactor / Efficiency.

%%% ============================================
%%% Battery and Power Management
%%% ============================================
%%% Battery Check
can_return(Dist_km) :-
    consumption_per_km(Rate),
    Energy is Rate * Dist_km * 2 * 1.2,  % 20% safety margin
    battery_capacity(Cap),
    Energy = Cap * 0.85.  % 15% reserve

%%% ============================================
%%% Airspace and Regulatory Constraints
%%% ============================================
%%% Weather Safety
weather_safe_for_flight :-
    weather(Condition, WindSpeed, _),
    safe_weather_condition(Condition),
    WindSpeed =< 15.  % Maximum safe wind speed

safe_weather_condition(clear).
safe_weather_condition(cloudy).
safe_weather_condition(light_rain).

% Definition of a valid mission
mission(Dist_km) :-
    Dist_km is 0, \+ weather_safe_for_flight;
    weather_safe_for_flight, can_return(Dist_km).