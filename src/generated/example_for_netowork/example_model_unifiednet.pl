feature_all(Features) :-
    % 直接提取原始数值
    sensor_data(sensor_KMS1, temperature, _, _, _, Temp_KMS1, _, _, _, _),
    sensor_data(sensor_cpu, cpuload, _, _, _, Cpu, _, _, _, _),
    sensor_data(sensor_weather, humidity, _, _, _, Humidity, _, _, _, _),
    sensor_data(sensor_weather, temperature, _, _, _, Temp_weather, _, _, _, _),

    Diff is abs(Temp_KMS1 - Temp_weather),
    % create binary features based on rules:
    (Temp > 26 -> TempExceed = 1 ; TempExceed = 0),
    (Cpu > 0.75 -> CpuHigh = 1 ; CpuHigh = 0),
    (Temp < 24 -> TempLow = 1 ; TempLow = 0),
    (Humidity > 0.85 -> HumidityHigh = 1 ; HumidityHigh = 0),
    (Diff > 2.0 -> DiffLarge = 1 ; DiffLarge = 0),
    % feature vector.
    Features = [Temp, Cpu, Humidity, Temp2, Diff, TempExceed, CpuHigh, TempLow, HumidityHigh, DiffLarge].


nn(all_net, [feature_all(Features)], [Overheat, Condensation, HighPower], [yes, no])
:: anomaly(all, [overheat_risk(Overheat), condensation_risk(Condensation), high_power_consumption(HighPower)]).
