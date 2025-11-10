# 🧩 Analýza faktorů dětské nadváhy – Random Forest Model

Tento projekt se zabývá analýzou dat o životním stylu dětí a hledáním klíčových faktorů, které ovlivňují riziko nadváhy.  
Pomocí modelu **Random Forest** byla vytvořena predikce, která dokáže odhadnout pravděpodobnost nadváhy na základě vybraných proměnných.

---

## Výkon finálního modelu
- **Accuracy:** 0.615  
- **F1 score:** 0.371  
- **ROC AUC:** 0.652  
- **Recall (nadváha):** 0.60  

Model tedy úspěšně identifikuje přibližně 60 % případů dětské nadváhy.

---

##  Klíčové faktory (Top 10)
| Proměnná | Význam |
|-----------|---------|
| SEX | Pohlaví dítěte |
| SWEETS | Frekvence konzumace sladkostí |
| TOOTH_BRUSHING | Pravidelnost čištění zubů (indikátor návyků) |
| AGE | Věk dítěte |
| BREAKFAST_WEEKDAYS | Pravidelnost snídaní ve všední dny |
| FIGHT_YEAR | Četnost konfliktů / agrese |
| PHYS_ACT_60 | Fyzická aktivita (≥60 min denně) |
| BUL_BEEN | Zkušenost se šikanou |
| LIFESAT | Spokojenost se životem |
| TIME_EXE | Čas věnovaný cvičení |

---

##  Postup práce
1. Načtení a očištění dat (`data.csv`)  
   - odstraněny identifikátory (ID, COUNTRY, THINK_BODY, BMI, …)  
   - chybějící hodnoty doplněny (`fillna(-1)`)  
2. Definice cílové proměnné `OVERWEIGHT` (0 = ne, 1 = ano)  
3. Trénink modelu **RandomForestClassifier(class_weight="balanced")**  
4. Výběr **Top 20 proměnných** podle významnosti (bez proměnné `HEALTH`)  
5. Vyhodnocení výkonu modelu a uložení výsledků

---

## Soubory v projektu
| Soubor | Popis |
|--------|--------|
| `final_random_forest.ipynb` | Finální notebook s tréninkem modelu |
| `1_random_forest.ipynb` | Původní experimentální verze |
| `main.py` | Hlavní spouštěcí skript |
| `app.py` | Jednoduchá aplikace pro predikci |
| `requirements.txt` | Přehled knihoven |
| `.gitignore` | Ignorované soubory (např. data.csv) |

---

##  Možnosti rozšíření
- Doplnění vizualizací (SHAP hodnoty, barplot faktorů)
- Vytvoření webové aplikace pro predikci
- Obohacení o další modely (např. Logistic Regression, XGBoost)

---

**Autor:** [Lenka Leva, Aneta Kantorova](https://github.com/lenkaleva)  
**Projekt:** [Children_DA_Project](https://github.com/lenkaleva/Children_DA_Project)
