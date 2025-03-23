# track-air-reply

## 目的

最新の Nostr の note1 に対して、それがどの note1 のエアリプなのかを推定します

一旦 bag in words なので精度わるぃ

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
Fetching kind 0 events to build pub2name mapping...
Initial pub2name: {}
Got 400 profiles...
Got 400 profiles...
Fetching contact list from Nostr...
Fetching notes from Nostr...
--------------------
Latest content: koteitan:2025-03-24 02:29:07:お寿司の話
--------------------
Loading word2vec model...
Computing context vector...
Related content(1.000):koteitan:2025-03-24 02:29:07:お寿司の話
Related content(0.703):609cb74df9:2025-03-24 00:48:13:はま寿司は持ち帰りの鯖寿司が一番おいしい
Related content(0.694):koteitan:2025-03-24 02:27:41:例えばお寿司
Related content(0.675):9a664c496a:2025-03-24 00:46:09:悲しみの寿司。悲し寿司
Related content(0.656):fe63f4f840:2025-03-24 01:51:46:明日にでもはま寿司行てくるか
Related content(0.649):e62f27d281:2025-03-24 00:50:49:はま寿司おいしいのに ハズレ店舗だったんじゃね
Related content(0.643):9b840e1210:2025-03-24 02:27:45:お寿司か、いいよな。最近は色んなネタがあるし、回転寿司も楽しいし。俺もたまには友達と行きたいな。でも、あんまり人混みは苦手なんだよな……。
Related content(0.636):fe9edd5d5c:2025-03-24 01:40:59:まじでkoheiさん無限に寝てる？
Related content(0.625):72e8d65495:2025-03-24 00:30:12:ぼくもそのフレーズ知ってるﾁﾓ！とっても力強い言葉だﾁﾓね！おにぎりも勇気をくれる存在だと思うﾁﾓ！一緒に楽しんで、みんなで勇気を分け合うﾁﾓ！🍙✨
Related content(0.621):fe63f4f840:2025-03-24 01:17:48:安回転ずしの中ではま寿司がいちばん美味しいと思ってるけど、ハズレ店舗を引いたヒトにリベンジしろとは言えない
--------------------
```

MeCab が正しく機能するために、必要な権限と設定が整っていることを確認してください。(mecabrc の場所など)
