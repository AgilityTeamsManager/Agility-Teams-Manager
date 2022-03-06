#!/usr/bin/sh
python3 -c "import pickle; pickle.dump({}, open('data/users.dat', 'bw'))"
rm -r data/alexcode228@gmail.com
echo -n "" > data/users.csv
