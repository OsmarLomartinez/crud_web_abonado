import pyodbc

# 🔗 Conexión
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=26.174.243.172;'
    'DATABASE=db_conexiondigital;'
    'UID=Osmar;'
    'PWD=osmar;'
)
cursor = conn.cursor()

# ✅ Mostrar filiales disponibles
def mostrar_filiales():
    print("\n🔸 Filiales disponibles:")
    cursor.execute("SELECT idFilial, NombreFilial FROM Filial")
    filiales = cursor.fetchall()
    for f in filiales:
        print(f"{f[0]}. {f[1]}")
    return [f[0] for f in filiales]  # retorna solo los IDs válidos

# ✅ Insertar abonado con selección de filial
def insertar_abonado():
    print("\n🔹 INSERTAR NUEVO ABONADO")
    paterno = input("Apellido paterno: ").upper()
    materno = input("Apellido materno: ").upper()
    pnombre = input("Primer nombre: ").capitalize()
    snombre = input("Segundo nombre: ").capitalize()
    numdoc = input("Número de documento: ")
    numcasa = input("Dirección (NumCasa): ")

    # Mostrar filiales y validar
    filiales_validas = mostrar_filiales()
    while True:
        try:
            id_filial = int(input("Seleccione ID de filial: "))
            if id_filial in filiales_validas:
                break
            else:
                print("❌ ID inválido. Intente nuevamente.")
        except ValueError:
            print("❌ Ingrese un número válido.")

    cursor.execute("""
        INSERT INTO Abonado (Paterno, Materno, PNombre, SNombre, NumDocIdentidad, NumCasa, idFilial)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (paterno, materno, pnombre, snombre, numdoc, numcasa, id_filial))
    conn.commit()
    print("✅ Abonado insertado correctamente.\n")

# ✅ Mostrar abonados
# ✅ Mostrar abonados (solo los 50 más recientes para optimizar rendimiento)
def mostrar_abonados():
    print("\n🔹 MOSTRANDO LOS 50 ABONADOS MÁS RECIENTES")
    cursor.execute("""
        SELECT TOP 50 A.IdAbonado, A.Paterno, A.Materno, A.PNombre, A.SNombre, 
                       A.NumDocIdentidad, A.NumCasa, F.DescripcionFilial
        FROM Abonado A
        INNER JOIN Filial F ON A.idFilial = F.idFilial
        ORDER BY A.IdAbonado DESC
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)



# ✅ Actualizar abonado
def actualizar_abonado():
    print("\n🔹 ACTUALIZAR ABONADO")
    id_abonado = input("ID del abonado a actualizar: ")
    nuevo_pnombre = input("Nuevo primer nombre: ").capitalize()
    nuevo_snombre = input("Nuevo segundo nombre: ").capitalize()
    nueva_direccion = input("Nueva dirección: ")

    cursor.execute("""
        UPDATE Abonado
        SET PNombre = ?, SNombre = ?, NumCasa = ?
        WHERE IdAbonado = ?
    """, (nuevo_pnombre, nuevo_snombre, nueva_direccion, id_abonado))
    conn.commit()
    print("✅ Abonado actualizado correctamente.\n")

# ✅ Eliminar abonado
def eliminar_abonado():
    print("\n🔹 ELIMINAR ABONADO")
    id_abonado = input("ID del abonado a eliminar: ")
    confirmar = input("¿Seguro que deseas eliminar este abonado? (s/n): ")
    if confirmar.lower() == 's':
        cursor.execute("DELETE FROM Abonado WHERE IdAbonado = ?", (id_abonado,))
        conn.commit()
        print("✅ Abonado eliminado correctamente.\n")
    else:
        print("❌ Operación cancelada.")

# ✅ Menú principal
def menu():
    while True:
        print("\n===== MENÚ CRUD ABONADO =====")
        print("1. Insertar abonado")
        print("2. Mostrar abonados")
        print("3. Actualizar abonado")
        print("4. Eliminar abonado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_abonado()
        elif opcion == "2":
            mostrar_abonados()
        elif opcion == "3":
            actualizar_abonado()
        elif opcion == "4":
            eliminar_abonado()
        elif opcion == "5":
            print("👋 Cerrando conexión y saliendo...")
            cursor.close()
            conn.close()
            break
        else:
            print("❌ Opción inválida.")

# 🔁 Ejecutar menú
menu()

