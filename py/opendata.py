import requests, json

def search_road(road_name):
    url = "https://datacenter.taichung.gov.tw/swagger/OpenData/a1b899c0-511f-4e3d-b22b-814982a97e41"
    Data = requests.get(url, verify=False)
    JsonData = json.loads(Data.text)
    Result = ""
    for item in JsonData:
        if road_name in item["路口名稱"]:
            Result += item["路口名稱"] + "：發生" + item["總件數"] + "件，主因是" + item["主要肇因"] + "\n\n"
    if Result == "":
        Result = "抱歉，查無相關資料！"
    return Result

# 如果直接執行此腳本，保留原功能
if __name__ == "__main__":
    Road = input("請輸入欲查詢的路名：")
    print(search_road(Road))
