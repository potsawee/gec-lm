#!/bin/tcsh
#$ -S /bin/tcsh

# Check Number of Args
if ($#argv != 5) then
   echo "Usage: $0 script lattices scp out log"
   exit 100
endif

set SCRIPT=$1
set LATTICES=$2
set SCP=$3
set OUT=$4
set LOG=$5

set WORKDIR=/home/alta/BLTSpeaking/ged-pm574/gec-lm/scripts
set COMMAND=$WORKDIR/$SCRIPT

set job = `qsub -cwd -j yes -o $LOG -P esol -l queue_priority=low $COMMAND $LATTICES $SCP $OUT`
echo $job
