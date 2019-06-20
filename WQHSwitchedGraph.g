WQHSwitchedGraph:= function(part, graph)

#Define local variables

local p, f, d, c, C, v, i, n, I1, I2, I3, adjCount, adjCountList, adjList, toSwitch, edges, outGraph;

#Check if inputs are structrually valid

if not IsList(part) then #check if given partition is a list
	Print("first argument must be a list");
	return;
fi;

if not Length(part)=2 then #check if partition has a C and D element
	Print("partition must have exactly two elements");
	return;
fi;

if not IsList(part[1]) then #check if C is a list
	Print("first element of partition must be a list of C's");
	return;
fi;

if not Length(part[1])=2 then #check if C has exactly 2 elements
	Print("C must have exactly two elements");
	return;
fi;

if not IsList(part[2]) then #check if D is a list
	Print("second element of partition must be a list of verticies");
	return;
fi;

for f in part[2] do #check if each element in D is a vertex with integer name
	if not IsInt(f) then
		Print("each element of D must be an integer");
		return;
	fi;
od;

for p in part[1] do #check if each c in C is a list
	if not IsList(p) then
		Print("each sublist of C must be a list of verticies");
		return;
	fi;
	
	for f in p do #check if each element in c is a vertex with integer name
		if not IsInt(f) then
			Print("each element of c must be an integer");
			return;
		fi;
	od;
od;

if not Length(part[1][1])=Length(part[1][2]) then
	Print("c's must be same size");
	return;
fi;

if not IsGraph(graph) then #check if given graph is actually a graph
	Print("graph must be a graph");
	return;
fi;

#TODO: Check if partitions are mathematically valid

I1:=InducedSubgraph(graph, part[1][1]);
I2:=InducedSubgraph(graph, part[1][2]);
I3:=InducedSubgraph(graph, Union(part[1][1], part[1][2]));

if not IsRegularGraph(I1) then
	Print("induced subgraph on c1 is not regular");
	return;
fi;

if not IsRegularGraph(I2) then
	Print("induced subgraph on c2 is not regular");
	return;
fi;

if not IsRegularGraph(I3) then
	Print("induced subgraph on c1 union c2 is not regular");
	return;
fi;

if not Length(Adjacency(I1, Vertices(I1)[1]))=Length(Adjacency(I2, Vertices(I2)[1])) then
	Print("degrees in induced subgraphs on c1 and c2 must be the same");
	return;
fi;

for d in part[2] do
#	Print(d, "\n");
	adjList:=Adjacency(graph, d);
	if not adjList=part[1][1] and not adjList=part[1][2] and not Length(Intersection(adjList, part[1][1]))=Length(Intersection(adjList, part[1][2])) then
		Print("invalid D");
		return;
	fi;
od;

#Do the switch

edges:=UndirectedEdges(graph); #gather all edges from original graph before switching
for d in part[2] do #gather all vertices that need to be switched for each vertex in D
	toSwitch:=[]; #list to hold vertices that need to be switched wrt d
	for C in part[1] do #determine which c's should be switched
		adjList:=Adjacency(graph, d);
		if adjList=C then
			Append(toSwitch, Union(part[1][1], part[1][2]));
		fi;
	od;
	for v in toSwitch do #switch the vertices wrt d
		if IsEdge(graph, [d, v]) then #if it's already an edge in the graph, remove it from the edge list
			if [d, v] in edges then
				Remove(edges, Position(edges, [d, v]));
			else
				Remove(edges, Position(edges, [v, d]));
			fi;
		else #otherwise add the edge to the edge list
			Add(edges, [v,d]);
		fi;
	od;
od;

#Construct output graph from edge list

outGraph:=Graph(Group(()), Vertices(graph), OnPoints, function(x,y) return [x,y] in edges or [y,x] in edges; end);
return outGraph;

end;
