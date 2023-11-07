import requests
from bs4 import BeautifulSoup

def wikipedia_cevap_al(soru):
    try:
        # Kullanıcının girdiği soruya göre Wikipedia'da arama yapacak URL oluşturuluyor
        url = f"https://tr.wikipedia.org/w/index.php?search={soru.replace(' ', '+')}"
        
        # Wikipedia'ya istek gönderiliyor ve cevap alınıyor
        response = requests.get(url)
        
        # İstek başarılı ise devam ediliyor
        if response.status_code == 200:
            # Gelen içerik BeautifulSoup ile analiz ediliyor
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Arama sonuçlarının bulunduğu bölümü seçiyoruz
            sonuclar = soup.find_all('div', class_='mw-search-result-heading')
            
            # Arama sonucu varsa devam ediliyor
            if sonuclar:
                # İlk sonucun başlığını ve linkini çekiyoruz
                ilk_sonuc = sonuclar[0]
                sayfa_baslik = ilk_sonuc.find('a').text
                sayfa_linki = "https://tr.wikipedia.org" + ilk_sonuc.find('a')['href']

                # İlgili sayfaya yeni bir istek yapılıyor
                sayfa_response = requests.get(sayfa_linki)
                
                # Sayfa isteği başarılı ise devam ediliyor
                if sayfa_response.status_code == 200:
                    # Sayfa içeriği BeautifulSoup ile analiz ediliyor
                    sayfa_soup = BeautifulSoup(sayfa_response.content, 'html.parser')
                    
                    # Sayfanın içeriğini belirli bir sınıftan alıyoruz
                    icerik = sayfa_soup.find('div', class_='mw-parser-output').text.strip()
                    
                    # Sayfa başlığını ve içeriğini döndürüyoruz
                    return sayfa_baslik, icerik
                else:
                    raise Exception(f"Web sitesine ulaşılamıyor. Hata kodu: {sayfa_response.status_code}")
            else:
                return None, None
        else:
            raise Exception(f"Web sitesine ulaşılamıyor. Hata kodu: {response.status_code}")
    except Exception as e:
        raise Exception(f"Hata oluştu: {e}")

