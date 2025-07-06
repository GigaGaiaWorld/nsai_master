% UAV数据流和属性
initial_charge(Drone, C) :- drone(Drone), t(0.8)::c(Drone, C).
battery_drain_rate(Drone, R) :- drone(Drone), t(0.7)::r(Drone, R).
drone_weight(Drone, W) :- drone(Drone), t(0.6)::w(Drone, W).

% 天气条件（随时间变化的事件）
0.2::weather(T, fog); 0.8::weather(T, clear) :- time(T).

% =============================================================== %
% DeepProbCEP模块：使用神经网络检测位置和障碍物
nn(position_net, [X, T], Y, [safe, warning, danger]) :: position_status(X, T, Y).
nn(obstacle_net, [X, T], Y, [none, static, moving]) :: obstacle_detected(X, T, Y).

% 根据时间序列事件定义的复杂事件模式
flight_path_clear(Drone, T) :-
    position_status(Drone, T, safe),
    obstacle_detected(Drone, T, none),
    weather(T, clear).

flight_path_caution(Drone, T) :-
    position_status(Drone, T, warning);
    obstacle_detected(Drone, T, static);
    weather(T, fog).

flight_path_danger(Drone, T) :-
    position_status(Drone, T, danger);
    obstacle_detected(Drone, T, moving).

% 复杂事件检测：危险状态持续
initiatedAt(danger_state = true, T) :-
    flight_path_danger(Drone, T),
    flight_path_danger(Drone, Tprev),
    previousTimeStamp(T, Timestamps, Tprev).

valid_drone_flight(danger_state = true, T) :-
    initiatedAt(danger_state = true, Tprev),
    \+ broken(danger_state = true, Tprev, T).
% =============================================================== %

% 定义视线范围（VLOS）规则
vlos(Drone, T) :- 
    weather(T, clear), distance(Drone, operator, T, D), D < 100;
    weather(T, fog), distance(Drone, operator, T, D), D < 50.

% 电池电量预测
battery_remaining(Drone, T, R) :-
    initial_charge(Drone, I),
    battery_drain_rate(Drone, Rate),
    time_elapsed(0, T, Hours),
    R is I - (Rate * Hours).

% 定义安全返航条件
can_return_safely(Drone, T) :- 
    battery_remaining(Drone, T, B),
    distance(Drone, operator, T, D),
    B > D * 0.2.  % 简单假设：返航需要20%的电量/距离单位

% 与外部系统的集成：授权和许可
authorized_zone(Drone, T) :-
    zone_type(Drone, T, residential), drone_weight(Drone, W), W < 0.25;
    zone_type(Drone, T, commercial), have_permit(Drone, commercial);
    zone_type(Drone, T, industrial), have_permit(Drone, industrial).

% 最终决策规则
safe_flight(Drone, T) :-
    vlos(Drone, T),
    can_return_safely(Drone, T),
    \+ valid_drone_flight(danger_state = true, T),
    authorized_zone(Drone, T).

emergency_landing_required(Drone, T) :-
    valid_drone_flight(danger_state = true, T);
    battery_remaining(Drone, T, B), B < 15;  % 低于15%电量需要紧急着陆
    \+ vlos(Drone, T).