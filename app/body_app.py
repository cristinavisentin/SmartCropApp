import streamlit as st

def cultivation_page():
    st.title("Cultivation page")


    st.header("Inserisci le informazioni sul tuo campo")
    field_size = st.number_input("Dimensione del campo (in ettari):", min_value=0.0, step=0.1)
    soil_type = st.selectbox("Tipo di terreno:", ["Sabbioso", "Argilloso", "Calcareo", "Torba", "Limoso"])
    ph_value = st.slider("pH del terreno:", 0.0, 14.0, 7.0)

    if st.button("Consiglia coltura"):
        if soil_type == "Argilloso" and 6.0 <= ph_value <= 7.5 and field_size > 1.0:
            recommendation = "Grano"
        elif soil_type == "Sabbioso" and ph_value > 7.5:
            recommendation = "Orzo"
        else:
            recommendation = "Mais"

        st.success(f"La pianta consigliata per il tuo campo è: **{recommendation}**")

    st.caption("Sviluppato per aiutare i contadini a migliorare la produttività!")