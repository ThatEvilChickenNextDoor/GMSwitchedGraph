GMSwitchedGraph:= function(part, graph)

if not IsList(part) then
	Print("first argument must be a list");
	return;
fi;

if not Length(part)=2 then
	Print("partition must have exactly two elements");
	return;
fi;

if not IsList(part[1]) then
	Print("first element of partition must be a list of C's");
	return;
fi;

if not IsList(part[2]) then
	Print("second element of partition must be a list of verticies");
	return;
fi;

for p in part[1] do
	if not IsList(p) then
		Print("each sublist of C's must be a list of verticies");
		return;
	fi;
od;

if not IsList(graph) then
	Print("graph must be a list of verticies");
	return;
fi;

Print(part[1], "\n");
Print(part[2], "\n");
Print(graph);
end;
