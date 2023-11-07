# Temel olarak Python'un resmi Docker imajını kullanıyoruz
FROM python:3.9
RUN pip install pymongo

# Çalışma dizinini belirliyoruz (isteğe bağlı)
WORKDIR /app

# Host makinedeki mevcut dizindeki gereksinimleri kopyalıyoruz
# (örneğin, requirements.txt dosyası içinde belirtilen bağımlılıklar)
COPY requirements.txt .

# Gerekli bağımlılıkları yükledik
RUN pip install --no-cache-dir -r requirements.txt

# Geri kalan dosyaları mevcut dizine kopyaladık
COPY . .

# Uygulama portunu belirtin (eğer uygulamanız belirli bir port dinliyorsa)
EXPOSE 8080

# Uygulamayı çalıştırın
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
