import streamlit as st
import joblib
import os
import numpy as np

st.set_page_config(page_title="𝐄𝐒𝐌𝐄𝐋 IMMO™", layout="centered")

@st.cache_resource
def charger_le_modele():
    if os.path.exists('esmel_modele.joblib'):
        return joblib.load('esmel_modele.joblib')
    return None

model = charger_le_modele()

st.title("🏠 Estimez le prix de votre maison chez 𝐄𝐒𝐌𝐄𝐋 IMMO™")
st.write("Ajustez les paramètres ci-dessous pour obtenir une estimation immédiate.")

if model is None:
    st.error("❌ Erreur : 'esmel_modele.joblib' introuvable. Lancez 'esmel.py' d'abord.")
else:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Emplacement")
        lat = st.number_input("Latitude", value=35.6, help="Position Nord/Sud")
        lon = st.number_input("Longitude", value=-119.5, help="Position Est/Ouest")
        st.divider()
        st.subheader("👥 Quartier")
        rev = st.slider("Revenu moyen des habitants (10k$)", 0.5, 15.0, 3.8)
        pop = st.number_input("Population totale du quartier", value=1400, step=100)

    with col2:
        st.subheader("🏗️ La Maison")
        age = st.slider("Âge de la maison", 1, 52, 28)
        rms = st.slider("Nombre de pièces", 1, 15, 5)
        brs = st.slider("Nombre de chambres", 1, 10, 1)
        occ = st.slider("Capacité d'occupation", 1, 6, 3)

    
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
            background-color: white;
            color: black;
            text-align: center;
            padding: 10px;
            border-top: 1px solid 
        #e6e6e6;
        }
        </style>
        <div class="footer">
            <p>🚀 © 2025 - CV Pro par Kouton Vignon Esmel, M1 Data Science, UFRMI Université Félix Houphouët Boigny. Contact : esmelyann@gmail.com / +225 0505411990, avec ❤️ pour booster votre carrière</p>
        </div>
        """
        st.markdown(footer, unsafe_allow_html=True)


        
