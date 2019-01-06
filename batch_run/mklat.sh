#!/bin/bash

# export SRC=lib/conll14st-test-data/exp-pm574/conll.processed.gec.src.v2
export SRC=lib/dtal-m2/nodisfl_train.gec.txt
export LATTICES=test-v3/dtal/lattices
export LOG=LOGs/mklat-dtal

./scripts/run-gec-mklat.sh $SRC $LATTICES-t010 0.10 $LOG-v3-t010.txt $LOG-v3-t010.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t020 0.20 $LOG-v3-t020.txt $LOG-v3-t020.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t030 0.30 $LOG-v3-t030.txt $LOG-v3-t030.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t040 0.40 $LOG-v3-t040.txt $LOG-v3-t040.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t045 0.45 $LOG-v3-t045.txt $LOG-v3-t045.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t050 0.50 $LOG-v3-t050.txt $LOG-v3-t050.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t055 0.55 $LOG-v3-t055.txt $LOG-v3-t055.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t060 0.60 $LOG-v3-t060.txt $LOG-v3-t060.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t070 0.70 $LOG-v3-t070.txt $LOG-v3-t070.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t075 0.75 $LOG-v3-t075.txt $LOG-v3-t075.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t080 0.80 $LOG-v3-t080.txt $LOG-v3-t080.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t085 0.85 $LOG-v3-t085.txt $LOG-v3-t085.log.txt
./scripts/run-gec-mklat.sh $SRC $LATTICES-t090 0.90 $LOG-v3-t090.txt $LOG-v3-t090.log.txt
