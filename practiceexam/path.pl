edge(a, b).
edge(b, c).
edge(c, d).
edge(e, d).

there_is_a_path(X, Y) :- X=Y.
there_is_a_path(X, Y) :- edge(X, Z), there_is_a_path(Z, Y).

check_down(Item, [Head | _]) :- Item=Head.
check_down(Item, [_ | Tail]) :- check_down(Item, Tail).
has_cycle([Head | Tail]) :- check_down(Head, Tail); has_cycle(Tail).

leaves(tree([]), Leaves) :- Leaves=[].
leaves(tree([Head | TTail]), Leaves) :- atom(Head), leaves(tree(TTail), LTail), Leaves = [Head | LTail].
leaves(tree([tree(HTree) | TTail]), Leaves) :- leaves(tree(HTree), HLeaves), leaves(tree(TTail), TLeaves), append(HLeaves, TLeaves, Leaves).