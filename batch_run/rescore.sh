#!/bin/bash

export SCRIPT=hlrescore_rnnlm.sh
export LATTICES=test-v3/conll/lattices
export RESCORE=test-v3/conll/rescore-1B-rnnlm300-300

./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t010 $LATTICES-t010/flist.scp $RESCORE-t010 LOGs/conll-rescore-v3-rnnlm300-300-t010.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t020 $LATTICES-t020/flist.scp $RESCORE-t020 LOGs/conll-rescore-v3-rnnlm300-300-t020.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t030 $LATTICES-t030/flist.scp $RESCORE-t030 LOGs/conll-rescore-v3-rnnlm300-300-t030.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t040 $LATTICES-t040/flist.scp $RESCORE-t040 LOGs/conll-rescore-v3-rnnlm300-300-t040.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t045 $LATTICES-t045/flist.scp $RESCORE-t045 LOGs/conll-rescore-v3-rnnlm300-300-t045.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t050 $LATTICES-t050/flist.scp $RESCORE-t050 LOGs/conll-rescore-v3-rnnlm300-300-t050.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t055 $LATTICES-t055/flist.scp $RESCORE-t055 LOGs/conll-rescore-v3-rnnlm300-300-t055.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t060 $LATTICES-t060/flist.scp $RESCORE-t060 LOGs/conll-rescore-v3-rnnlm300-300-t060.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t070 $LATTICES-t070/flist.scp $RESCORE-t070 LOGs/conll-rescore-v3-rnnlm300-300-t070.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t075 $LATTICES-t075/flist.scp $RESCORE-t075 LOGs/conll-rescore-v3-rnnlm300-300-t075.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t080 $LATTICES-t080/flist.scp $RESCORE-t080 LOGs/conll-rescore-v3-rnnlm300-300-t080.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t085 $LATTICES-t085/flist.scp $RESCORE-t085 LOGs/conll-rescore-v3-rnnlm300-300-t085.txt
./scripts/run-gec-rescore.sh $SCRIPT $LATTICES-t090 $LATTICES-t090/flist.scp $RESCORE-t090 LOGs/conll-rescore-v3-rnnlm300-300-t090.txt
