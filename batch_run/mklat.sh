#!/bin/bash

export SRC=lib/conll14st-test-data/exp-pm574/conll.processed.gec.src.v2

./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t010 0.10 LOGs/mklat-conll-v3-t010.txt LOGs/mklat-conll-v3-t010.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t020 0.20 LOGs/mklat-conll-v3-t020.txt LOGs/mklat-conll-v3-t020.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t030 0.30 LOGs/mklat-conll-v3-t030.txt LOGs/mklat-conll-v3-t030.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t040 0.40 LOGs/mklat-conll-v3-t040.txt LOGs/mklat-conll-v3-t040.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t045 0.45 LOGs/mklat-conll-v3-t045.txt LOGs/mklat-conll-v3-t045.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t050 0.50 LOGs/mklat-conll-v3-t050.txt LOGs/mklat-conll-v3-t050.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t055 0.55 LOGs/mklat-conll-v3-t055.txt LOGs/mklat-conll-v3-t055.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t060 0.60 LOGs/mklat-conll-v3-t060.txt LOGs/mklat-conll-v3-t060.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t070 0.70 LOGs/mklat-conll-v3-t070.txt LOGs/mklat-conll-v3-t070.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t075 0.75 LOGs/mklat-conll-v3-t075.txt LOGs/mklat-conll-v3-t075.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t080 0.80 LOGs/mklat-conll-v3-t080.txt LOGs/mklat-conll-v3-t080.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t085 0.85 LOGs/mklat-conll-v3-t085.txt LOGs/mklat-conll-v3-t085.log.txt
./scripts/run-gec-mklat.sh $SRC test-v3/conll/lattices-t090 0.90 LOGs/mklat-conll-v3-t090.txt LOGs/mklat-conll-v3-t090.log.txt
