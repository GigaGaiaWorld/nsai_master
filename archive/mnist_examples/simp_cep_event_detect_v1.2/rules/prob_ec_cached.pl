% :- use_module('examples/Energy/model/addition.py).
% % PROLOG-INDEPENDENT
% %=================我觉得这个方法有问题 I think it has some issue with timestamp=================%
% %===== holdsAt/2 谓词：状态持续 =====% 

% % 1. 在时间0时, aux为true
% holdsAt_(aux = true, 0).
% % 2. 状态从Tprev延续到T, 没有被打断
% holdsAt(F = V, T) :-                            % holdsAt(sequence0 = false, 13).   (GIVEN)
%   \+ sdFluent(F),                               % not sdFluent( aux ). ==> F != aux
%   T @> 0,                                       % 13 > 0
%   allTimeStamps(Timestamps),                    % allTimeStamps([...]),
%   previousTimeStamp(T, Timestamps, Tprev),      % previousTimeStamp(13, [...], 12),
%   holdsAt_(F = V, Tprev),                       % holdsAt_(sequence0 = false, 12).
%   \+ broken(F = V, Tprev, T).                   % not broken(sequence0 = false, 12, 13).
% % 3. 状态在Tprev时被初始化
% holdsAt(F = V, T) :-                            % holdsAt(sequence0 = false, 13).   (GIVEN)
%   \+ sdFluent(F),                               % not sdFluent( aux ). ==> F != aux
%   T @> 0,                                       % 13 > 0
%   allTimeStamps(Timestamps),                    % allTimeStamps([...]),
%   previousTimeStamp(T, Timestamps, Tprev),      % previousTimeStamp(16, [...], 12),
%   initAtDigit(F = V, Tprev).                    % initiatedAt(sequence0 = false, 12). => recurrent

% %===== broken/3 谓词：状态被中断的判断 =====% 
% % 1. T1到T2时间内, 状态F从V1变化成了V2
% broken(F = V1, T1, T2):-                        % broken(sequence0 = false, 12, 16). 
%   allTimeStamps(Timestamps),                    % allTimeStamps([...]),
%   previousTimeStamp(T2, Timestamps, T2prev),    % previousTimeStamp(16, [...], 12),
%   initAtDigit(F = V2, T2prev),                  % initiatedAt(sequence0 = true, 12),
%   V1 \= V2.                                     % false \= true.
% % 2. T1到T2时间内, 若存在其他时间戳, 递归
% broken(F = V, T1, T2) :-                        % broken(sequence0 = false, 12, 16). 
%   allTimeStamps(Timestamps),                    % allTimeStamps([...]),
%   previousTimeStamp(T2, Timestamps, T2prev),    % previousTimeStamp(16, [...], 12),
%   T2prev > T1,                                  % 12 > 12,
%   broken(F = V, T1, T2prev).                    % broken(sequence0 = false, 12, 12).

% previousTimeStamp(T, Timestamps, Tprev):- Tprev is T - 1.
% nextTimeStamp(T, Timestamps, Tnext):- Tnext is T + 1.