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
    if  st.session_state['gorge'] == 'Oui':
        if isaac_score > 1:
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

st.header('Identification du patient')

st.session_state['name'] = st.text_input('Nom')
st.session_state['surname'] = st.text_input('Prénom')
st.session_state['brith_date'] = st.date_input('Date de naissance', date.today() ,format="DD/MM/YYYY")
st.session_state['is_ordonnance'] = st.selectbox("Présentation d'une ordonnance de dispensation conditionnelle (si TROD+) datant au plus de 7 jours", ('Oui', 'Non'))
st.session_state['age'] = date_actuelle.year - st.session_state['brith_date'].year - ((date_actuelle.month, date_actuelle.day) < (st.session_state['brith_date'].month, st.session_state['brith_date'].day))

if st.button('Valider') or st.session_state['preliminary_info_validated']:
    st.session_state['preliminary_info_validated'] = True
    if st.session_state['is_ordonnance'] == 'Non':
        st.divider()
        st.header("Critères d'éligibilités du patient")
        st.subheader("Calcul du score de Mac Isaac")
        st.caption("Le patient présente les éléments cliniques suivants :")
        st.session_state['temperature'] = st.checkbox("Température > 38°C")
        st.session_state['absence_de_toux'] = st.checkbox("Absence de toux")
        st.session_state['adenopathie'] = st.checkbox("Adénopathie(s) cervicale(s) antérieure(s) douloureuse(s)")
        st.session_state['amygale'] = st.checkbox("Augmentation de volume ou exsudat amygdalien")
        st.subheader("Aspect de la gorge")
        st.session_state['gorge'] = st.selectbox("Le patient a l'aspect de la gorge compatible avec une angine érythémateuse ou érythématopultacée", ('Oui', 'Non'))
        st.session_state['isaac_score'] = compute_isaac_score(st.session_state['temperature'], st.session_state['absence_de_toux'], st.session_state['adenopathie'], st.session_state['amygale'], st.session_state['age'])
        if st.button('Réalisabilité du test TROD') or st.session_state['bouton_trod']:
            st.session_state['bouton_trod'] = True
            st.text(f'Le score Mac-Isaac est de {st.session_state["isaac_score"]}')
            st.session_state['realisabilite_trod'] = realisabilite_trod(st.session_state['isaac_score'], st.session_state['gorge'])
            if st.session_state['realisabilite_trod']:
                st.text("Le TROD angine est réalisable à l'officine")
                print_tracabilite_fiche_patient()
            else:
                st.text("Le TROD angine n'est pas réalisable à l'officine car le score de Mac Isaac est inférieur à 2 et/ou l'aspect de la gorge du patient n'est pas compatible.")
    elif st.session_state['is_ordonnance'] == 'Oui':
        print_tracabilite_fiche_patient()

