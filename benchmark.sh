# Usage: ./benchmark.sh <dataDir> <solDir> <model>


if [ $# -ne 3 ]; then
    echo "Usage: ./benchmark.sh <dataDir> <solDir> <model>"
    exit 1
fi

echo Experimental Campaign:
echo Data directory: $1
echo Output directory: $2
echo Model: $3

mkdir -p $2
cd $2 && mkdir -p $3
echo `date` > $3/date.txt
cd ../../

for instance in `ls $1`; do
    echo Resolution of $instance
    python3 src/$3.py $1/$instance $2/$3/
done

grep Result $2/$3/*.sol >> $2/$3/results.csv
exit 0
