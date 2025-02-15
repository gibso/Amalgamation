#program base.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% spec Nat %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

spec(spec_Nat).
hasId(spec_Nat,0).

%% sorts %%
hasSort(spec_Nat,sort_Element,0).
isNonDataSort(spec_Nat,sort_Element).
sortHasPriority(spec_Nat,sort_Element,3).

hasSort(spec_Nat,sort_Nat,0).
isNonDataSort(spec_Nat,sort_Nat).
sortHasPriority(spec_Nat,sort_Nat,3).

%% operators %%
hasOp(spec_Nat,po_c,0).
opHasSort(spec_Nat,po_c,sort_Element,domain,0).
isNonDataOp(spec_Nat,po_c).
opHasPriority(spec_Nat,po_c,1).

hasOp(spec_Nat,po_plus,0).
opHasSort(spec_Nat,po_plus,sort_Nat,arg1,0).
opHasSort(spec_Nat,po_plus,sort_Nat,arg2,0).
opHasSort(spec_Nat,po_plus,sort_Nat,domain,0).
isNonDataOp(spec_Nat,po_plus).
opHasPriority(spec_Nat,po_plus,1).

hasOp(spec_Nat,po_qsum,0).
opHasSort(spec_Nat,po_qsum,sort_Nat,arg1,0).
opHasSort(spec_Nat,po_qsum,sort_Nat,arg2,0).
opHasSort(spec_Nat,po_qsum,sort_Nat,domain,0).
isNonDataOp(spec_Nat,po_qsum).
opHasPriority(spec_Nat,po_qsum,2).

hasOp(spec_Nat,po_s,0).
opHasSort(spec_Nat,po_s,sort_Element,arg1,0).
opHasSort(spec_Nat,po_s,sort_Nat,arg2,0).
opHasSort(spec_Nat,po_s,sort_Nat,domain,0).
isNonDataOp(spec_Nat,po_s).
opHasPriority(spec_Nat,po_s,3).

hasOp(spec_Nat,po_sum,0).
opHasSort(spec_Nat,po_sum,sort_Nat,arg1,0).
opHasSort(spec_Nat,po_sum,sort_Nat,domain,0).
isNonDataOp(spec_Nat,po_sum).
opHasPriority(spec_Nat,po_sum,2).

hasOp(spec_Nat,po_zero,0).
opHasSort(spec_Nat,po_zero,sort_Nat,domain,0).
isNonDataOp(spec_Nat,po_zero).
opHasPriority(spec_Nat,po_zero,2).

%% predicates %%
%% axioms %%

%% Axiom Ax-sumzerozero:p:2 %%
hasAxiom(spec_Nat,0,0).
axHasEquivalenceClass(spec_Nat,0,0,0).
isNonDataAx(spec_Nat,0).
axHasPriority(spec_Nat,0,2).
axInvolvesPredOp(spec_Nat,0,po_sum,0).
axInvolvesPredOp(spec_Nat,0,po_zero,0).


%% Axiom Ax-qsumzero:p:2 %%
hasAxiom(spec_Nat,1,0).
axHasEquivalenceClass(spec_Nat,1,1,0).
isNonDataAx(spec_Nat,1).
axHasPriority(spec_Nat,1,2).
axInvolvesPredOp(spec_Nat,1,po_zero,0).
axInvolvesPredOp(spec_Nat,1,po_qsum,0).
axInvolvesSort(spec_Nat,1,sort_Nat,0).


%% Axiom Ax-plusZeroId:p:1 %%
hasAxiom(spec_Nat,2,0).
axHasEquivalenceClass(spec_Nat,2,2,0).
isNonDataAx(spec_Nat,2).
axHasPriority(spec_Nat,2,1).
axInvolvesPredOp(spec_Nat,2,po_zero,0).
axInvolvesPredOp(spec_Nat,2,po_plus,0).
axInvolvesSort(spec_Nat,2,sort_Nat,0).


%% Axiom Ax-targetTheoremNat:p:3 %%
hasAxiom(spec_Nat,3,0).
axHasEquivalenceClass(spec_Nat,3,3,0).
isNonDataAx(spec_Nat,3).
axHasPriority(spec_Nat,3,3).
axInvolvesPredOp(spec_Nat,3,po_sum,0).
axInvolvesPredOp(spec_Nat,3,po_zero,0).
axInvolvesPredOp(spec_Nat,3,po_qsum,0).
axInvolvesSort(spec_Nat,3,sort_Nat,0).


%% Axiom Ax-heurekaLemmaNat:p:3 %%
hasAxiom(spec_Nat,4,0).
axHasEquivalenceClass(spec_Nat,4,4,0).
isNonDataAx(spec_Nat,4).
axHasPriority(spec_Nat,4,3).
axInvolvesPredOp(spec_Nat,4,po_sum,0).
axInvolvesPredOp(spec_Nat,4,po_plus,0).
axInvolvesPredOp(spec_Nat,4,po_qsum,0).
axInvolvesSort(spec_Nat,4,sort_Nat,0).




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% spec List %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

spec(spec_List).
hasId(spec_List,1).

%% sorts %%
hasSort(spec_List,sort_El,0).
isNonDataSort(spec_List,sort_El).
sortHasPriority(spec_List,sort_El,3).

hasSort(spec_List,sort_L,0).
isNonDataSort(spec_List,sort_L).
sortHasPriority(spec_List,sort_L,3).

%% operators %%
hasOp(spec_List,po_app,0).
opHasSort(spec_List,po_app,sort_L,arg1,0).
opHasSort(spec_List,po_app,sort_L,arg2,0).
opHasSort(spec_List,po_app,sort_L,domain,0).
isNonDataOp(spec_List,po_app).
opHasPriority(spec_List,po_app,2).

hasOp(spec_List,po_cons,0).
opHasSort(spec_List,po_cons,sort_El,arg1,0).
opHasSort(spec_List,po_cons,sort_L,arg2,0).
opHasSort(spec_List,po_cons,sort_L,domain,0).
isNonDataOp(spec_List,po_cons).
opHasPriority(spec_List,po_cons,3).

hasOp(spec_List,po_nil,0).
opHasSort(spec_List,po_nil,sort_L,domain,0).
isNonDataOp(spec_List,po_nil).
opHasPriority(spec_List,po_nil,2).

hasOp(spec_List,po_qrev,0).
opHasSort(spec_List,po_qrev,sort_L,arg1,0).
opHasSort(spec_List,po_qrev,sort_L,arg2,0).
opHasSort(spec_List,po_qrev,sort_L,domain,0).
isNonDataOp(spec_List,po_qrev).
opHasPriority(spec_List,po_qrev,2).

hasOp(spec_List,po_rev,0).
opHasSort(spec_List,po_rev,sort_L,arg1,0).
opHasSort(spec_List,po_rev,sort_L,domain,0).
isNonDataOp(spec_List,po_rev).
opHasPriority(spec_List,po_rev,2).

%% predicates %%
%% axioms %%

%% Axiom Ax-revnilnil:p:2 %%
hasAxiom(spec_List,6,0).
axHasEquivalenceClass(spec_List,6,6,0).
isNonDataAx(spec_List,6).
axHasPriority(spec_List,6,2).
axInvolvesPredOp(spec_List,6,po_rev,0).
axInvolvesPredOp(spec_List,6,po_nil,0).


%% Axiom Ax-qrevnilxx:p:2 %%
hasAxiom(spec_List,7,0).
axHasEquivalenceClass(spec_List,7,7,0).
isNonDataAx(spec_List,7).
axHasPriority(spec_List,7,2).
axInvolvesPredOp(spec_List,7,po_qrev,0).
axInvolvesPredOp(spec_List,7,po_nil,0).
axInvolvesSort(spec_List,7,sort_L,0).


%% Axiom Ax-appNilIsId:p:1 %%
hasAxiom(spec_List,8,0).
axHasEquivalenceClass(spec_List,8,8,0).
isNonDataAx(spec_List,8).
axHasPriority(spec_List,8,1).
axInvolvesPredOp(spec_List,8,po_app,0).
axInvolvesPredOp(spec_List,8,po_nil,0).
axInvolvesSort(spec_List,8,sort_L,0).


%% Axiom Ax-targetTheoremLists:p:3 %%
hasAxiom(spec_List,9,0).
axHasEquivalenceClass(spec_List,9,9,0).
isNonDataAx(spec_List,9).
axHasPriority(spec_List,9,3).
axInvolvesPredOp(spec_List,9,po_qrev,0).
axInvolvesPredOp(spec_List,9,po_rev,0).
axInvolvesPredOp(spec_List,9,po_nil,0).
axInvolvesSort(spec_List,9,sort_L,0).




