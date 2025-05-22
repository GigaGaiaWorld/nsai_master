% T: Text, Encoded: Encoded embeddings, R: Relation, Entity: the characters in the story.
:-use_module(library(lists)).
% get a relation from the embeddings "E", for the input embedding "E" it will implement a multiclass classification, 
% the output "Relation" will be selected from: "child, child_in_law..." (using nn)
nn(rel_extract, E, Relation,[child, child_in_law, parent, parent_in_law, sibling, sibling_in_law, grandparent, grandchild, nephew, uncle, so]) :: extract_relation(E,Relation).
% encoder, from the input text "Text" and two entities "Ent1" and "Ent2", it will get the output "Embeddings" vector. (using nn)
nn(encoder, [Text,Ent1,Ent2], Embeddings) :: encode(Text,Ent1,Ent2,Embeddings).
% from input text "Text" and entity "Entity" it will get the output "G" gender as "male or female"
nn(gender_net,[T,Entity],G,[male,female]) :: gender(T,Entity,G).


% generate symbolic fact from input data. (using nn)
get_edge(s(Entities,Text), Edge) :-
    % select a entity "E1" from the list of entities "Entities" and get the rest of the list of entities "Entities2" without "E1"
    select(E1,Entities,Entities2),
    % select a entity "E2" from the rest of list of entities "Entities2"
    member(E2,Entities2),
    % encode the input text "Text" and the selected entities "E1" and "E2" to get the encoded embeddings "Encoded"
    encode(Text,E1,E2,Encoded),
    % extract the relation from the encoded embeddings "Encoded" to get the output "Relation" (using nn)
    extract_relation(Encoded,Relation),
    % generate the symbolic fact "Edge" with the relation "Relation", the two selected entities "E1" and "E2", and the encoded embeddings "Encoded"
    Edge =.. [Relation,E1,E2]. % for example: grandparent(john,mary).


% use recursive functions to generate all the symbolic facts from the input data. (using nn)
get_edges( [Sentence|Others], [Edge|Edges]) :-
    get_edge(Sentence,Edge),
    get_edges(Others,Edges).

get_edges([], []).

% generate clutrr questions from the input data
clutrr_text(Entities, Text,X,R2,Y) :-
    gender_rel(R,G,R2), % basic gender relation
    gender(Text,Y,G), % get the gender of the second entity "Y" from the input text "Text" (using nn)
    get_edges(Text,Edges), % generate all symbolic facts from input data. (using nn)
    clutrr_edges(Entities,Edges,X,R,Y). % derive composite relations between X and Y from edges.

% 
clutrr_edges(Entities,Edges,X,R,Y) :-
    relation(R), % ensure the relation "R" is in the list of relations
    Goal =.. [R,X,Y], % create a goal with the relation "R" and the two entities "X" and "Y"
    rules(Rules), % get all the rules for the relation "R"
    forward(Edges,Rules, Goal). % get the composite relations between X and Y from the symbolic facts.

% a recursive function to get the composite relations between X and Y from the symbolic facts.
forward(Facts,Rules, Goal) :-  member(Goal,Facts). % check if the goal is in the list of facts.
% if the goal is not in the list of facts, then get the next facts from the rules with forward_step and call the forward function recursively.
forward(Facts,Rules, Goal) :- \+member(Goal,Facts),forward_step(Facts,Rules,NextFacts),forward(NextFacts,Rules,Goal).

% get the next facts from the rules.
forward_step(Facts,Rules, AllFacts) :-
% member(rule(Head, Body), Rules): transversal rule list, the form of each rule is rule(Head, Body), Head: conclusion of the rule, Body: premises of the rule.
% maplist([X]>>member(X,Facts), Body): For each sub-goal X in the rule body, check whether X is in the current set of facts.
% + member(Head, Facts): Make sure the conclusion of the rule, Head , is not already in Facts to avoid adding duplicate facts that already exist.
% findall(Head, ( ... ), [New|NewFacts]): Collect all Heads that meet the above conditions into a list
    findall(Head,(member(rule(Head, Body),Rules), maplist([X]>>member(X,Facts),Body), \+member(Head,Facts)), [New|NewFacts]),
    append([New|NewFacts],Facts,AllFacts).

% derive composite relations from the basic relations:
rule(grandchild(X,Y),  [child(X,Z), child(Z,Y)]).
rule(grandchild(X,Y),  [so(X,Z), grandchild(Z,Y)]).
rule(grandchild(X,Y),  [grandchild(X,Z), sibling(Z,Y)]).
rule(grandparent(X,Y),  [parent(X,Z), parent(Z,Y)]).
rule(grandparent(X,Y),  [sibling(X,Z), grandparent(Z,Y)]).
rule(child(X,Y),  [child(X,Z), sibling(Z,Y)]).
rule(child(X,Y),  [so(X,Z), child(Z,Y)]).
rule(parent(X,Y),  [sibling(X,Z), parent(Z,Y)]).
rule(parent(X,Y),  [child(X,Z), grandparent(Z,Y)]).
rule(sibling(X,Y),  [child(X,Z), uncle(Z,Y)]).
rule(sibling(X,Y),  [parent(X,Z), child(Z,Y)]).
rule(sibling(X,Y),  [sibling(X,Z), sibling(Z,Y)]).
rule(child_in_law(X,Y),  [child(X,Z),so(Z,Y)]).
rule(parent_in_law(X,Y),  [so(X,Z), parent(Z,Y)]).
rule(nephew(X,Y), [sibling(X,Z), child(Z,Y)]).
rule(uncle(X,Y),  [parent(X,Z), sibling(Z,Y)]).
% "rules" is the gather of all the "rule"s:
rules([rule(grandchild(X,Y),  [child(X,Z), child(Z,Y)]),  rule(grandchild(X,Y),  [so(X,Z), grandchild(Z,Y)]),  rule(grandchild(X,Y),  [grandchild(X,Z), sibling(Z,Y)]),  rule(grandparent(X,Y),  [parent(X,Z), parent(Z,Y)]),  rule(grandparent(X,Y),  [sibling(X,Z), grandparent(Z,Y)]),  rule(child(X,Y),  [child(X,Z), sibling(Z,Y)]),  rule(child(X,Y),  [so(X,Z), child(Z,Y)]),  rule(parent(X,Y),  [sibling(X,Z), parent(Z,Y)]),  rule(parent(X,Y),  [child(X,Z), grandparent(Z,Y)]),  rule(sibling(X,Y),  [child(X,Z), uncle(Z,Y)]),  rule(sibling(X,Y),  [parent(X,Z), child(Z,Y)]),  rule(sibling(X,Y),  [sibling(X,Z), sibling(Z,Y)]),  rule(child_in_law(X,Y),  [child(X,Z),so(Z,Y)]),  rule(parent_in_law(X,Y),  [so(X,Z), parent(Z,Y)]),  rule(nephew(X,Y), [sibling(X,Z), child(Z,Y)]),  rule(uncle(X,Y),  [parent(X,Z), sibling(Z,Y)])]).

% list of name of all relations, use for creating facts with:
% Edge =.. [Relation,E1,E2].  or  Goal =.. [R,X,Y]
relation(child).
relation(child_in_law).
relation(parent).
relation(parent_in_law).
relation(sibling).
relation(sibling_in_law).
relation(grandparent).
relation(grandchild).
relation(nephew).
relation(uncle).
relation(so).

% define basic relations, gender facts are covered:
gender_rel(child,male,son).
gender_rel(child,female,daughter).

gender_rel(parent,male,father).
gender_rel(parent,female,mother).

gender_rel(grandchild,male,grandson).
gender_rel(grandchild,female,granddaughter).

gender_rel(grandparent,male,grandfather).
gender_rel(grandparent,female,grandmother).

gender_rel(uncle,male,uncle).
gender_rel(uncle,female,aunt).

gender_rel(child_in_law,male,son_in_law).
gender_rel(child_in_law,female,daughter_in_law).

gender_rel(parent_in_law,male,father_in_law).
gender_rel(parent_in_law,female,mother_in_law).

gender_rel(nephew,male,nephew).
gender_rel(nephew,female,niece).

gender_rel(sibling,male,brother).
gender_rel(sibling,female,sister).

gender_rel(sibling_in_law,male,brother_in_law).
gender_rel(sibling_in_law,female,sister_in_law).

gender_rel(so,male,husband).
gender_rel(so,female,wife).