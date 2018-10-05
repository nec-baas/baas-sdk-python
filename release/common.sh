if [ ! -f config.sh ]; then
    echo "Error: no config.sh"
    exit 1
fi
 
. ./config.sh

WORKCDIR=work
SRCDIR=$WORKCDIR/$VERSION

OUTDIR=out
DEST=baas-sdk-python-${VERSION}
DESTDIR=$OUTDIR/$DEST

PACKAGE_NAME_PREFIX=necbaas
PACKAGE_NAME=${PACKAGE_NAME_PREFIX}-${VERSION}.tar.gz
