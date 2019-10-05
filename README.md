# scrape_expense_amount

# What is?

実行日より未来日に予定されている経費の振り込み予定をMFクラウド経費からスクレイピングして通知します。

# Work on Zapier

[Zapier](https://zapier.com/) の Code on Zapier for Python を使用すると Zapierで実行可能です。
ただし、無料版だと実行時間の制約がある為に有料版での実行が必要です。

[ZapierにLINE Notifyを対応してみた \- Qiita](https://qiita.com/dddaisuke/items/fbf9c5c12f19df3440cd) を使用してLINE通知を設定すると
以下の様に表示されます。

![line-notify-image](./images/line-notify-sample.jpg)

# Usage

```
$ export PYTHONPATH=`pwd`/site-packages
$ ./scraping.py
あなたに直近支払いのある経費は0件です。
```


