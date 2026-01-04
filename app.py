import streamlit as st
import pandas as pd
import pickle
import numpy as np

# ==============================
#   SEUL STYLE CONSERVÉ : Barre latérale gauche
# ==============================
st.markdown(
    """
    <style>
    /* Barre latérale gauche uniquement */
    .sidebar-left {
        position: fixed;
        top: 80px;
        left: 0;
        bottom: 0;
        width: 260px;
        background: linear-gradient(to bottom, #334155, #1e293b);
        color: white;
        padding: 2rem 1.8rem;
        font-family: 'Segoe UI', sans-serif;
        font-size: 0.95rem;
        box-shadow: 6px 0 15px rgba(0,0,0,0.35);
        z-index: 900;
        overflow-y: auto;
    }

    .sidebar-left h3 {
        color: #60a5fa;
        margin-bottom: 1.4rem;
        font-size: 1.3rem;
        border-bottom: 1px solid #475569;
        padding-bottom: 0.8rem;
    }

    .sidebar-left ul {
        list-style: none;
        padding: 0;
        margin: 1.2rem 0;
    }

    .sidebar-left li {
        margin: 0.8rem 0;
        color: #cbd5e1;
    }

    .sidebar-left strong {
        color: #93c5fd;
    }

    /* Décalage du contenu principal */
    .main-content {
        margin-left: 280px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
#   UI SIMPLE
# ==============================
st.title(" Attack Type Detection")
st.write("Votre bouclier contre les menaces en ligne")

st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.write("Entrez le fichier Excel à analyser :")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# ==============================
#   CLASSES
# ==============================
attack_type_dict = {
    'ARP_poisioning': np.int64(0),
    'DDOS_Slowloris': np.int64(1),
    'DOS_SYN_Hping': np.int64(2),
    'MQTT_Publish': np.int64(3),
    'Metasploit_Brute_Force_SSH': np.int64(4),
    'NMAP_FIN_SCAN': np.int64(5),
    'NMAP_OS_DETECTION': np.int64(6),
    'NMAP_TCP_scan': np.int64(7),
    'NMAP_UDP_SCAN': np.int64(8),
    'NMAP_XMAS_TREE_SCAN': np.int64(9),
    'Thing_Speak': np.int64(10),
    'Wipro_bulb': np.int64(11)
}

benign_classes = {'MQTT_Publish', 'Thing_Speak', 'Wipro_bulb'}

st.markdown("### Signification des classes Attack_type")
for attack, code in attack_type_dict.items():
    st.markdown(f"- **{attack}** : code = `{code}`")

# ==============================
#   CHARGEMENT MODÈLE
# ==============================
@st.cache_resource
def load_pipeline():
    try:
        with open("pipeline1.pkl", "rb") as f:
            pipeline1 = pickle.load(f)
        with open("final_model1.pkl", "rb") as f:
            le = pickle.load(f)
        return pipeline1, le
    except Exception as e:
        st.error(f"Erreur lors du chargement des fichiers pickle : {e}")
        raise e

pipeline, le= load_pipeline()

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
#   BARRE LATÉRALE GAUCHE
# ==============================
st.markdown(
    """
    <div class="sidebar-left">
        <h3>Types d'attaques détectées</h3>
        <ul>
            <li><strong>Attaques réseau de bas niveau :</strong><br>ARP_poisoning</li>
            <li><strong>Attaques par déni de service :</strong><br>DDOS_Slowloris,<br>DOS_SYN_Hping</li>
            <li><strong>Techniques de reconnaissance Nmap :</strong><br>NMAP_FIN_SCAN,<br>NMAP_OS_DETECTION,<br>NMAP_TCP_scan,<br>NMAP_UDP_SCAN,<br>NMAP_XMAS_TREE_SCAN</li>
            <li><strong>Force brute :</strong><br>Metasploit_Brute_Force_SSH</li>
            <li><strong>Trafic IoT légitime :</strong><br>MQTT_Publish,<br>Thing_Speak,<br>Wipro_bulb</li>
        </ul>
        <p style="margin-top: 2rem; font-size: 0.9rem; color: #94a3b8;">
            Précision moyenne du modèle : 94-97%
        </p>
    </div>
    """,
    unsafe_allow_html=True
)