ExtendSets2:= function(G, l, V)

#G is automorphism group of graph, l is a set of sets of a given size, V is the set of vertices

local new, i , j, last, poss, prereps, reps;

new:= [];

for i in l do
	Print("Calculating for ", i, " ...\n");
	last:=Combinations(Difference(V, i), 2);
	poss:= List(last, j -> AsSet(Concatenation(i,j)));
#	Print("Calculating orbits for ", i, " ...\n");
#	prereps:= List(Orbits(G, poss, OnSets), Representative);
#    for j in prereps do
	if not poss in new then
		Add(new, poss);
	fi;
#	od;
od;
#Print("Calculating final orbits...\n");
#reps:= List(Orbits(G, new, OnSets), Representative);

return new;

end;
