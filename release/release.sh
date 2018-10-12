#!/bin/sh

. ./common.sh

# workディレクトリ作成
/bin/rm -rf $WORKDIR
mkdir -p $SRCDIR

((cd .. && git archive --format=tar $TAG) | tar xvf - -C $SRCDIR) \
    || { echo "extract error"; exit 1; }

# モジュールのインストール（テスト関連）
( cd $SRCDIR && pip install .[test] ) \
    || { echo "modules install error"; exit 1; }

# unit test
( cd $SRCDIR && pytest -v tests/unit ) \
    || { echo "unit test error"; exit 1; }

# func test
( cd $SRCDIR && pytest -v tests/func ) \
    || { echo "func test error"; exit 1; }

# archive package files 
( cd $SRCDIR && ./setup.py sdist ) \
    || { echo " archive package files error"; exit 1; }

# ディレクトリ作成
/bin/rm -rf $DESTDIR
mkdir -p $DESTDIR

# ファイルコピー
cp $SRCDIR/dist/necbaas-${VERSION}.tar.gz $DESTDIR

echo "Done."

