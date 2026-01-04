import streamlit as st
import pandas as pd
import pickle
import numpy as np

# ==============================
#   SEUL STYLE CONSERVÉ : Barre latérale gauche
# ==============================
st.set_page_config(
    page_title="IoT Intrusion Detection (RT-IoT2022)",
    page_icon="🛡️",
    layout="wide"
)
col1, col2 = st.columns([1, 3])  # ajuster la proportion
with col2:
# Titre et sous-titre
    st.markdown("""
<h1 style="
text-align:center;
color: #000000;
font-weight: 700;
font-family: 'Segoe UI', sans-serif;
">
🛡️ IoT Intrusion Detection System
</h1>
""", unsafe_allow_html=True)



st.markdown("""
    ### Mini-projet ML
    Cette application utilise des **modèles de Machine Learning** pour détecter
    les attaques réseau dans des environnements **IoT** à partir du dataset **RT-IoT2022**.
    
    """)
  # ==============================
# DICTIONNAIRE DES CLASSES
# ==============================
attack_type_dict = {
    'ARP_poisioning 🖧': 0,
    'DDOS_Slowloris 💥': 1,
    'DOS_SYN_Hping ⚡': 2,
    'MQTT_Publish 📡': 3,
    'Metasploit_Brute_Force_SSH 🔐': 4,
    'NMAP_FIN_SCAN 🕵️‍♂️': 5,
    'NMAP_OS_DETECTION 🖥️': 6,
    'NMAP_TCP_scan 🔎': 7,
    'NMAP_UDP_SCAN 🧭': 8,
    'NMAP_XMAS_TREE_SCAN 🎄': 9,
    'Thing_Speak 🌐': 10,
    'Wipro_bulb 💡': 11
}

# ==============================
#   UI SIMPLE
# ==============================
st.title(" Attack Type Detection")
st.write("Votre bouclier contre les menaces en ligne")

st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.write("Entrez le fichier Excel à analyser :")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])


         
st.markdown("### 🔍 Signification des classes **Attack_type**")
for attack, code in attack_type_dict.items():
    st.markdown(f"- **{attack}** : code = `{code}`")

st.markdown("""
<hr style="
border:none;
height:1px;
background:linear-gradient(to right, transparent, #94a3b8, transparent);
margin:30px 0;
">
""", unsafe_allow_html=True)
# ==============================
#   CHARGEMENT MODÈLE
# ==============================
@st.cache_resource
def load_pipeline():
    try:
        with open("pipeline1.pkl", "rb") as f:
            pipeline1 = pickle.load(f)
        with open("final_model1.pkl", "rb") as f:
            label_encoder = pickle.load(f)
        return pipeline1, label_encoder
    except Exception as e:
        st.error(f"Erreur lors du chargement des fichiers pickle : {e}")
        raise e

pipeline, label_encoder = load_pipeline()

# ==============================
#   PRÉDICTION
# ==============================
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Aperçu des données")
    st.write(df.head())

    predictions = pipeline.predict(df)
    decoded_predictions = label_encoder.inverse_transform(predictions)

    st.subheader("Classes Prédites")

    # Tableau simple sans style : juste une liste numérotée
    for i, pred in enumerate(decoded_predictions, 1):
        if pred in benign_classes:
            st.write(f"{i}. {pred} → Trafic légitime")
        else:
            st.write(f"{i}. {pred} → ATTAQUE DÉTECTÉE")

    # Optionnel : Probabilités (tableau normal Streamlit)
    if hasattr(pipeline.named_steps["classifier"], "predict_proba"):
        probs = pipeline.predict_proba(df)
        proba_df = pd.DataFrame(probs, columns=label_encoder.classes_)
        st.subheader("Probabilités de Prédiction")
        st.dataframe(proba_df)

else:
    st.info("Veuillez uploader un fichier Excel (.xlsx) pour commencer la prédiction.")

st.markdown('</div>', unsafe_allow_html=True)
# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShFS5Aos0PhDsLhfPJL6Irlm3GqgHD6bCCZg&s",
        width=250
    )
    st.header("📥 Chargement des données")
    uploaded_file = st.file_uploader(
        "Uploader un fichier CSV ou Excel",
        type=["csv", "xlsx"]
    )
    st.divider()
    st.subheader("🎓 Contexte Académique")
    st.info("""
    **Réalisée par :** Siham Bouzagrar 
     
    **Module :** Machine Learning / Data Science
      
    **Encadrant :** Mr. Abdelhamid FADIL  
    
    """)