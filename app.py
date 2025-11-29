import streamlit as st
import pandas as pd

# Načtení dat
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('data.csv')

df = st.session_state.df

# ------------------------- Úvodní stránka -------------------------

st.title("Dětská nadváha v mezinárodním kontextu")
st.subheader("Analýza dat z mezinárodní HBSC studie (2002–2018)")

st.markdown("""
### 📊 Zdroje dat  
HBSC (Health Behaviour in School-aged Children) je mezinárodní studie zkoumající zdraví, životní styl a psychickou pohodu žáků 5., 7. a 9. tříd.  
Analýza vychází z pěti vln: **2002, 2006, 2010, 2014 a 2018**, každá o ~250 000 pozorováních.
""")

# ------------------------- Rezervace místa pro obrázek -------------------------
# Sem v budoucnu vložíme obrázek, např.:
# st.image("assets/uvod.jpg", caption="Ilustrační obrázek", use_column_width=True)

# ------------------------- Cíl projektu -------------------------
st.markdown("""
### 🎯 Cíl projektu  
Cílem bylo určit hlavní faktory, které ovlivňují dětskou nadváhu. Zaměřily jsme se na otázky:
- Jakou roli hraje pohyb, strava a spánek?  
- Jsou sportující děti štíhlejší?  
- Jak velký vliv mají nezdravé potraviny?  
- Jak se liší riziko mezi pohlavími, věkem a státy?  
- Ovlivňuje nadváhu psychická pohoda?  
- Jak se nadváha mění v čase?
""")

# ------------------------- Hlavní zjištění -------------------------
st.markdown("""
### 🔍 Hlavní zjištění
- **20 % dětí má nadváhu** – každé páté dítě.  
- **Chlapci tvoří 2/3** dětí s nadváhou.  
- Nejohroženější věková skupina je **11 let**.  
- Nejrizikovější faktory jsou:  
    - častá konzumace sladkostí  
    - nedostatek pohybu  
    - žádná snídaně ve všední dny  
    - špatná ústní hygiena  
    - časté rvačky  
- **Dívky s nadváhou** častěji trpí psychickými a zdravotními problémy.  
- **Chlapci** jedí více sladkostí, pijí slazené nápoje a tráví více času u počítače.  
- **Mezinárodní rozdíly:**  
    - největší rozdíl mezi pohlavími: *Itálie*  
    - nejmenší: *Dánsko*  
    - nejvíce dětí s nadváhou: *Malta*, *Maďarsko*  
    - nejméně: *Dánsko*, *Nizozemsko*
""")

# ------------------------- Poděkování -------------------------
st.markdown("""
### 🙏 Poděkování  
.
""")
