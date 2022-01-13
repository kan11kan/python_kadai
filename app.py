import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

#メモ
#- ファイルの中身を変更する度にターミナルで $python3 app.py　を叩かないとエラーになる
#- ◯行目："""" が意味するところ→複数行コメントアウト（シングルクオートでも可）
#- 理解できていないポイント→モジュールの扱い→第9回の課題をやってみる。
#- リスト内包表記？？


@app.route("/")
def index():
    #"""初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    #"""はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""
    with urlopen("http://feeds.feedburner.com/hatena/b/hotentry") as res:
        #- with urlopen("~")as res:でhttpのGet通信を発行している
        #- from urllib.request import urlopen　で関数を呼び出している

        html = res.read().decode("utf-8")
        #- html　という変数に先程読み込んだhtmlを格納し

    soup = BeautifulSoup(html, "html.parser")
        #- BeautifulSoup(html,"html.parser")でHTMLを読み込んでいる

    items = soup.select("item")
        #- 5行目："from bs4 import BeautifulSoup" でBeautifulSoupを使える状態にしている
        #- 取得したHTML要素の　item というクラスの要素を全て取得する



    shuffle(items)
    item = items[0]


    print(item)
    return json.dumps({
        "content" : item.find("title").string,
        "link" : item.find("link").string,
        "link": item.get('rdf:about')
    })
    

#/api/testにアクセスされた時
@app.route("/api/test")
#def api_test()という関数を呼び出す
def api_test():
    with urlopen("https://www.yoheim.net/blog.php?q=20200401") as res:
        html = res.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".article h2")
    shuffle(items)
    item = items[0]


    """
    print("hoge")
    print (items)"""
    """ bloombergのページのクラスをメモ 
        <div class="story-list-story__info__headline">
            <a class="story-list-story__info__headline-link" href="/news/articles/2022-01-13/R5M0FZDWRGG001?srnd=cojp-v2">ブラックロックのリーダー氏、ＦＲＢはオーバーシュートを回避する</a>
        </div>
    """
    #return "hello from flask"
    #titles = soup.select(".story-list-story__info__headline a")
    #titles = [t.string for t in titles]
    print(item)
    
    return json.dumps({
        "content":item.text,
        #"link" : item.text.find("link"),
        "link": item.get('rdf:about')
        }, ensure_ascii=False)
    """json.dumps({
        "content" : item.text({})ensure_ascii=False#.find_all("title")#.string
        #"link" : soup#.find("story-list-story__info__headline-link").string#,
        #"link": item.get('rdf:about')
    })"""
    """
    return json.dumps({
        "content" : item.find("title").string,
        "link" : item.find("link").string,
        "link": item.get('rdf:about')
    })"""

    pass

if __name__ == "__main__":

    #サーバー起動
    app.run(debug=True, port=5004)
