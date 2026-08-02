(* === LA TRAHISON DE LA TIJD: WOLFRAM REKENMODULE === *)

(* 1. Tijdlijn & Cumulatieve Torsie *)
jarenSindsNicaea = 1371 - 325;
jaarlijkseTorsie = 365.25 - 365.24219;
cumulatieveTorsie = N[jarenSindsNicaea * jaarlijkseTorsie];

(* 2. De Dertien bij Dertien Matrix & Modulo 21 *)
matrixRijen = 13;
matrixKolommen = 13;
totaalCellen = matrixRijen * matrixKolommen; (* 169 *)
moduloWaarde = 21;
residuResonantie = Mod[totaalCellen, moduloWaarde];

(* 3. 13:20 Kalender & Galactisch Nulpunt *)
manen = 13;
dagenPerMaan = 28;
totaalMaanDagen = manen * dagenPerMaan; (* 364 *)
zonneJaar = 365;
galactischNulpunt = zonneJaar - totaalMaanDagen; (* 1 *)

(* === UITVOER & VISUALISATIE === *)
Print["=== WISKUNDIGE PARAMETERS ==="];
Print["Jaren sinds Nicaea: ", jarenSindsNicaea];
Print["Cumulatieve Torsie (Delta T): ", cumulatieveTorsie, " dagen"];
Print["Matrix Dimensie: ", matrixRijen, " x ", matrixKolommen, " = ", totaalCellen, " cellen"];
Print["Modulo ", moduloWaarde, " Resonantie: ", residuResonantie];
Print["Galactisch Nulpunt (Day Out of Time): ", galactischNulpunt];

(* Visualisatie van de 13x13 Matrix met Vortex Elementen *)
matrixRaster = Table[If[Mod[i + j, moduloWaarde] == residuResonantie, 1, 0], {i, matrixRijen}, {j, matrixKolommen}];
ArrayPlot[matrixRaster, 
  ColorRules -> {0 -> RGBColor[0.15, 0.18, 0.25], 1 -> RGBColor[0.2, 0.8, 0.9]},
  PlotLabel -> "13x13 Vortex Matrix (Mod 21 Resonantie)"]
