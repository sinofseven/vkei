# _*_ coding:UTF-8 _*_
import json
from retry import retry
from urllib.request import urlopen
from bs4 import BeautifulSoup

## brand-x リリースカレンダーURL
url="http://www.brand-x.jp/page/38"

def main():
    try:
        getReleasedate()
    except:
         print("カレンダー情報が取得できませんでした")

## ヴィジュアル系カレンダーを読み込んでJSON化
@retry(tries=4, delay=5, backoff=2)
def getReleasedate():
    # 参考URL：http://qiita.com/hujuu/items/b0339404b8b0460087f9
    # ブランドXカレンダーを読み込む
    html =urlopen(url)
    # BeautifulSoapで指定ページをパースする
    bsObj = BeautifulSoup(html, "html.parser")

    # 読み込むテーブルを指定
    # 取得したテーブルのclassを指定
    # 今回取得したいページにはtableタグのclassがなかったのでdivタグのclassを指定
    table = bsObj.findAll("div",{"class":"free_contents"})[0]
    # trタグの内容を取得
    rows = table.findAll("tr")

    # 値のみを配列に
    jsonRow = []
    for row in rows:        
        for cell in row.findAll(['td', 'th']):
            jsonRow.append(cell.get_text())
    
    # Pythonオブジェクト→JSON文字列
    jsonstring = json.dumps(jsonRow, ensure_ascii=False)
    print(jsonstring)


if __name__ == '__main__':
    main()