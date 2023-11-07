import openai
from pymongo import MongoClient
from my_secrets import CHATGPT_API_KEY

openai.api_key = CHATGPT_API_KEY

# MongoDB bağlantısını oluşturun
try:
    client = MongoClient('mongodb+srv://cuberium:cuberiumm@cluster0.v5kohjk.mongodb.net/')  # MongoDB bağlantı URL'sini güncelleyin
    db = client['ChatCBR_db']  # Veritabanı adını değiştirin (varsa)
except Exception as e:
    print(f"MongoDB bağlantısı oluşturulurken hata oluştu: {str(e)}")

def kaydetSoruCevap(soru, cevap):
    try:
        # Soru ve cevapları veritabanına kaydedin
        sorular_collection = db['sorular']  # Sorular koleksiyonunu kullanın
        cevaplar_collection = db['cevaplar']  # Cevaplar koleksiyonunu kullanın

        sorular_collection.insert_one({"soru": soru})
        cevaplar_collection.insert_one({"cevap": cevap})
        print("Soru ve cevap veritabanına başarıyla kaydedildi.")
    except Exception as e:
        print(f"Veritabanına kayıt yapılırken hata oluştu: {str(e)}")


def chatCevapAl(message):
    try:
        messages = [
            {"role": "user", "content": message}
        ]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content

        # Soru ve cevabı veritabanına kaydet
        kaydetSoruCevap(message, reply)

        return reply
    except Exception as e:
        print(f"ChatCevapAl işlevinde hata oluştu: {str(e)}")
        return None