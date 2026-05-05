import requests, json

def get_weather(city):
    city = city.replace("台","臺")
    token = "rdec-key-123-45678-011121314"
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + token + "&format=JSON&locationName=" + str(city)
    Data = requests.get(url)
    if Data.status_code != 200:
        return "查詢失敗，請檢查縣市名稱或網路連線。"
    try:
        weather_data = json.loads(Data.text)
        if "records" not in weather_data or not weather_data["records"]["location"]:
            return "查無相關資料，請檢查縣市名稱。"
        Weather = weather_data["records"]["location"][0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
        Rain = weather_data["records"]["location"][0]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
        return Weather + "，降雨機率：" + Rain + "%"
    except (KeyError, IndexError, json.JSONDecodeError):
        return "資料解析失敗，請稍後再試。"

# 如果直接執行此腳本，保留原功能
if __name__ == "__main__":
    city = input("請輸入縣市：")
    print(get_weather(city))
