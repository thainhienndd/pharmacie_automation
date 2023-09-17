import streamlit as st
import datetime
date_actuelle = datetime.datetime.now()


def compute_isaac_score(temperature, toux, adenopathie, amygale, age):
    isaac_score = 0
    if temperature:
        isaac_score += 1
    if toux:
        isaac_score += 1
    if adenopathie:
        isaac_score += 1
    if amygale:
        isaac_score += 1
    if age > 45:
        isaac_score -= 1
    return isaac_score


def realisabilite_trod(isaac_score, gorge):
    if gorge:
        if isaac_score >= 2:
            return True
    return False


def print_tracabilite_fiche_patient():
    st.divider()
    st.header('Information pour la fiche de traçabilité client')
    st.session_state['identification_structure'] = st.text_input('Identification de la structure', 'Pharmacie de Thai-Nhien et Jean')
    st.session_state['nom_pharmacien'] = st.selectbox('Nom du pharmacien', ('Thai-Nhien le meilleur', 'Jean caca'))
    st.session_state['nom_test'] = st.text_input('Nom du test disposant du marquage CE (et figurant sur la liste de l’ANSM)', 'Test X')
    st.session_state['num_lot'] = st.text_input('Numéro de lot du TROD angine', '123ABC')
    st.session_state['date_peremption'] = st.date_input('Date de péremption', datetime.date(2025, 1, 1))
    st.session_state['test_results'] = st.selectbox('Résultat du test', ('Positif', 'Négatif', 'Non concluant (y compris impossibilité de réaliser le test)'))

st.title('PoC improve pharmacie efficiency')
st.divider()

if 'preliminary_info_validated' not in st.session_state:
    st.session_state['preliminary_info_validated'] = False
if 'bouton_trod' not in st.session_state:
    st.session_state['bouton_trod'] = False

st.header('Information préliminaire')


st.session_state['name'] = st.text_input('Nom')
st.session_state['surname'] = st.text_input('Prénom')
st.session_state['brith_date'] = st.date_input('Date de naissance', datetime.date(2000, 1, 1))
st.session_state['is_ordonnance'] = st.selectbox("Présence d'une ordonnance", ('Oui', 'Non'))
st.session_state['age'] = date_actuelle.year - st.session_state['brith_date'].year - ((date_actuelle.month, date_actuelle.day) < (st.session_state['brith_date'].month, st.session_state['brith_date'].day))

if st.button('Valider les informations préliminaires') or st.session_state['preliminary_info_validated']:
    st.session_state['preliminary_info_validated'] = True
    if st.session_state['is_ordonnance'] == 'Non':
        st.divider()
        st.header('Vérification de la réalisabilité du test TROD')
        st.session_state['temperature'] = st.checkbox('La température du patient >38°')
        st.session_state['absence_de_toux'] = st.checkbox('Le patient a de la toux')
        st.session_state['adenopathie'] = st.checkbox('Le patient a une/des adénopathies cervicales douloureuses')
        st.session_state['amygale'] = st.checkbox('Le patient a une augmentation de volume ou un exsudat amygdalien')
        st.session_state['gorge'] = st.checkbox("Le patient a l'aspect de la gorge compatible avec une angine érythémateuse ou érythématopultacée")
        st.session_state['isaac_score'] = compute_isaac_score(st.session_state['temperature'], st.session_state['absence_de_toux'], st.session_state['adenopathie'], st.session_state['amygale'], st.session_state['age'])
        if st.button('Réalisabilité du test TROD') or st.session_state['bouton_trod']:
            st.session_state['bouton_trod'] = True
            st.text(f'Pour information le score Mac-Isaac est de {st.session_state["isaac_score"]}')
            st.session_state['realisabilite_trod'] = realisabilite_trod(st.session_state['isaac_score'], st.session_state['gorge'])
            if st.session_state['realisabilite_trod']:
                st.text('Test TROD réalisable !')
                print_tracabilite_fiche_patient()
            else:
                st.text('Test TROD non réalisable :(')
    elif st.session_state['is_ordonnance'] == 'Oui':
        print_tracabilite_fiche_patient()


