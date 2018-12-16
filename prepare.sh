mkdir -p pgm_sample
mkdir logs
mkdir '.\samples\'$1
mkdir '.\logs\'$1

echo processing of video...
./mplayer/mplayer.exe -vo pnm:pgm:outdir='pgm_sample\'$1 '.\samples\'$1 > '.\logs\'$1'\'mplayer_log.txt
echo complited

echo processing of pictures...
./detect/test ./output './pgm_sample/'$1'/'* > '.\logs\'$1'\'foe_log.txt
echo complited

# mkdir output
# mkdir '.\output\'$1
# mv *.pgm ./output/$1
rm *.pgm

echo end of preparation

