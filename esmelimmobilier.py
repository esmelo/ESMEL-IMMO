import streamlit as st
import joblib
import os
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="𝐄𝐒𝐌𝐄𝐋 IMMO™", layout="centered", page_icon="🏠")

@st.cache_resource
def charger_le_modele():
    chemin_actuel = os.path.dirname(__file__)
    chemin_modele = os.path.join(chemin_actuel, 'esmel_modele.joblib')
    if os.path.exists(chemin_modele):
        return joblib.load(chemin_modele)
    return None

model = charger_le_modele()

st.title("🏠 Estimez votre maison chez 𝐄𝐒𝐌𝐄𝐋 IMMO™")
st.write("Ajustez les paramètres pour obtenir une estimation immédiate.")

if model is None:
    st.error("❌ Erreur : Le fichier 'esmel_modele.joblib' est introuvable.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Emplacement")
        lat = st.number_input("Latitude", value=35.6)
        lon = st.number_input("Longitude", value=-119.5)
        st.divider()
        st.subheader("👥 Quartier")
        rev = st.slider("Revenu moyen (en 10k$)", 0.5, 15.0, 3.8)
        pop = st.number_input("Population totale", value=1400, step=100)

    with col2:
        st.subheader("🏗️ La Maison")
        age = st.slider("Âge de la maison (années)", 1, 52, 28)
        rms = st.slider("Nombre total de pièces", 1, 15, 5)
        brs = st.slider("Nombre de chambres", 1, 10, 1)
        occ = st.slider("Occupants par foyer", 1, 6, 3)

    st.write("") 
    
    if st.button("🚀 Calculer la valeur estimée", use_container_width=True):
        features = np.array([[rev, age, rms, brs, pop, occ, lat, lon]])
        prediction = model.predict(features)[0]
        
        prix_usd = prediction * 100000 
        taux_conversion = 450
        prix_fcfa = prix_usd * taux_conversion
    
        st.divider()
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="Prix en Dollars", value=f"{prix_usd:,.0f} $")
        with col_res2:
            format_fcfa = "{:,.0f}".format(prix_fcfa).replace(",", " ")
            st.metric(label="Prix en FCFA", value=f"{format_fcfa} XOF")
            
        st.balloons()
        st.success('✅ Estimation terminée !')

footer_luxe = """
<style>
/* Cache tout ce qui est possible */
header, footer, .stAppDeployButton, #MainMenu {
    display: none !important;
    visibility: hidden !important;
}

/* On remonte le contenu pour ne pas laisser de vide en haut */
.block-container {
    padding-top: 0px !important;
    margin-top: -30px !important;
    padding-bottom: 100px !important;
}

/* NOTRE BARRE QUI RECOUVRE TOUT EN BAS */
.custom-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 50px; /* Hauteur suffisante pour cacher le logo en dessous */
    background-color: #0E1117; /* Doit être la même couleur que le fond */
    color: #D4AF37;
    text-align: center;
    line-height: 50px;
    font-size: 14px;
    border-top: 2px solid #D4AF37;
    z-index: 999999999 !important; /* Priorité maximale */
}
</style>
<div class="custom-footer">
    © 2025 <b>𝐄𝐒𝐌𝐄𝐋 IMMO™</b> | L'Excellence Immobilière | 📍 Abidjan, CI
</div>
"""
st.markdown(footer_luxe, unsafe_allow_html=True)

# Script de secours pour tenter de supprimer l'élément par son tag
components.html(
    """
    <script>
    const hideSreamlit = () => {
        const pDoc = window.parent.document;
        const footer = pDoc.getElementsByTagName("footer")[0];
        if (footer) footer.style.display = "none";
        const header = pDoc.getElementsByTagName("header")[0];
        if (header) header.style.display = "none";
    }
    setInterval(hideSreamlit, 300);
    </script>
    """,
    height=0,
)
