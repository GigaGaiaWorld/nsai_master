% =============================== % EXAMPLE % =============================== %
lann(mnist_net1:"decrib net1",[M]:"describe M",N,[0,1,"None"]:"desc someting") :: event1(M,N). % lann(what?)
lann(mnist_net2,[X],Y:"what is Y?",[2,3,"dog","horn"]:"output 2 and 3")    % (what_is_this(X,S):maybe?
:: funfunf(X,Y).     % have fun here)!

lann(mnist_net3:"wah?",       % net work haha
[R],S:"what whatwhaitsat?",     % X and what Y: this Y! stop, lann(X,Y)
["this","thas","was","isss"]:"outoutoutout")    % (what_e q2wre g wads  cf :: event114(X,Y).
:: digit232(R,S).     % have fun here)!


% UAV properties
initial_langda_content[i]ge ~ normal(90, 5).
langda_content[i]ge_cost ~ normal(-0.1, 0.2).
weight ~ normal(0.2, 0.1).

% Weather conditions
1/10::fog; 9/10::clear.

% Visual line of sight
vlos(X) :- 
    fog, distance(X, operator) < 50;
    clear, distance(X, operator) < 100;
    clear, over(X, bay), distance(X, operator) < 400.

langda(ans:"answer",LLM:"nothing"). % langda(LLM:"this is me").
% langda(X:"answer",LLM). % stop it
langda(why:"answer",NET:"[mlp(1,2,3,4,5,6)]").
langda(X).
/*
% Sufficient langda_content[i]ge to return to operator
can_return(X) :- 
    B is initial_langda_content[i]ge, O is langda_content[i]ge_cost,
    D is distance(X, operator), 0 < B + (2 * O * D), langda(LLM:"how about this?")
*/ langda(NET:"[no(1,2,3)]",LLM:"This is crazy")        .       waht_coin(sdaw,A) :- zzz(X;Y),
langda(LLM,NET).

% Permits related to local features
permits(X) :- 
    distance(X, service) < 15; distance(X, primary) < 15;
    distance(X, secondary) < 10; distance(X, tertiary) < 5;
    distance(X, crossing) < 5; distance(X, rail) < 5;
    over(X, park).

valid_drone_flight(X) :- (langda(X:"Return",T,LLM:"there's a high building at: (100,200)",NET:"[mnist_net1(0,1), mnist_net2(2,3)]",), vlos(X));(can_return(X));langda(T:"anstimewer",NET).

coin_win() :-
    % the code need to be clean!
    langda(X:"return", T:"time", NET:"[mnist_net1(0,1), mnist_net2(2,3)]",              % a langda code for new stuff
    LLM:"If the code difference is 2, it returns 1, otherwise it returns 0.")          % we use deepseek here!
    ,permits(X), langda(X:"return", Y:"fun", Z:"darmstadt", NET:"[position_net(there,here), audio(dog,child,horn)]",     % nothing useful % so quit!
    LLM:"If the we is 2,            % comment end
    and horn is there, we eat banana."). coin_this(X,Y,3) :- langda(X,LLM:"asdasda"),       % comment conisthis

    predicate(sd, X), asd(MMMA)
    . 

% Definition of a valid mission
landscape(X) :- 
    vlos(X), weight < 25, can_return(X); 
    permits(X), can_return(X).