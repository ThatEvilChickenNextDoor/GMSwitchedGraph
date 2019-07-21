CosetGraph:= function(G, H, orbList) #Generate graph from list of orbits from right cosets of group G with subgroup H

#Define local variables

local cos, orbs, o, pre, edges, imG, outGraph;

Print("Checking inputs...\n"); #Check input validity

if not IsGroup(G) then
	ErrorNoReturn("G must be a group\n");
fi;

if not IsSubgroup(G, H) then
	ErrorNoReturn("H must be a subgroup of G\n");
fi;

if not IsList(orbList) then
	ErrorNoReturn("orbList must be a list\n");
fi;

for o in orbList do #check if each element of orbList is an orbit of H
	if not AsSet(o)=AsSet(Orbit(H, o[1], OnRight)) then
		ErrorNoReturn("orbList must be composed of orbits of H\n");
	fi;
od;

Print("Generating edges...\n"); #Generate edges from coset

cos:=RightCosets(G, H); #generate set of cosets
pre:=Concatenation(orbList);
edges:=List(pre, i->[1,Position(cos, i)]); #match each element in orbit with its index in the set of cosets

Print("Constructing output graph...\n"); #Construct output graph from edge list

imG:=Image(ActionHomomorphism(G, cos, OnRight));
return EdgeOrbitsGraph(imG, edges);

end;
