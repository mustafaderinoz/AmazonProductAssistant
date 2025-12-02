# 🛒 Amazon Ürün Asistanı

## Yapay Zekâ destekli Amazon ürün arama ve değerlendirme uygulamasıdır. Streamlit ile modern bir arayüz sunar, Selenium ile Amazon'dan veri çeker ve Google Gemini 2.5 Flash API ile anahtar kelime oluşturma, en iyi ürünleri seçme ve kullanıcı yorumlarını özetleme gibi akıllı işlemler gerçekleştirir.

## 🚀 Özellikler

* 🔎 Anahtar kelime oluşturma (Gemini) — kullanıcının doğal dil girdisini Amazon arama çubuğuna uygun kısa anahtar kelimelere dönüştürür
* 🛒 Amazon ürün listeleme (Selenium) — başlık, fiyat, puan, yorum sayısı, görsel ve link bilgilerini çeker
* 🧠 Gemini 2.5 Flash API ile **en iyi ürünleri seçme** 
* ✨ AI destekli yorum analizi ve özetleme
* 🎨 Modern Streamlit + CSS arayüz (başlık, buton stilleri, input vs.)
* ⚠️ Amazon scraping için hata/exception handling ve chromedriver otomatik kurulum

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji                                                                                              | Açıklama                            |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------- |
| <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white">          | Projenin ana programlama dili       |
| <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white">    | Web arayüzü                         |
| <img src="https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white">      | Web scraping / otomasyon            |
| <img src="https://img.shields.io/badge/chromedriver--autoinstaller-0A0A0A?style=flat">                 | Chromedriver otomatik kurulumu      |
| <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white"> | Yapay zekâ modeli (text generation) |
| <img src="https://img.shields.io/badge/python--dotenv-4E9A06?style=flat">                              | .env yönetimi (API anahtarı)        |

---

## 📦 Proje Yapısı

```
📦 amazon-asistan
│
├── main.py               # Streamlit arayüzü ve uygulama akışı (ilk kod bloğu)
├── AmazonScraper.py      # Selenium ile Amazon'dan veri çekme ve yorumları alma
├── GeminiApi.py          # Google Gemini entegrasyonu (anahtar kelime, seçim, özet)
├── requirements.txt      # Gerekli Python paketleri
├── .env                  # API anahtarları (API_KEY)
├── screenshots/          # Arayüz ekran görüntüleri
└── README.md
```

---

## 🛠️ Gerekli Kurulumlar

### 1️⃣ Sanal Ortam Oluşturma

```bash
python -m venv venv
```

### 2️⃣ Sanal Ortamı Aktif Etme

```bash
# Windows
.\venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3️⃣ Gerekli Kütüphanelerin Kurulumu

Tercih edilen yol: proje kökünde `requirements.txt` dosyası varsa:

```bash
pip install -r requirements.txt
```

Eğer `requirements.txt` yoksa şu paketleri kurun:

```bash
pip install streamlit selenium chromedriver-autoinstaller google-generativeai python-dotenv
```

> Not: Selenium sürücüsünü `chromedriver-autoinstaller` otomatik yüklemektedir. Sunucuda/CI ortamında headless mod ve ek bağımlılıklar (ör. libnss, xvfb) gerekebilir.

### 🔑 API Anahtarı Ekleme

Proje klasörüne `.env` adında bir dosya ekleyin ve içine aşağıdaki satırı koyun:

```bash
API_KEY="YOUR_API_KEY"
```

Bu API_KEY, Gemini / Google Generative API anahtarınız olmalıdır.

### ▶️ Uygulamayı Çalıştırma

```bash
streamlit run main.py
```

---

---

## 📱 Ekran Görüntüleri

|                                       |
| ------------------------------------- |
| ![Arayüz 1](screenshots/asistan1.png) |

---

## | ![Arayüz 2](screenshots/asistan2.png) |



---

