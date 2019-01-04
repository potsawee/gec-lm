#!/bin/tcsh
#$ -S /bin/tcsh

# Check Number of Args
if ($#argv != 5) then
   echo "Usage: $0 script lattices scp out log"
   exit 100
endif

<<<<<<< HEAD
set ALLARGS = ($*)
=======
>>>>>>> 5f0f592fb532515cb220975e95eae033862543c2
set SCRIPT=$1
set LATTICES=$2
set SCP=$3
set OUT=$4
set LOG=$5

set WORKDIR=/home/alta/BLTSpeaking/ged-pm574/gec-lm/scripts
set COMMAND=$WORKDIR/$SCRIPT

<<<<<<< HEAD
if ( ! -d CMDs) mkdir -p CMDs
set CMDFILE=CMDs/run-gec-rescore.cmds
echo `date` >> $CMDFILE
echo $0 $ALLARGS >> $CMDFILE
echo "------------------------------------" >> $CMDFILE


set job = `qsub -cwd -j yes -o $LOG -P esol -l queue_priority=low -l mem_grab=50G -l mem_free=50G $COMMAND $LATTICES $SCP $OUT`
=======
set job = `qsub -cwd -j yes -o $LOG -P esol -l queue_priority=low $COMMAND $LATTICES $SCP $OUT`
>>>>>>> 5f0f592fb532515cb220975e95eae033862543c2
echo $job
