#!/bin/tcsh
#$ -S /bin/tcsh

# set verbose

# Check Number of Args
if ($#argv != 3) then
   echo "Usage: $0 latdir scp mlf"
   exit 100
endif

set LATTICEDIR=$1 # lattice directory (biased)
set SCP=$2 # scp file
set MLF=$3 # output


# set HLRESCOREBIN=base/bin/HLRescore
set HLRESCOREBIN=/home/htk3.5/exp-ar527/alpha3/bin.cpu/HLRescore
set HLRESCORECFG=lib/hlrescore.cfg


# ---------- Vocabulary ---------- #
# set VOCAB=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/one-billion+agid+conll.uniq.lst
set VOCAB=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/one-billion+agid+dtal.uniq.lst
# ----------------------------------------------------------- #

$HLRESCOREBIN -A -D -V -C $HLRESCORECFG -L $LATTICEDIR -f -i $MLF -S $SCP $VOCAB
