echo 'usage: start.sh <sample_name> [online|offline] [new]'

if [[ "$3" = "new" ]]
then
./prepare.sh $1
fi

python draw_foe.py $1 $2 > start_log.txt

read ww