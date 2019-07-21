AdjacencyMatrix:= function(graph)

local n, A, i, j;
n:=Length(Vertices(graph));
A:=NullMat(n, n);
for i in [1..n] do
		for j in [1..n] do
		if IsEdge(graph, [i,j]) then
			A[i][j]:=1;
		fi;
	od;
od;
return A;
end;