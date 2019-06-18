GMSwitchedGraph:= function(part, graph)
#Define local variables
local p, f, Switch;
#Check if given partition is a list
if not IsList(part) then
	Print("first argument must be a list");
	return;
fi;
#Check if partition has a C and D element
if not Length(part)=2 then
	Print("partition must have exactly two elements");
	return;
fi;
#Check if C is a list
if not IsList(part[1]) then
	Print("first element of partition must be a list of C's");
	return;
fi;
#Check if D is a list
if not IsList(part[2]) then
	Print("second element of partition must be a list of verticies");
	return;
fi;
#Check if each C_i is a list
for p in part[1] do
	if not IsList(p) then
		Print("each sublist of C's must be a list of verticies");
		return;
	fi;
	#Check if each element in C_i is a vertex
	for f in p do
		if not IsIntegers(f) then
			Print("each element of C_i must be an integer");
			return;
		fi;
	od;
od;
#Check if given graph is actually a graph
if not IsGraph(graph) then
	Print("graph must be a graph");
	return;
fi;

Print(part[1], "\n");
Print(part[2], "\n");
Print(graph, "\n");

Switch :=graph;

#for p in part[1] do	
	
end;

#Position(VertexNames(graph),x);
#VertexNames(graph)[Position(Vertices(graph),y)];