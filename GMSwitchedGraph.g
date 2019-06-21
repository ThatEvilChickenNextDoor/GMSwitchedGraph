AHGMSwitchedGraph:= function(S, graph)

#Define local variables

local s, c, C, adjCount, adjList, toSwitch, edges, outGraph;

Print("Checking inputs...\n"); #Check if inputs are structrually valid

if not IsList(S) then #check if given S is a list
	ErrorNoReturn("first argument must be a list");
	return -1;
fi;

for s in S do #check if each element in S is a vertex with integer name
	if not IsInt(s) then
		ErrorNoReturn("each element of c must be an integer");
	fi;
od;

if not IsGraph(graph) then #check if given graph is actually a graph
	ErrorNoReturn("graph must be a graph");
	return -1;
fi;

#Check if inputs are mathematically valid

if not IsRegularGraph(InducedSubgraph(graph, S)) then #check if S induces a regular subgraph
	Print("S does not induce a regular subgraph", "\n");
	return -1;
fi;

toSwitch:=[];
C:=Difference([1..Length(Vertices(graph))], S); #check if all points in C has either all, none, or half neighbors in S
for c in C do
	adjList:=Adjacency(graph, c);
	adjCount:=Length(Intersection(adjList, S));
	if not adjCount=0 and not adjCount=Length(S) then
		if not adjCount=Length(S)/2 then #if has exactly half neighbors, mark vertex for switching
			Print("invalid switching set", "\n");
			return -1;
		else
			Add(toSwitch, c);
		fi;
	fi;
od;

Print("Switching edges...\n"); #Do the switch

edges:=UndirectedEdges(graph); #gather all edges from original graph before switching
for c in toSwitch do #gather all the vertices that need to be switched
	for s in S do #switch the vertices wrt S
		if IsEdge(graph, [s, c]) then #if it's already an edge in the graph, remove it from the edge list
			if [s, c] in edges then
				Remove(edges, Position(edges, [s, c]));
			else
				Remove(edges, Position(edges, [c, s]));
			fi;
		else #otherwise add the edge to the edge list
			Add(edges, [s,c]);
		fi;
	od;
od;

Print("Constructing output graph...\n"); #Construct output graph from edge list

return Graph(Group(()), Vertices(graph), OnPoints, function(x,y) return [x,y] in edges or [y,x] in edges; end);

end;
