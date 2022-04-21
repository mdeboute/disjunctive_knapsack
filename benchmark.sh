# Usage: ./benchmark.sh <dataDir> <solDir> <model>


if [ $# -ne 3 ]; then
    echo "Usage: ./benchmark.sh <dataDir> <solDir> <model>"
    exit 1
fi

echo "Experimental Campaign:"
echo "Data directory: $1"
echo "Output directory: $2"
echo "Model: $3"

mkdir -p $2
cd $2 && mkdir -p $3
echo `date` > $3/date.txt
cd ../../

for instance in `ls $1`; do
    echo Resolution of $instance
    log="log_${instance%.dat}.txt"
    python3 src/$3.py $1/$instance > $2/$3/$log
done

cd $2
grep Result $3/*.txt > $3/results.csv
# for each line of the results.csv file remove all before ':'
sed 's/^.*://' $3/results.csv > $3/results.csv

echo "Experimental Campaign finished!"
exit 0
