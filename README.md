# Nostr Note Estimation

## 目的

このプロジェクトの目的は、最新の Nostr のノートに対して、それがどのノートのエアリプなのかを推測することです。

## プロジェクトのセットアップと使用方法

## インストール

`estimate-related-notes.py` スクリプトを実行するには、以下の依存関係をインストールする必要があります。

1. **MeCab**: 日本語形態素解析器。システムに MeCab システムライブラリをインストールする必要があります。パッケージマネージャーを使用してインストールできます。例えば、Ubuntu では以下のコマンドを使用します。
   ```bash
   sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
   ```

2. **Python モジュール**: pip を使用して必要な Python モジュールをインストールします。
   ```bash
   pip install websockets mecab-python3 gensim
   ```

3. **Word Vector データ**: 以下のコマンドを使用してデータをダウンロードし、解凍します。
   ```bash
   wget http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/data/20170201.tar.bz2
   tar -xvjf 20170201.tar.bz2
   ```

## 使用方法

スクリプトを実行するには、以下のコマンドを使用します。
```bash
python3 estimate-related-notes.py
```

## 出力例

スクリプトを実行すると、以下のような出力が表示されます。

```
Fetching contact list from Nostr...
Fetching notes from Nostr...
--------------------
Latest content: 人生はつくれる
--------------------
Loading word2vec model...
Computing context vector...
--------------------
Latest content: 人生はつくれる
--------------------
Related content 417 (similarity: 0.7260157465934753): えーっと……確かに発売日は2021年だよな。流行ってるっていうのはちょっと大げさかも。でもさ、今でも好きな人多いし、影響力はあると思うぜ。時が経ってもいい曲は残るしな。
--------------------
Related content 272 (similarity: 0.7238972187042236): 洒落怖に自分の人生が淡々と記述される回
--------------------
```

MeCab が正しく機能するために、必要な権限と設定が整っていることを確認してください。
