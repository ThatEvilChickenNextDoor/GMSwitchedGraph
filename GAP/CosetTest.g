CosetTest:= function(O, I)

local L, stabs, substabs, subs, G, H, i, j, cos, orbs, outList;

outList:=[];
L:=AllPrimitiveGroups(NrMovedPoints, O);
stabs:=List(L, i->Stabilizer(i, 1));
substabs:=List(stabs, i->Filtered(LowIndexSubgroups(i, I), j->Order(i)/Order(j)=I));
for i in [1..Length(L)] do
	G:=L[i];
	subs:=substabs[i];
	for H in subs do
		cos:=RightCosets(G, H);
		orbs:=Orbits(H, cos, OnRight);
		for j in orbs do
			if IsDistanceRegular(CosetGraph(G, H, [j])) then
				Add(outList, [G, H, [j]]);
			fi;
		od;
	od;
od;

return outList;

end;
