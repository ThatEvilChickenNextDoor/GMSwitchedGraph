WQHSwitchedGraph:= function(part, graph)

#Define local variables

local p, f, d, c, C, v, i, n, adjCount, adjCountList, adjList, toSwitch, edges, outGraph;

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

if not Length([part[1])=2 then #check if C has exactly 2 elements
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

if not IsGraph(graph) then #check if given graph is actually a graph
	Print("graph must be a graph");
	return;
fi;

#TODO: Check if partitions are mathematically valid

for c in part[1] do #start measuring number of neighbors for each vertex
	adjCountList:=[]; #initialize list for counting neighbors
	for v in part[1] do
		Add(adjCountList, -1);
	od;
#	Print("adjCountList", "\t", adjCountList, "\n");
	for v in c do #start checking
		adjList:=Adjacency(graph, v);
#		Print(v, "\n");
#		Print("adjList", "\t", adjList, "\n");
		for i in [1..Length(part[1])] do #loop through all c's in partition
			adjCount:=Length(Intersection(part[1][i], adjList)); #calculate number of neighbors with this c
#			Print("adjCount", "\t", adjCount, "\n");
#			Print("adjCountList", "\t", adjCountList, "\n");
			if not adjCountList[i]=adjCount then #check if number of neighbors is inconsistent
#				Print("not in list", "\n");
				if adjCountList[i]=-1 then #if first run, store number of neighbors in list
					adjCountList[i]:=adjCount;
				else #if not first run, throw error
					Print("invalid partition");
					return;
				fi;
			fi;
		od;
	od;
od;

for d in part[2] do
#	Print(d, "\n");
	adjList:=Adjacency(graph, d);
	if not adjList=part[1][1] and not adjList=part[1][2] and not Length
od;

#Do the switch

edges:=UndirectedEdges(graph); #gather all edges from original graph before switching
for d in part[2] do #gather all vertices that need to be switched for each vertex in D
	toSwitch:=[]; #list to hold vertices that need to be switched wrt d
	for C in part[1] do #determine which c's should be switched
		adjList:=Adjacency(graph, d);
		if adjList=C then
			Append(toSwitch, C);
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
