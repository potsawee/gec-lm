#!/bin/tcsh
#$ -S /bin/tcsh

# Check Number of Args
if ($#argv != 5) then
   echo "Usage: $0 file lattices threshold log log-output"
   exit 100
endif

set ALLARGS = ($*)
set FILE=$1
set LATTICES=$2
set THRESHOLD=$3
set LOG=$4
set LOGOUTPUT=$5

if ( ! -d CMDs) mkdir -p CMDs
set CMDFILE=CMDs/run-gec-mklat.cmds
echo `date` >> $CMDFILE
echo $0 $ALLARGS >> $CMDFILE
echo "------------------------------------" >> $CMDFILE

set WORKDIR=/home/alta/BLTSpeaking/ged-pm574/gec-lm/scripts
set COMMAND=$WORKDIR/make_lattices.sh


set job = `qsub -cwd -j yes -o $LOGOUTPUT -P esol -l queue_priority=cuda-low -l osrel='*' -l mem_grab=50G -l mem_free=50G $COMMAND $FILE $LATTICES $THRESHOLD $LOG`
echo $job
