#!/bin/tcsh
#$ -S /bin/tcsh

# To rescore multiple sentences - for GEC based on RNNLM

# Check Number of Args
if ($#argv != 3) then
   echo "Usage: $0 lattices scp out"
   exit 100
endif

set LATTICEDIR=$1
set SCP=$2
set OUT=$3

set MLF=$OUT/1best-rnnlm.mlf
set RESCORELAT=$OUT/lattices

if (! -d $OUT ) mkdir -p $OUT
if (! -d $RESCORELAT ) mkdir -p $RESCORELAT

set HLRESCOREBIN=/home/mifs/xc257/RNNLM/htk_3.4.1.cuedrnnlm.v1.0.maxlogp/HTKTools/HLRescore
# set CFG=/home/dawna/mgb3/transcription/exp-xc257/KB3CTD+R1/decode-LM04-S1seg.RNNLM02.v1.1/base/scripts/hlr.cfg.approx_ng3
set CFG=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/hlrescore-rnnlm-cfgs/hlr.cfg.approx_ng4
set VOCAB=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/one-billion+agid+dtal.uniq.lst




# set LMMODEL=/home/dawna/mgb3/transcription/exp-xc257/KB3CTD+R1/decode-LM04-S1seg.RNNLM02.v1.1/lib/lms.rescore/rnnlm.su3words/ngrnn.intpltlm
# set LMMODEL=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/lms.rescore/rnnlm/ngrnn.intpltlm
# set LMMODEL=ngrnn.intpltlm
# set LMMODEL=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/lms.rescore/rnnlm.su3words/rnnlm.su3words



# RNNLM v1.0 - RNNLM05
# set LMMODEL=/home/dawna/mgb3/transcription/lms/RNNLM05/lib/lms.rescore/rnnlm/rnnlm
set LMMODEL=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/lms.rescore/RNNLM05/ngrnn.intpltlm
# set LMMODEL=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/lms.rescore/RNNLM05/rnnlm



# set TASK=task61
# set LATTICEDIR=/home/alta/BLTSpeaking/ged-pm574/gec-lm/test/$TASK/rescore/lattices/
# set SCP=/home/alta/BLTSpeaking/ged-pm574/gec-lm/test/$TASK/rescore/lattices/flist.scp
# set RESCORELAT=/home/alta/BLTSpeaking/ged-pm574/gec-lm/test/$TASK/rescore/rescore-rnnlm/lattices/
# set MLF=/home/alta/BLTSpeaking/ged-pm574/gec-lm/test/$TASK/rescore/rescore-rnnlm/1bestRNNLM.mlf


$HLRESCOREBIN -T 1 -A -D -V \
  -L $LATTICEDIR \
  -l $RESCORELAT \
  -n $LMMODEL \
  -S $SCP \
  -C $CFG \
  -f \
  -i $MLF \
  -w $VOCAB
