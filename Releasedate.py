# _*_ coding:UTF-8 _*_
import json
from retry import retry
from urllib.request import urlopen
from bs4 import BeautifulSoup

## brand-x リリースカレンダーURL
url="http://www.brand-x.jp/page/38"

def main():
    try:
        calendar=getVcalendar()
        print(calendar)
    except:
        import traceback
        traceback.print_exc()         
        print("カレンダー情報が取得できませんでした")

## ヴィジュアル系カレンダーを読み込んでJSON化
#@retry(tries=4, delay=5, backoff=2)
def getVcalendar():
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
    data=[]
    for row in rows:
        jsonRow = []
        i=0
        for cell in row.findAll(['td', 'th']):            
                title= ""
                if i == 0:
                    header="date"
                elif i == 1:
                    header="artist"
                elif i == 2:
                    header="title"
                elif i == 3:
                    header="media"
                elif i == 4:
                    header="price"   
                jsonRow.append([header,cell.get_text()])
                i=i+1
        data.append(jsonRow)
    # Pythonオブジェクト→JSON文字列
    jsondata = json.dumps(data, ensure_ascii=False)
    return jsondata
 

if __name__ == '__main__':
    main()