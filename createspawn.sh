#!/bin/bash

couleurs="orange bleu vert rouge blanc violet cyan vertflash jaune noir marron"
marqueurs="arbrevivant illusionfosse illusioneboulis illusionchutespierre ronces lianes fletrissure empetre piege tenebresmagiques trou"
marqueursmur="murbrise toile"

cwd=`pwd`

rm -rf create
mkdir create

for coul in $couleurs; do
	echo "Creating for $coul"
	mkdir create/$coul
	cd src/public/images/markers
	for m in $marqueurs; do
		composite $m.png -geometry +6+6 fondmarqueur-$coul.png $cwd/create/$coul/$m.png
	done
	for m in $marqueursmur; do
		composite $m.png fondmarqueurmur-$coul.png $cwd/create/$coul/$m.png
	done
	cd - >/dev/null

	cd src/public/images/spawns
	find . -name '*png' ! -name 'fond-*' ! -size 0 | while read s; do
		composite $s fond-$coul.png $cwd/create/$coul/$s
	done
	cd - >/dev/null

	cd create
	#compress $coul >/dev/null 2>/dev/null &
	cd - >/dev/null
done
