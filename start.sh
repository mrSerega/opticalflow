rm -rf pgm_sample

mkdir -p pgm_sample

./mplayer/mplayer.exe -vo pnm:pgm:outdir=pgm_sample $1

./detect/test ./output ./pgm_sample/*