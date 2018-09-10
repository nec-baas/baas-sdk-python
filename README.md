NECモバイルバックエンド基盤 Python SDK
=================================

NECモバイルバックエンド基盤の Python SDK です。
Python 2/3 両方に対応しています。

インストール
----------

    $ python setup.py install

使用方法
-------

"import necbaas" としてモジュールをインポートしてください。

使用方法は sample/sample.py を参照してください。

APIについて
----------

* API呼び出しはすべて同期呼び出しです
* エラー発生時は HTTPError 例外が throw されます
