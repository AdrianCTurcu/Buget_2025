from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_buget, update_buget, add_achizitie, get_all_achizitii, get_achizitii_pe_luna  

app = Flask(__name__)
app.config['BUGET_LUNAR'] = 2000.0

@app.route('/')
def home():
    return render_template('index.html')


from database import get_achizitii_pe_luna

@app.route('/buget')
def buget():
    buget_lunar = get_buget()
    luna = request.args.get('luna')  # dacă nu e selectată, e None
     # 🔥 Dicționar pentru afișare frumoasă lună
    LUNI = {
        "01": "Ianuarie", "02": "Februarie", "03": "Martie",
        "04": "Aprilie", "05": "Mai", "06": "Iunie",
        "07": "Iulie", "08": "August", "09": "Septembrie",
        "10": "Octombrie", "11": "Noiembrie", "12": "Decembrie"
    }
    nume_luna = LUNI.get(luna) if luna else None
    if luna:
        rows = get_achizitii_pe_luna(luna)
    else:
        rows = get_all_achizitii(limit=5)  # fallback la ultimele 5

    produse = [
        {
            "id": row[0],
            "nume": row[1],
            "pret": row[2],
            "data": row[3]
        }
        for row in rows
    ]

    total = sum(p["pret"] for p in produse)
    disponibil = buget_lunar - total

    return render_template(
    'buget.html',
    buget=buget_lunar,
    produse=produse,
    total=total,
    disponibil=disponibil,
    luna_selectata=luna,
    nume_luna=nume_luna  # <-- Asta e vital
)


@app.route('/set-buget', methods=['POST'])
def set_buget():
    buget_nou = request.form.get('buget_nou')
    if buget_nou:
        update_buget(float(buget_nou))
    return redirect(url_for('buget'))

# adaugam datele in baza de date 
@app.route('/adauga', methods=['POST'])
def adauga():
    nume = request.form.get('nume_produs')
    pret = request.form.get('pret_produs')

    if nume and pret:
        try:
            pret = float(pret)
            add_achizitie(nume, pret)
        except ValueError:
            pass  # opțional: loghezi eroarea

    return redirect(url_for('buget'))

if __name__ == "__main__":
    init_db()
    print("✔️ Aplicatia este funcțională")
    print("✔️ Baza de date a fost creată.")
    app.run(debug=True, port=5000)
