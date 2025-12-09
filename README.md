

---

# **UTM StudySchedule Bot**

### *Telegram bot pentru monitorizarea și notificarea în timp real a orarului studenților UTM – FCIM*

---

## **📌 Descriere generală**

**UTM StudySchedule Bot** este o aplicație complexă ce automatizează procesul de preluare, analiză și distribuire a informațiilor privind orarul studenților masteranzi de la **Universitatea Tehnică a Moldovei, Facultatea Calculatoare, Informatică și Microelectronică (FCIM)**.

Botul monitorizează site-ul oficial al facultății, descarcă orarul publicat în format PDF, îl procesează prin scraping și îl transformă într-un format accesibil utilizatorului. În plus, oferă funcționalități de notificare automată despre modificările din orar și despre lecțiile sau examenele ce urmează să înceapă.

Acesta reprezintă o soluție eficientă pentru provocarea reală a studenților: orarul este publicat într-un singur PDF pentru toate grupele, ceea ce face dificilă navigarea, filtrarea și organizarea informațiilor. Botul rezolvă această problemă prin personalizarea completă a experienței utilizatorului.

---

## **🎯 Funcționalități principale**

### **🔄 Monitorizare automată a orarului (Background Service)**

* Verifică periodic pagina oficială a FCIM.
* Detectează schimbările în linkurile către orarul lecțiilor și examenelor.
* Actualizează baza locală și anunță utilizatorii abonați.

### **📥 Descărcarea și prelucrarea PDF-urilor**

* Descarcă automat fișierele PDF ale orarului.
* Parsează tabelele PDF folosind Camelot.
* Normalizează structura tabelară și generează fișiere JSON.

### **🔄 Transformarea datelor pentru utilizatori**

* Filtrare inteligentă a orarului pentru:

  * o anumită **grupă**,
  * un anumit **profesor**,
  * o anumită **zi** sau **săptămână**.
* Structurare pentru lecții și examene.

### **🤖 Interfață Telegram intuitivă**

Botul pune la dispoziție un meniu complet:

```
📋 Meniu Principal  
🔔 /subscribe – Activează notificările  
🔕 /unsubscribe – Dezactivează notificările  
📅 /azi — Orarul pentru astăzi  
📅 /maine — Orarul pentru mâine  
📆 /saptamana_curenta — Orarul săptămânii curente  
📆 /saptamana_viitoare — Orarul săptămânii viitoare  
📚 /orar_lectii — Orarul complet al lecțiilor  
📝 /orar_examene — Calendarul examenelor  
🏠 /menu — Revino la meniul principal  
```

### **🔔 Notificări inteligente**

* Notificări instant la modificarea PDF-ului oficial.
* Notificări cu 15 minute înainte de începerea unei lecții sau a unui examen.
* Notificări personalizate în funcție de grupa/studentul sau profesorul abonat.

---

## **🏛️ Arhitectura și integrarea Design Patterns**

Proiectul folosește **9 design pattern-uri** pentru a crea o arhitectură scalabilă, modulară și ușor de extins.

### **1. Adapter**

Transformă structura JSON brută într-un format intern unificat utilizat de restul aplicației.

### **2. Builder**

Generează notificări personalizate pentru studenți și profesori într-un format coerent.

### **3. Command**

Gestionarea comenzilor Telegram prin obiecte dedicate (`/start`, `/menu`, `/azi`, etc.).

### **4. Composite**

Construiește structuri ierarhice pentru zile, semestre, lecții, examene.

### **5. Facade**

`ScheduleFacade` coordonează subsistemele:

* Descărcare,
* Parsare,
* Monitorizare,
* Telegram Botul,
* Notificări.

### **6. Factory Method**

Creează parser-ele PDF → DataFrame pentru lecții și examene.

### **7. Observer**

Gestionează abonații și trimite notificări automate la schimbări de orar.

### **8. Strategy**

Transformă orarul în funcție de tipul utilizatorului (student/profesor).

### **9. Template Method**

Definește algoritmul standard de descărcare PDF, cu pași extensibili în subclase.

---

## **📊 Fluxul aplicației**

1. Se monitorizează pagina FCIM.
2. Dacă linkurile către PDF-uri s-au schimbat → se descarcă noile fișiere.
3. Fișierele PDF sunt parcurse și convertite în JSON.
4. JSON-ul este adaptat într-o structură internă.
5. Botul răspunde la comenzi și furnizează orarul filtrat.
6. Serviciul de fundal trimite notificări automate.

---


## **📌 Concluzie**

**UTM StudySchedule Bot** oferă automatizarea întregului proces de preluare și distribuire a orarului și prin integrarea unui set de pattern-uri de proiectare, proiectul demonstrează bune practici de arhitectură software, furnizând o aplicație stabilă, extensibilă și ușor de întreținut.

---

