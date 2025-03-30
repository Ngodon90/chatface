import requests
from bs4 import BeautifulSoup
import json

# URL của trang sản phẩm
URL = "https://hunonic.com/thiet-bi-dien-thong-minh/"

# Fake User-Agent để tránh bị chặn
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Gửi yêu cầu HTTP
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Tìm tất cả sản phẩm trên trang
products = soup.find_all("div", class_="product-small")

# Kiểm tra nếu không tìm thấy sản phẩm
if not products:
    print("⚠️ Không tìm thấy sản phẩm. Kiểm tra lại class HTML hoặc website có chặn bot không.")
    exit()

# Danh sách lưu thông tin sản phẩm
product_list = []

# Duyệt qua từng sản phẩm để lấy thông tin
for product in products:
    try:
        name_tag = product.find("p", class_="name product-title")
        name = name_tag.text.strip() if name_tag else "Không có tên"

        price_tag = product.find("span", class_="woocommerce-Price-amount")
        price = price_tag.text.strip() if price_tag else "Không có giá"

        link_tag = product.find("a")
        link = link_tag["href"] if link_tag else "Không có link"

        image_tag = product.find("img")
        image = image_tag["src"] if image_tag else "Không có ảnh"

        # Gửi request đến trang chi tiết sản phẩm để lấy mô tả
        if link != "Không có link":
            product_response = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_response.text, "lxml")

            description_tag = product_soup.find("div", class_="product-short-description")
            description = description_tag.text.strip() if description_tag else "Không có mô tả"
        else:
            description = "Không có mô tả"

        # Thêm vào danh sách sản phẩm
        product_list.append({
            "name": name,
            "price": price,
            "link": link,
            "image": image,
            "description": description
        })

        print(f"✅ Đã lấy: {name}")
    except Exception as e:
        print(f"⚠️ Lỗi khi lấy dữ liệu sản phẩm: {e}")
        continue  # Nếu lỗi, bỏ qua sản phẩm đó

# Lưu vào file JSON
if product_list:
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(product_list, f, ensure_ascii=False, indent=4)
    print(f"✅ Đã lưu {len(product_list)} sản phẩm vào products.json")
else:
    print("⚠️ Không có sản phẩm nào được lưu.")
