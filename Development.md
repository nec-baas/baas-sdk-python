開発手順
=======

テスト手順
----------

テストには nose が必要です。また Python 複数バージョンテストの実施のため
tox も必要です。

    $ pip install nose tox

### 単体テスト

単体テストは以下手順で実施してください

    $ nosetests tests/units

### 機能テスト

BaaSサーバに接続するための設定を $HOME/.baas/python_test_config.yaml に格納してください。
ファイルテンプレートは tests/func/python_test_config.sample.yaml にあります。

機能テストは以下手順で実施してください

    $ nosetests tests/func

### 複数バージョン一括テスト

Python 複数バージョン一括テストをする場合は tox を使用してください。

    $ tox    

ドキュメント生成
-------------

Sphinx が必要です。

    $ pip install sphinx sphinx-rtd-theme

以下手順で sphinx 関連のファイルを生成します。
(docs ディレクトリにはすでに生成済みのため通常再実施は不要)

    $ sphinx-apidoc -F -o docs necbaas

以下手順で html ファイルを生成します

    $ cd docs && make html
