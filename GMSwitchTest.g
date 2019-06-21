GMSwitchTest:= function(toTest, graph)

#Define local variables

local i, V, o, counter, successList, nonIsoList, charPoly;

successList:=[];
nonIsoList:=[];
counter:=0;

Print("Checking inputs...\n"); #Check if inputs are formatted correctly

if not IsList(toTest) then
	ErrorNoReturn("first argument must be a list to test", "\n");
fi;

if not IsGraph(graph) then
	ErrorNoReturn("second argument must be a graph to test", "\n");
fi;

Print("Inputs clean!\n"); #Checks passed, begin testing

V:=Length(Vertices(graph));
charPoly:=CharacteristicPolynomial(AdjacencyMatrix(graph));

for i in toTest do
	Print("Checking ", i, "...\n");
	o:=AHGMSwitchedGraph(i, graph);;
	if IsGraph(o) then
		Print(i, " produced graph");
		if CharacteristicPolynomial(AdjacencyMatrix(o))=charPoly then
			Print(" successfully");
			Add(successList, i);
			if not IsIsomorphicGraph(graph, o) then
				Print(" and is not isomorphic!");
				Add(nonIsoList, i);
			fi;
		else
			Print(" unsuccessfully");
		fi;
		Print("\n");
	fi;
	counter:=counter+1;;
od;

#Output results

Print(Length(toTest), " inputs, ", counter, " tested, ", Length(successList), " valid switches, ", Length(nonIsoList), " not isomorphic\n");
return [successList, nonIsoList];

end;