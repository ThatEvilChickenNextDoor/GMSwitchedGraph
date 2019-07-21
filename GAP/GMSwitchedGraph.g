GMSwitchedGraph:= function(part, graph)

#Define local variables

local d, c, C, i, adjCount, adjCountList, adjList, toSwitch, edges, outGraph;

Print("Checking inputs...\n"); #Check if inputs are structrually valid

if not IsList(part) then #check if given partition is a list
	ErrorNoReturn("first argument must be a list");
fi;

if not Length(part)=2 then #check if partition has a C and D element
	ErrorNoReturn("partition must have exactly two elements");
fi;

if not IsList(part[1]) then #check if C is a list
	ErrorNoReturn("first element of partition must be a list of C's");
fi;

if not IsList(part[2]) then #check if D is a list
	ErrorNoReturn("second element of partition must be a list of verticies");
fi;

for d in part[2] do #check if each element in D is a vertex with integer name
	if not IsInt(d) then
		ErrorNoReturn("each element of D must be an integer");
	fi;
od;

for C in part[1] do #check if each c in C is a list
	if not IsList(C) then
		ErrorNoReturn("each sublist of C must be a list of verticies");
	fi;
	for c in C do #check if each element in c is a vertex with integer name
		if not IsInt(c) then
			ErrorNoReturn("each element of c must be an integer");
		fi;
	od;
od;

if not IsGraph(graph) then #check if given graph is actually a graph
	ErrorNoReturn("graph must be a graph");
fi;

#Check if partitions are mathematically valid

for C in part[1] do #start measuring number of neighbors for each vertex
	adjCountList:=[]; #initialize list for counting neighbors
	for i in part[1] do
		Add(adjCountList, -1);
	od;
#	Print("adjCountList", "\t", adjCountList, "\n");
	for c in C do #start checking
		adjList:=Adjacency(graph, c);
#		Print(c, "\n");
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
	Print(d, "\n");
	for C in part[1] do
		adjList:=Adjacency(graph, d);
		adjCount:=Length(Intersection(C, adjList));
		if not adjCount=Length(C)/2 and not adjCount=Length(C) and not adjCount=0 then
			Print("invalid D");
			return;
		fi;
	od;
od;

Print("Switching edges...\n"); #Do the switch

edges:=UndirectedEdges(graph); #gather all edges from original graph before switching
for d in part[2] do #gather all vertices that need to be switched for each vertex in D
	toSwitch:=[]; #list to hold vertices that need to be switched wrt d
	for C in part[1] do #determine which c's should be switched
		adjList:=Adjacency(graph, d);
		adjCount:=Length(Intersection(C, adjList));
		if adjCount = Length(C)/2 then #only add the vertices in c to the list to be switched if d is adjacent to exactly half of its vertices
			Append(toSwitch, C);
		fi;
	od;
	for c in toSwitch do #switch the vertices wrt d
		if IsEdge(graph, [d, c]) then #if it's already an edge in the graph, remove it from the edge list
			if [d, c] in edges then
				Remove(edges, Position(edges, [d, c]));
			else
				Remove(edges, Position(edges, [c, d]));
			fi;
		else #otherwise add the edge to the edge list
			Add(edges, [c,d]);
		fi;
	od;
od;

Print("Constructing output graph...\n"); #Construct output graph from edge list

outGraph:=Graph(Group(()), Vertices(graph), OnPoints, function(x,y) return [x,y] in edges or [y,x] in edges; end);
return outGraph;

end;
