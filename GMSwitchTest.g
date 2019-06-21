GMSwitchTest:= function(toTest, graph)

local i, V, C, o, counter, successList, nonIsoList, charPoly;

successList:=[];
nonIsoList:=[];
counter:=0;

if not IsList(toTest) then
	Print("first argument must be a list to test", "\n");
	return -1;
fi;

if not IsGraph(graph) then
	Print("second argument must be a graph to test", "\n");
	return -1;
fi;

V:=Length(Vertices(graph));
charPoly:=CharacteristicPolynomial(AdjacencyMatrix(graph));

for i in toTest do
	C:=Difference([1..V], i);;
	o:=GMSwitchedGraph([[C],i],graph);;
	if IsGraph(o) then
		Print(i, " produced graph");
		if CharacteristicPolynomial(AdjacencyMatrix(o))=charPoly then
			Print(" successfully");
			Add(successList, i);
			if not IsIsomorphicGraph(graph, o) then
				Print(" and is nonisomorphic!");
				Add(nonIsoList, i);
			fi;
		fi;
		Print("\n");
	fi;
	counter:=counter+1;;
od;
Print(Length(toTest), " inputs, ", counter, " tested, ", Length(successList), " valid switches, ", Length(nonIsoList), " not isomorphic\n");
return [successList, nonIsoList];

end;