GMSwitchedGraph:= function(G, H, cos)

#Define local variables

local d, c, C, i, adjCount, adjCountList, adjList, toSwitch, edges, outGraph;


Print("Constructing output graph...\n"); #Construct output graph from edge list

outGraph:=Graph(Group(()), Vertices(graph), OnPoints, function(x,y) return [x,y] in edges or [y,x] in edges; end);
return outGraph;

end;
