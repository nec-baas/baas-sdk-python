開発手順
========

テスト手順
----------

テスト関連のモジュールをインストールしてください

    $ pip install .[test]

### 単体テスト

単体テストは以下手順で実施してください

    $ pytest -v tests/unit

### 機能テスト

BaaSサーバに接続するための設定を $HOME/.baas/python_test_config.yaml に格納してください。
ファイルテンプレートは tests/func/python_test_config.sample.yaml にあります。

!!!注意!!!
指定したテナントのデータは削除されます。
必ず FT 専用のテナントを作って実行してください。

また、$HOME/.baas/python ディレクトリは削除されます。
設定ファイル等の必要なファイルは退避させてください。
!!!注意!!!

機能テストは以下手順で実施してください

    $ pytest -v tests/func

### 複数バージョン一括テスト

Python 複数バージョン一括テストをする場合は tox を使用してください。

    $ tox

ドキュメント生成
-------------

ドキュメント関連のモジュールをインストールしてください

    $ pip install .[doc]

以下手順で sphinx 関連のファイルを生成します。
(docs ディレクトリにはすでに生成済みのため通常再実施は不要)

    $ sphinx-apidoc -F -o docs necbaas

以下手順で html ファイルを生成します

    $ cd docs && make html
