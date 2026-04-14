import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# 1. 初始化 Firebase
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection("靜宜資管")

def search_data():
    # 2. 讓使用者輸入搜尋欄位與關鍵字
    field = input("請輸入要搜尋的欄位 (例如: name, mail): ").strip()
    keyword = input(f"請輸入要搜尋的關鍵字 ({field}): ").strip()

    print(f"\n正在搜尋 {field} 為 '{keyword}' 的資料...\n" + "-"*30)

    try:
        # 3. 執行查詢 (使用 FieldFilter 進行完全比對)
        query = collection_ref.where(filter=FieldFilter(field, "==", keyword))
        docs = query.get()

        # 4. 檢查是否有結果
        count = 0
        for doc in docs:
            count += 1
            print(f"文件 ID: {doc.id}")
            print(f"文件內容: {doc.to_dict()}")
            print("-" * 30)

        if count == 0:
            print("找不到符合條件的資料。")
        else:
            print(f"搜尋完畢，共找到 {count} 筆資料。")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    search_data()