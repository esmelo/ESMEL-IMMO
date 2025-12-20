import streamlit as st
import joblib
import os
import numpy as np

st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">', unsafe_allow_html=True)
st.set_page_config(page_title="𝐄𝐒𝐌𝐄𝐋 IMMO™", layout="centered", page_icon="🏠")

@st.cache_resource
def charger_le_modele():
    if os.path.exists('esmel_modele.joblib'):
        return joblib.load('esmel_modele.joblib')
    return None

model = charger_le_modele()

st.title("🏠 Estimez le prix de votre maison chez 𝐄𝐒𝐌𝐄𝐋 IMMO™")
st.write("Ajustez les paramètres ci-dessous pour obtenir une estimation immédiate.")

if model is None:
    st.error("❌ Erreur : 'esmel_modele.joblib' introuvable.")
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
        rms = st.slider("Nombre de pièces", 1, 15, 5)
        brs = st.slider("Nombre de chambres", 1, 10, 1)
        occ = st.slider("Capacité d'occupation (pers.)", 1, 10, 3)

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
        st.success('✅ Estimation terminée ! Merci d\'utiliser 𝐄𝐒𝐌𝐄𝐋 IMMO™.')

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: #333;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    border-top: 1px solid #e6e6e6;
    z-index: 100;
}
</style>
<div class="footer">
    <p>© 2025- CV Pro par <b>𝐄𝐒𝐌𝐄𝐋 IMMO™</b> |Créer et entraîner par Kouton Vignon Esmel, M1 Data science & IA à l'UFR-MI de l'Université Félix Houphouët-Boigny. Contact : esmelyann@gmail.com / +225 0505411990 (Whatsapp et appel) | ⚠️Modèle basé sur les realités californiene | 📍 Abidjan, CI</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
  


