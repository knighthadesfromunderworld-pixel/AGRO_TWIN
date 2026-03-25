import streamlit as st
import matplotlib.pyplot as plt
from gtts import gTTS
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Agro Twin - Manual", layout="wide")
st.title("🌱 Agro Twin: Manual Field Analysis")

# --- TRANSLATION MAP ---
translations = {
    "Long Term": "நீண்ட கால பயிர்",
    "Short Term": "குறுகிய கால பயிர்",
    "High Profit": "அதிவேக லாப பயிர்",
    "Teak": "தேக்கு மரம்", "Mahogany": "மஹோகனி",
    "Turmeric": "மஞ்சள்", "Groundnut": "நிலக்கடலை",
    "Banana": "வாழை", "Papaya": "பப்பாளி",
    "Land Use": "நிலப் பயன்பாடு",
    "Percentage": "சதவீதம்"
}

def get_recommendation(ph, n):
    lt = "Teak" if ph > 6.5 else "Mahogany"
    st_crop = "Turmeric" if n > 20 else "Groundnut"
    hp = "Banana" if ph > 6.0 else "Papaya"
    return lt, st_crop, hp

# --- UI LAYOUT ---
st.subheader("Enter Soil Data for 3 Squares")
col1, col2, col3 = st.columns(3)

with col1:
    ph1 = st.number_input("pH Level (S1)", 0.0, 14.0, 6.8)
    n1 = st.number_input("Nitrogen (S1)", 0, 50, 25)
with col2:
    ph2 = st.number_input("pH Level (S2)", 0.0, 14.0, 7.0)
    n2 = st.number_input("Nitrogen (S2)", 0, 50, 28)
with col3:
    ph3 = st.number_input("pH Level (S3)", 0.0, 14.0, 6.2)
    n3 = st.number_input("Nitrogen (S3)", 0, 50, 18)

if st.button("Generate Agro-Twin Report"):
    avg_ph = (ph1 + ph2 + ph3) / 3
    avg_n = (n1 + n2 + n3) / 3
    lt, st_crop, hp = get_recommendation(avg_ph, avg_n)

    # LAND PERCENTAGE LOGIC
    # We allocate 40% for the Tree, 35% for Cash Crop, and 25% for High Profit
    p_lt, p_st, p_hp = 40, 35, 25

    st.markdown("---")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("📋 Recommendations & Land Use")
        
        # Displaying English and Tamil with Percentages
        st.write(f"**{translations['Long Term']}:** {lt} — **{p_lt}%**")
        st.write(f"**{translations['Short Term']}:** {st_crop} — **{p_st}%**")
        st.write(f"**{translations['High Profit']}:** {hp} — **{p_hp}%**")
        
        # --- TAMIL VOICE OVER ---
        # "40 percent of land for Teak, 35 percent for Turmeric..."
        voice_text = (f"உங்கள் நிலத்தில் {p_lt} சதவீதம் {translations[lt]} வளர்க்கலாம். "
                      f"{p_st} சதவீதம் {translations[st_crop]} வளர்க்கலாம். "
                      f"{p_hp} சதவீதம் {translations[hp]} வளர்க்கலாம்.")
        
        tts = gTTS(text=voice_text, lang='ta')
        tts.save("final_report.mp3")
        st.audio("final_report.mp3")
        st.success("🔊 Tamil Voice-over Generated with Land Percentages!")

    with res_col2:
        st.subheader("📊 Land Allocation Chart")
        labels = [f"{lt} ({p_lt}%)", f"{st_crop} ({p_st}%)", f"{hp} ({p_hp}%)"]
        sizes = [p_lt, p_st, p_hp]
        colors = ['#2e7d32', '#fbc02d', '#d32f2f']
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        st.pyplot(fig)
