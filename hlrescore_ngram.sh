#!/bin/tcsh
#$ -S /bin/tcsh

# set verbose
# To rescore multiple sentences - for GEC based on ngram LMs

# Check Number of Args
if ($#argv != 3) then
   echo "Usage: $0 lattices scp out"
   exit 100
endif

set LATTICEDIR=$1
set SCP=$2
set OUT=$3

set MLF=$OUT/1best.mlf
set RESCORELAT=$OUT/lattices

if (! -d $OUT ) mkdir -p $OUT
if (! -d $RESCORELAT ) mkdir -p $RESCORELAT


# set HLRESCOREBIN=base/bin/HLRescore
set HLRESCOREBIN=/home/htk3.5/exp-ar527/alpha3/bin.cpu/HLRescore
set HLRESCORECFG=lib/hlrescore.cfg
# set LATTICEDIR=test/task3/task3_script1.1/decode/lattices

# 4-gram trained on MGB3 (from mfjg)
# set NGRAMMODEL=/home/dawna/mgb3/transcription/lms/LM04/lms/fg_train.lm

set NGRAMMODEL=/home/alta/BLTSpeaking/ged-pm574/n-gram-lm/lms/google-ar527/fg_train.lm
# set NGRAMMODEL=/home/alta/BLTSpeaking/ged-pm574/n-gram-lm/lms/LM.grp14/lms/fg_train.lm



# set MLF=test/task3/task3_script1.1/decode/rescore/tg_21.0_0.0/task3_task3_script1.mlf
# set RESCORELAT=test/task3/task3_script1.1/decode/rescore/tg_21.0_0.0/lattices
# set SCP=myscp.scp
set VOCAB=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/one-billion+agid+dtal.uniq.lst2
# set VOCAB=/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/one-billion+agid+conll.uniq.lst


# $HLRESCOREBIN -A -D -V -C $HLRESCORECFG -L $LATTICEDIR -T 1 -t 300.0 1000.0 -s 21.0 -p 0.0 -n $NGRAMMODEL -f -i $MLF -w -l $RESCORELAT -S $SCP $VOCAB
# pruning: -t 300.0 1000.0
# LM scale factor: -s 21.0
# word insertion probability: -p 0.0
$HLRESCOREBIN -A -D -V -C $HLRESCORECFG -L $LATTICEDIR -T 1 -n $NGRAMMODEL -f -i $MLF -w -l $RESCORELAT -S $SCP $VOCAB
# ./base/bin/HLRescore -T 1 -A -V -D -C lib/hlrescore.cfg -X lat -i OUTPUT -n MODEL -f WORDLIST SLF

# RNNLM
# ./HLRescore.cuedrnnlm.v1.1 -T 1 -A -D -V -L lattices.in -l lattices.out -t 300.0 300.0 \
#          -s 12.0 -r 0.0 -p 0.0 -n lms/ngrnn.intpltlm -S ./dev_1_lattices.scp \
#          -C ./hlr.cfg -f -i lattices.out/dev_dev_1.mlf -w ./test.lv.dct
