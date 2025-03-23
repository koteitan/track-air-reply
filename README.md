# track-air-reply

## 目的

最新の Nostr の note1 に対して、それがどの note1 のエアリプなのかを推定します

## つかいかた

## インストール

`estimate-related-notes.py` スクリプトを実行するには、以下の依存関係をインストールする必要があります。

   ```bash
   sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
   pip install websockets mecab-python3 gensim
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
$ python3 estimate-related-notes.py 
Fetching contact list from Nostr...
Fetching notes from Nostr...
--------------------
Latest content: わかめスープ、激辛唐辛子魚粉鍋
--------------------
Loading word2vec model...
Computing context vector...
--------------------
Latest content: わかめスープ、激辛唐辛子魚粉鍋
--------------------
Related content 499 (similarity: 0.7119824886322021): 今回はカレー用豚バラが1パック入ってるからカレーです
--------------------
Related content 46 (similarity: 0.6608330607414246): 高カロリーの物食べたい
--------------------
Related content 424 (similarity: 0.6289700865745544): ストッキング鍋…？ 4月には歌いまくりたい。 エンイー。 
--------------------
```

MeCab が正しく機能するために、必要な権限と設定が整っていることを確認してください。
