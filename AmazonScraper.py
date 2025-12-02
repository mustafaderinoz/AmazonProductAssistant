from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from time import sleep
import streamlit as st # Hata mesajları için

def verileri_getir(arama_kelimesi):
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    urunler_data = []
    
    try:
        # 1. Amazon Ana Sayfasına Git
        driver.get("https://www.amazon.com.tr/")
        wait = WebDriverWait(driver, 10)
        
        # 2. Çerez Kabul Etme
        try:
            accept_cookies = wait.until(EC.element_to_be_clickable((By.ID, "sp-cc-accept")))
            accept_cookies.click()
        except:
            pass

        # 3. Arama Yapma
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.send_keys(arama_kelimesi)
        search_box.send_keys(Keys.ENTER)
        
        # 4. Filtreleme (Sıralama: Çok Satanlar)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "a-autoid-0-announce"))).click()
            wait.until(EC.element_to_be_clickable((By.ID, "s-result-sort-select_5"))).click()
            sleep(2)
        except:
            pass
        
        sleep(3) # Ürünlerin yüklenmesi için bekleme

        # 5. Veri Çekme İşlemi
        urun_kartlari = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        
        sayac = 0
        for kart in urun_kartlari:
            try:
                # A. BAŞLIK
                try:
                    baslik = kart.find_element(By.XPATH, './/h2//span').text
                except:
                    continue # Başlığı yoksa geç

                # B. FİYAT
                try:
                    fiyat_tam = kart.find_element(By.CLASS_NAME, 'a-price-whole').text
                    fiyat = f"{fiyat_tam} TL"
                except:
                    fiyat = "Fiyat Görünmüyor"

                # C. ÜRÜN LİNKİ
                try:
                    ham_link = kart.find_element(By.XPATH, './/h2/parent::a').get_attribute("href")
                    if "/dp/" in ham_link:
                        asin = ham_link.split('/dp/')[1].split('/')[0]
                        link = f"https://www.amazon.com.tr/dp/{asin}"
                    else:
                        link = ham_link.split('?')[0]
                except:
                    link = "#"

                # D. ÜRÜN GÖRSELİ
                try:
                    gorsel_url = kart.find_element(By.CSS_SELECTOR, '.s-image').get_attribute('src')
                except:
                    gorsel_url = ""

                # E. PUAN
                try:
                    puan = kart.find_element(By.CLASS_NAME, "a-icon-alt").get_attribute("textContent")
                except:
                    puan = "Puan Yok"

                # F. DEĞERLENDİRME SAYISI
                try:
                    yorum_sayisi = kart.find_element(By.XPATH, './/span[contains(@class, "s-underline-text")]').text
                except:
                    yorum_sayisi = "0"
                
                # Listeye Ekle
                urunler_data.append({
                    "id": sayac, # Gemini seçimi için ID
                    "ad": baslik,
                    "fiyat": fiyat,
                    "puan": puan,
                    "yorum_sayisi": yorum_sayisi,
                    "link": link,
                    "gorsel": gorsel_url
                })
                sayac += 1
                
            except:
                continue
                
    except Exception as e:
        st.error(f"Selenium Hatası: {e}")
    finally:
        driver.quit()
        
    return urunler_data

def yorumlari_cek(urun_link, max_yorum=10):
    """Ürün linkinden yorumları çeker"""
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    
    yorumlar = []
    
    try:
        driver.get(urun_link)
        wait = WebDriverWait(driver, 10)
        sleep(2)
        
        # Tüm yorumları göster butonuna tıkla
        try:
            tum_yorumlar_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[@data-hook="see-all-reviews-link-foot"]'))
            )
            tum_yorumlar_btn.click()
            sleep(3)
        except:
            pass
        
        # Yorumları çek
        yorum_elementleri = driver.find_elements(By.XPATH, '//span[@data-hook="review-body"]')
        
        for i, yorum_elem in enumerate(yorum_elementleri[:max_yorum]):
            try:
                yorum_metni = yorum_elem.text.strip()
                if yorum_metni:
                    yorumlar.append(yorum_metni)
            except:
                continue
                
    except Exception as e:
        st.warning(f"Yorum çekilemedi: {e}")
    finally:
        driver.quit()
    
    return yorumlar