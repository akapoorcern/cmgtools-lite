#!/bin/bash
P=plots/80X/TnP
IN="mupog_sos_v1.2"; OUT="$IN/00_harvest"

MEAS="SOS SOS_PR SOS_NM1_{Id,Iso,Ip} SOS_003 SOS_NoIP SOS_presel"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    RANGES_PT="--rrange 0.955 1.035  --yrange 0.9 1.005"
    RANGES_OTHER="--rrange 0.975 1.025  --yrange 0.9 1.005"
    MAIN="tnpHarvest.py"
    case $M in
        SOS*) MODS=" -s MCTG -b bern4 --salt dvoigt2  --salt BWDCB2 --balt bern3 "; 
              TIT="$(echo $M | sed 's/_/ /g') efficiency"; 
              RANGES_PT="   --rrange 0.82 1.105  --yrange 0.0 1.005";
              RANGES_OTHER="--rrange 0.82 1.105  --yrange 0.0 1.005"; ;; 
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        python $MAIN -N mu_${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"  $RANGES_PT 
        if echo $M | grep -q SOS; then
            python $MAIN -N mu_${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT" --xrange 0 25 --postfix _zoom $RANGES_PT
        fi
    done
    python $MAIN -N mu_${M}_eta_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
    python $MAIN -N mu_${M}_vtx_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER 
    if echo $M | grep -q SOS; then
        python $MAIN -N mu_${M}_eta_pt520 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
        python $MAIN -N mu_${M}_vtx_pt520 $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER
    fi;
done
