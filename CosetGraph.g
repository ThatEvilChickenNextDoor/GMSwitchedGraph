CosetGraph:= function(G, H, n) #Generate graph with n edges per point from right cosets of group G with subgroup H

#Define local variables

local cos, orbs, orbLengths, pre, edges, imG, outGraph;

Print("Checking inputs...\n"); #Check input validity

if not IsGroup(G) then
	ErrorNoReturn("G must be a group\n");
fi;

if not IsSubgroup(G, H) then
	ErrorNoReturn("H must be a subgroup of G\n");
fi;

if not IsPosInt(n) then
	ErrorNoReturn("n must be a positive integer\n");
fi;

Print("Generating cosets...\n"); #Generate edges from coset

cos:=RightCosets(G, H); #generate set of cosets

Print("Finding orbits...\n");

orbs:=Orbits(H, cos, OnRight); #find orbits of cosets
orbLengths:=List(orbs, Length); #determine length of each orbit
if not n in orbLengths then
	Print("unable to find orbit of desired length\n");
	return fail;
fi;
pre:=orbs[Position(orbLengths, n)]; #choose the orbit with desired length
edges:=List(pre, i->[1,Position(cos, i)]); #match each element in orbit with its index in the set of cosets

Print("Constructing output graph...\n"); #Construct output graph from edge list

imG:=Image(ActionHomomorphism(G, cos, OnRight));
return EdgeOrbitsGraph(imG, edges);

end;
