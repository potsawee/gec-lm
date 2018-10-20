#!/bin/tcsh
#$ -S /bin/tcsh

set ALLARGS = ($*)
# Check Number of Args
if ( $#argv != 1 ) then
   echo "Usage: $0 file"
   exit 100
endif

set FILE=$1


# Set path to CUDA toolkit
set CUDAPATH="/usr/local/cuda-8.0/lib64:/home/mifs/ar527/bin/tensorflow-gpu/cudnn-8.0-linux-x64-v6.0/cuda/lib64:/usr/local/cuda-8.0/extras/CUPTI/lib64/"

# Set path to CL toolkit
#setenv PYTHONPATH /home/alta/CL-tools/sequence_labeler/sequence-labeler-master:$PWD
#setenv PYTHONPATH $PWD
setenv PYTHONPATH /home/dawna/kmk/anaconda2/lib/python2.7/site-packages:/home/dawna/kmk/misc/lib/python2.7/site-packages:$PWD

# Add offset to GPU number
setenv CUDA_VISIBLE_DEVICES ""

# Disable TensorFlow warnings/home/dawna/ar527/tools/rtk/rtk/neu/tensorflow/custom_sequence.py
#setenv TF_CPP_MIN_LOG_LEVEL 2

if ( $?LD_LIBRARY_PATH ) then
    setenv LD_LIBRARY_PATH "${CUDAPATH}:${LD_LIBRARY_PATH}"
else
    setenv LD_LIBRARY_PATH $CUDAPATH
endif

set PYTHONBIN=/home/dawna/kmk/anaconda2/bin/python

# run sequence labelling
$PYTHONBIN /home/alta/BLTSpeaking/ged-pm574/gec-lm/scripts/experiment.py $FILE
