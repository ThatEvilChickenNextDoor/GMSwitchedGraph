ExtendSets2:= function(G, l, V)

#G is automorphism group of graph, l is a set of sets of a given size, V is the set of vertices

local new, i , j, last, poss, prereps, reps;

new:= [];;

for i in l do
	last:= Difference(V, i);
	poss:= List(last, j -> AsSet(Concatenation(i,[j])));
	prereps:= List(Orbits(G, poss, OnSets), Representative);
        for j in prereps do
		if not j in new then
			Add(new, j);
		fi;
	od;
od;

reps:= List(Orbits(G, new, OnSets), Representative);

return reps;

end;
