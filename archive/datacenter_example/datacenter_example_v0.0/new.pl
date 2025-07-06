:- use_module('in_out.py').

% nn predicates that convert features into probabilities:
nn(temp_net, [Mean_value], Temp_an, [0, 1])::temp_data(Mean_value, Temp_an).
% nn(cpul_net, [Mean_value], Temp_an, [no_anomaly, anomaly])::cpul_data(Mean_value, Temp_an).

% event_temperature_exceed(Temp) :- 
%     temp_data(Temp, anomaly).

% event_cpuload_high(CPU_load) :- 
%     cpul_data(CPU_load, anomaly).

% anomaly(Temp, CPU_load, anomaly) :- 
%     event_temperature_exceed(Temp).

% anomaly(Temp, CPU_load, anomaly) :- 
%     event_cpuload_high(CPU_load).

% anomaly(_, _, no_anomaly).
% t(0.8)::anomaly(Temp, CPUl, R) :- 
%     temp_data(Temp, R1),
%     cpul_data(CPUl, R2),
%     R = R1 * R2.

t(_)::anomaly(Temp, R) :- 
    temp_data(Temp, R1),
    R is R1.

query(anomaly(_, no_anomaly)).