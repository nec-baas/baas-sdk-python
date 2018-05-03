開発手順
=======

テスト手順
--------

テストには nose が必要です

    $ pip install nose

単体テストは以下手順で実施してください

    $ nosetests

ドキュメント生成
-------------

Sphinx が必要です。

    $ pip install sphinx sphinx-rtd-theme

以下手順で sphinx 関連のファイルを生成します。
(docs ディレクトリにはすでに生成済みのため再実施は不要)

    $ sphinx-apidoc -F -o docs necbaas

以下手順で html ファイルを生成します

    $ cd docs && make html