#!/usr/bin/sh
rm -r data/alexcode228@gmail.com
python3 -c "import pickle; pickle.dump({}, open('data/data.dat', 'bw'))"
echo -n "" > data/users.csv
