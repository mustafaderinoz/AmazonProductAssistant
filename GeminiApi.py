import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import streamlit as st

# --- AYARLAR ---
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def searchbox_metin_olustur(girdi):
    prompt = f"""
            Kullanıcı bir ürün arıyor. Bu metni Amazon.com.tr arama çubuğuna yazılacak
            EN KISA ve EN ETKİLİ anahtar kelimelere dönüştür.

            KURALLAR:
            - Gereksiz kelimeleri çıkar: "istiyorum", "alacağım", "bana bul", "uygun fiyatlı" vb.
            - Sadece ürün adı + kritik teknik özellikleri bırak.
            - Renk, boyut, model, güç, kapasite, teknik standart gibi gerçekten işe yarayan özellikleri ekle.
            - Amazonun anlamayacağı doğal konuşma ifadelerini temizle.
            - Eğer kullanıcının teknik talebi tam karşılanamıyorsa, ona uygun **kaliteli marka + genel kabul gören teknik özellik** yaz.
            - Maksimum 3–6 kelimelik kısa bir arama çıktısı üret.
            - ÇIKTI sadece anahtar kelimeler olmalı (cümle kurma, ekstra açıklama YOK).
            
            Örnek 1:
            Girdi: "Su geçirmez kol saati istiyorum, spor yaparken kullanacağım."
            Çıktı: su geçirmez 50m spor kol saati
            
            Örnek 2:
            Girdi: "RDR2 oyununu akıcı şekilde oynayabileceğim fiyatı uygun laptop arıyorum"
            Çıktı: gaming laptop rtx 3050 16gb

            Örnek 3:
            Girdi:Kız arkadaşıma huawei akıllı saat alacağım kibar olsun
            Çıktı: Huawei akıllı saat 41mm kadın
            
            KULLANICI GİRDİSİ: "{girdi}"
            SADECE çıktılardaki gibi cevap döndür onun haricinde başka hiçbir şey yazma.
            """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Hata: {e}")
        return girdi

def en_iyi_urunleri_sec(kullanici_istegi,urun_listesi):
    # Gemini'ye göndermek için listeyi sadeleştiriyoruz (resim linki vs. token harcamasın diye)
    analiz_listesi = []
    for urun in urun_listesi:
        analiz_listesi.append({
            "id": urun['id'],
            "ad": urun['ad'],
            "fiyat": urun['fiyat'],
            "puan": urun['puan'],
            "yorum_sayisi": urun['yorum_sayisi']
        })

    prompt = f"""
    Bir alışveriş asistanısın.
    KULLANICI İSTEĞİ: "{kullanici_istegi}"
    
    Aşağıdaki ürün listesinden, kullanıcının isteğine EN UYGUN olan 5 ile 10 arası ürünü seç.
    
    ÜRÜN LİSTESİ:
    {json.dumps(analiz_listesi, ensure_ascii=False)}
    
    KURALLAR:
    1. Kullanıcının bütçe imasına, kalite beklentisine ve teknik isteğine bak.
    2. SADECE seçilen ürünlerin 'id' numaralarını içeren bir JSON listesi döndür.
    3. Başka hiçbir açıklama yazma.
    
    Örnek Cevap Formatı:
    [1, 4, 6, 12, 15]
    """
    
    try:
        response = model.generate_content(prompt)
        temiz_cevap = response.text.replace("```json", "").replace("```", "").strip()
        secilen_idler = json.loads(temiz_cevap)
        
        # ID'leri eşleşen tam ürün verilerini (resim, link dahil) geri döndür
        filtrelenmis = [u for u in urun_listesi if u['id'] in secilen_idler]
        return filtrelenmis
    except Exception as e:
        st.error(f"Filtreleme hatası: {e}")
        return urun_listesi[:5] # Hata olursa ilk 5'i göster

def yorum_ozeti_olustur(yorumlar, urun_adi,girdi):
    """Yorumları AI ile özetler"""
    if not yorumlar:
        return "Yorum bulunamadı."
    
    yorumlar_text = "\n\n".join([f"- {yorum}" for yorum in yorumlar])
    
    prompt = f"""
    Aşağıdaki ürün hakkındaki müşteri yorumlarını analiz et ve özet bir rapor hazırla.
    
    ÜRÜN: {urun_adi}
    Ürünü satın almak isteyen kullanıcının isteği:{girdi}
    
    YORUMLAR:
    {yorumlar_text}
    
    RAPOR FORMATI:
    1. **Genel Değerlendirme:** (2-3 cümle)
    2. **Artıları:** (Madde madde)
    3. **Eksileri:** (Madde madde)
    4. **Sonuç ve Öneri:** (1-2 cümle)
    
    Kısa ve öz yaz.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Özet oluşturulamadı: {e}"