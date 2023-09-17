import streamlit as st
import datetime

st.title('PoC improve pharmacie efficiency')
st.divider()

if 'preliminary_info_validated' not in st.session_state:
    st.session_state['preliminary_info_validated'] = False

st.header('Information préliminaire')


st.session_state['name'] = st.text_input('Nom')
st.session_state['surname'] = st.text_input('Prénom')
st.session_state['brith_date'] = st.date_input('Date de naissance', datetime.date(2000, 1, 1))
st.session_state['is_ordonnance'] = st.selectbox("Présence d'une ordonnance", ('Oui', 'Non'))

if st.button('Valider les informations préliminaires') or st.session_state['preliminary_info_validated']:
    st.session_state['preliminary_info_validated'] = True
    if st.session_state['is_ordonnance'] == 'Non':
        st.session_state['temperature'] = st.number_input('Température du patient', 38)
        st.session_state['absence_de_toux'] = st.checkbox('Le patient a de la toux')
        st.session_state['adenopathie'] = st.checkbox('Le patient a une/des adénopathies cervicales douloureuses')
        st.session_state['amygale'] = st.checkbox('Le patient a une augmentation de volume ou un exsudat amygdalien')

#st.selectbox('Nom du pharmacie', ('Thai-Nhien le meilleur', 'Jean caca'))