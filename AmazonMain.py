import streamlit as st
import GeminiApi
import AmazonScraper
import time

st.set_page_config(layout="wide", page_title="Amazon AI Arama")

st.markdown("""
<style>
.header-container {
    background: linear-gradient(90deg, #5b6cf9 0%, #7a4ba2 100%);
    padding: 40px; border-radius: 15px; text-align: center; color: white;
    margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.header-title {
    font-size: 40px; font-weight: bold; margin: 0; display: flex;
    align-items: center; justify-content: center; gap: 15px;
}
.header-subtitle { font-size: 18px; margin-top: 10px; opacity: 0.9; font-weight: 300; }
div.stButton > button {
    background-color: white; color: #333; border: 1px solid #ddd;
    width: 100%; border-radius: 8px;
}
div.stButton > button:hover { border-color: #5b6cf9; color: #5b6cf9; }
div.stButton > button[kind="primary"] {
    background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
    color: white; border: none; border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all 0.3s ease;
    font-weight: bold; letter-spacing: 0.5px;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(45deg, #2575fc 0%, #6a11cb 100%);
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 20px rgba(37,117,252,0.4);
}
div.stButton > button[kind="primary"]:active {
    transform: translateY(1px); box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.stTextInput > div > div > input { border-radius: 8px; }
</style>

<div class="header-container">
    <div class="header-title">🛒 Amazon Ürün Asistanı</div>
    <div class="header-subtitle">Yapay Zeka Destekli Akıllı Alışveriş</div>
</div>
""", unsafe_allow_html=True)

if 'secilen_urunler' not in st.session_state: st.session_state.secilen_urunler = []
if 'yorum_ozeti' not in st.session_state: st.session_state.yorum_ozeti = {}

container = st.container()
with container:
    with st.form("arama_formu", clear_on_submit=False):
        col_input, col_btn = st.columns([6, 1])
        with col_input:
            girdi = st.text_input(
                "Arama",
                placeholder="Ne aramak istersiniz? (örn: oyun bilgisayarı, bluetooth kulaklık...)",
                label_visibility="collapsed"
            )
        with col_btn:
            buton = st.form_submit_button("🔍 Ara", width="stretch")

if buton and girdi:
    st.session_state.secilen_urunler = []
    st.session_state.yorum_ozeti = {}

    with st.status("🚀 İşlemler yapılıyor...", expanded=True) as status:
        st.write("📝 Anahtar kelimeler oluşturuluyor...")
        arama_metni = GeminiApi.searchbox_metin_olustur(girdi)
        st.write(f"**Ara:** `{arama_metni}`")

        st.write("🛒 Amazon'dan veriler çekiliyor...")
        ham_veriler = AmazonScraper.verileri_getir(arama_metni)
        st.write(f"📦 Toplam {len(ham_veriler)} ürün bulundu.")

        if len(ham_veriler) > 0:
            st.write("🧠 Yapay zeka en iyi ürünleri seçiyor...")
            secilenler = GeminiApi.en_iyi_urunleri_sec(girdi, ham_veriler)
            st.session_state.secilen_urunler = secilenler
            status.update(label="✅ Arama ve Analiz Tamamlandı!", state="complete", expanded=False)
        else:
            status.update(label="❌ Ürün Bulunamadı", state="error", expanded=True)
            st.error("Hiç ürün bulunamadı. Lütfen daha genel bir arama yapın.")

if len(st.session_state.secilen_urunler) > 0:
    st.markdown("---")
    st.subheader(f"✅ Sizin için seçilen {len(st.session_state.secilen_urunler)} ürün:")
    st.write("")

    for urun in st.session_state.secilen_urunler:
        with st.container():
            col1, col2 = st.columns([1, 4])

            with col1:
                if urun.get('gorsel'): st.image(urun['gorsel'], width="stretch")
                else: st.write("📷 Görsel Yok")

            with col2:
                st.markdown(f"### {urun['ad']}")
                st.write(f"**💰 Fiyat:** {urun['fiyat']}")
                st.write(f"**⭐ Puan:** {urun.get('puan','N/A')} | **💬 Yorum Sayısı:** {urun.get('yorum_sayisi','0')}")
                st.markdown(f"**[🔗 Ürünü Amazon'da İncele]({urun['link']})**")
                st.write("")

                analiz_butonu = st.button(
                    "✨ AI ile Yorumları Analiz Et & Özetle",
                    key=f"btn_{urun.get('id', urun['link'])}",
                    type="primary",
                    help="Gemini, ürünün yorumlarını okur ve artılarını/eksilerini özetler."
                )

                if analiz_butonu:
                    with st.spinner("Yorumlar analiz ediliyor..."):
                        yorumlar = AmazonScraper.yorumlari_cek(urun['link'], max_yorum=10)
                        if yorumlar:
                            print(f"\n--- {urun['ad']} İçin Çekilen Yorumlar ---")
                            for i in yorumlar: print(f"- {i}")
                            print("------------------------------------------\n")
                            ozet = GeminiApi.yorum_ozeti_olustur(yorumlar, urun['ad'],girdi)
                            st.session_state.yorum_ozeti[urun['link']] = ozet
                        else:
                            st.warning("Yorum bulunamadı veya çekilemedi.")

                if urun['link'] in st.session_state.yorum_ozeti:
                    st.info(f"**🤖 AI Özeti:**\n\n{st.session_state.yorum_ozeti[urun['link']]}")

        st.divider()
