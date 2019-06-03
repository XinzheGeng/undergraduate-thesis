#!/bin/sh
python train.py -t 10 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 30 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 50 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 80 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 100 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 1000 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 10000 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 20000 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
python train.py -t 40000 -T 20000 -d ./dataset.pickle >> test.log
echo '=============================================================' >> test.log
