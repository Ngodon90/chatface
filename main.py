import google.generativeai as genai
import json
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAHgj4r56eEBO5CZBsVXPStVF9MWkeFjKzcwKL4jG8AmvZAKVsHgEsFxwBZApEZCWcePZC4fT2jYstK00fGRbBbckMEVVczZAeHPyh3ZCeZA5o1mMxuqwpI0pTrFHrZBqjAQLygD6GUCZCYSJEGpZC6NO3wTwnW2tHuRb3RG8GT4UW25WW7llMqpGsT7q5YgZAg8Tgs7"
VERIFY_TOKEN = "171119090216"


@app.route("/", methods=["GET"])
def home():
    return "Chatbot Facebook đang chạy!"

# Xác thực Webhook với Facebook
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Xác thực thất bại!", 403

# Xử lý tin nhắn từ Messenger
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if "message" in messaging_event:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]

                    # Gửi tin nhắn phản hồi
                    send_message(sender_id, f"Bạn vừa nói: {message_text}")

    return "OK", 200

# Hàm gửi tin nhắn
def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    requests.post(url, headers=headers, json=data)

# Đọc dữ liệu sản phẩm từ file JSON
with open("products.json", "r", encoding="utf-8") as f:
    product_data = json.load(f)

# Thiết lập API key
genai.configure(api_key="AIzaSyCeSZFV-F0lCXCVeImSimDN6qNafLI-erw")

# Hàm tìm kiếm sản phẩm trong dữ liệu JSON
def find_product_info(query):
    
   # print(f"Tìm kiếm: {query}")  # Debug: Xem câu hỏi
    for product in product_data:
        #print(f"Đang kiểm tra: {product}")  # Debug: Kiểm tra từng sản phẩm
        if "title" in product and product["title"].lower() in query.lower():
            return f'{product["title"]}: {product.get("description", "Không có mô tả")}. Giá: {product.get("price", "Không có giá")}. Xem chi tiết tại {product.get("link", "#")}'
    return None  # Trả về None nếu không tìm thấy sản phẩm


# Hàm gọi Google Gemini API
def ask_gemini(question):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Không dùng "model=" ở đây
    response = model.generate_content(question)
    return response.text


# Chatbot kết hợp dữ liệu và AIba
def chatbot_response(user_input):
    product_info = find_product_info(user_input)
    if product_info:  # Nếu tìm thấy sản phẩm
        return product_info
    else:  # Nếu không có dữ liệu trong JSON, gọi AI
        return ask_gemini(user_input)
    

if __name__ == "__main__":
    app.run(port= 8080, debug=True)