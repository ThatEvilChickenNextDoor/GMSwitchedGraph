CosetTest:= function(O, I)

local L, stabs, substabs, i, j, cos, orbs;

L:=AllPrimitiveGroups(NrMovedPoints, O);
stabs:=List(L, i->Stabilizer(i, 1));
substabs:=List(stabs, i->Filtered(LowIndexSubgroups(i), I), j->Order(i)/Order(j)=I));
for i in [1..Length(L)] do
	cos:=RightCosets(L[i], substabs[i]);
	orbs:=Orbits(substabs[i], cos, OnRight);
	for j in orbs do
		if Length(j)=O*I then
			Print(IsDistanceRegular(CosetGraph(L[i], substabs[i], [j])), "\n");
		fi;
	od;
od;

return;

end;