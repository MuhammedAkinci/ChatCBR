from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import chatCevapAl, kaydetSoruCevap
import os

env = os.environ.get('ENVIRONMENT', 'development')

app = Flask(__name__)
CORS(app)

@app.route('/')
def frontendIndex():
    return render_template(
        'index.html',
        logo_image="/static/images/chatcbr3.png",
        name="ChatCBR"
    )

@app.route("/api/sor")
def soruSor():
    soru = request.args.get("soru")
    if not soru:
        return jsonify({"ok": False, "message": "Soru girmediniz."})

    try:
        cevap = chatCevapAl(soru)
        if cevap is None:
            return jsonify({"ok": False, "message": "Cevap alınamadı."})
        else:
            # Soru ve cevabı MongoDB'ye kaydet
            kaydetSoruCevap(soru, cevap)
            return jsonify({"ok": True, "cevap": cevap})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})

if __name__ == "__main__":
    app.run()
