if [ ! -f config.sh ]; then
    echo "Error: no config.sh"
    exit 1
fi
 
. ./config.sh

WORKCDIR=work
SRCDIR=$WORKCDIR/$VERSION

OUTDIR=out
DESTDIR=$OUTDIR/$VERSION

