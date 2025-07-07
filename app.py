from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# 🔗 Conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=26.174.243.172;'
    'DATABASE=db_conexiondigital;'
    'UID=Osmar;'
    'PWD=osmar;'
)
cursor = conn.cursor()

@app.route('/')
def index():
    cursor.execute("""
        SELECT TOP 50 A.IdAbonado, A.Paterno, A.Materno, A.PNombre, A.SNombre, 
                       A.NumDocIdentidad, A.NumCasa, F.DescripcionFilial
        FROM Abonado A
        INNER JOIN Filial F ON A.idFilial = F.idFilial
        ORDER BY A.IdAbonado DESC
    """)
    abonados = cursor.fetchall()
    return render_template("index.html", abonados=abonados)

@app.route('/insertar', methods=['POST'])
def insertar():
    paterno = request.form['paterno'].upper()
    materno = request.form['materno'].upper()
    pnombre = request.form['pnombre'].capitalize()
    snombre = request.form['snombre'].capitalize()
    numdoc = request.form['numdoc']
    numcasa = request.form['numcasa']
    id_filial = int(request.form['idfilial'])

    cursor.execute("""
        INSERT INTO Abonado (Paterno, Materno, PNombre, SNombre, NumDocIdentidad, NumCasa, idFilial)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (paterno, materno, pnombre, snombre, numdoc, numcasa, id_filial))
    conn.commit()
    return redirect('/')

# Puedes agregar rutas para actualizar y eliminar

if __name__ == '__main__':
    app.run(debug=True)
