#!/bin/tcsh
#$ -S /bin/tcsh

# Check Number of Args
<<<<<<< HEAD
if ($#argv != 4) then
   echo "Usage: $0 file lattices log log-output"
   exit 100
endif

set ALLARGS = ($*)
set FILE=$1
set LATTICES=$2
set LOG=$3
set LOGOUTPUT=$4

if ( ! -d CMDs) mkdir -p CMDs
set CMDFILE=CMDs/run-gec-mklat.cmds
echo `date` >> $CMDFILE
echo $0 $ALLARGS >> $CMDFILE
echo "------------------------------------" >> $CMDFILE

set WORKDIR=/home/alta/BLTSpeaking/ged-pm574/gec-lm/scripts
set COMMAND=$WORKDIR/make_lattices.sh


set job = `qsub -cwd -j yes -o $LOGOUTPUT -P esol -l queue_priority=cuda-low -l gpuclass=pascal -l osrel='*' -l mem_grab=50G -l mem_free=50G $COMMAND $FILE $LATTICES $LOG`
=======
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
>>>>>>> 5f0f592fb532515cb220975e95eae033862543c2
echo $job
