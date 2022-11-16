'''
Utilizando la clase MySQL, cargue los datos a la Base de datos de:
    Estudiantes.txt
    Kardex.txt

Genere las constraseñas a los estudiantes en una tabla llamada Usuarios, utilice la clase Password.

Para ello, cree la Base de Datos y las tablas: Estudiantes, Usuarios y Kardex con los campos que tienen
los archivos mencionados, considere integridad referencial.
Realice el CRUD a la tabla Kardex

Realice algo SIMILAR para MongoDB, considere solo consultas de una tabla.

para instalar mysql: pip install mysql-conector-python
para instalar pymongo: pip install pymongo

'''
from crudmysql import MySQL
from env import variables
from caja import Password
from decimal import Decimal

RUTA = "C:/Users/juanj/PycharmProjects/Unidad3_2 (2)/Unidad3_2/"

def regresa_conjunto_estudiantes():
    estudiantes = set()
    with open(RUTA + "Estudiantes.prn") as arch_estudiantes:
        for linea in arch_estudiantes:
            control = linea[0:8]
            nombre = linea[8:-1]
            estudiantes.add((control,nombre))
    # Cerrar el archivo
    arch_estudiantes.close()
    return estudiantes

def regresa_conjunto_promedios():
    promedios_materias = set()
    with open(RUTA + "kardex.txt") as kardex:
        for linea in kardex:
            control = linea.split("|")[0]
            materia = linea.split("|")[1]
            promedio = linea.split("|")[2][:-1]  # el -1 para no incluir el último caracter
            promedios_materias.add((control,materia,promedio))
    # Cerrar el archivo
    kardex.close()
    return promedios_materias

def cargar_datos():# host="localhost", user="root", pws="", bd="opensource"
    obj_estudiante = MySQL(variables)
    obj_estudiante.conectar_mysql()
    print("Cargando datos . . . ")
    lista_estudiantes = regresa_conjunto_estudiantes()
    lista_materias = regresa_conjunto_promedios()
    for ctrl,nom in lista_estudiantes:
        sql =f"INSERT INTO estudiantes values('{ctrl}','{nom}');"
        obj_estudiante.consulta_sql(sql)
        usr = Password(longitud=10,contrasena='1234567890')
        usr.generar_password()
        sql_usr = f'INSERT INTO usuarios(control,clave,clave_cifrada) VALUES("{ctrl}","{usr.contrasena}","{usr.contrasena_cifrada}");'
        obj_estudiante.consulta_sql(sql_usr)
    for ctrl, mat, prom in lista_materias:
        sql = f"INSERT INTO kardex(control, materia, calificacion) values('{ctrl}','{mat}',{prom});"
        print(sql)
        obj_estudiante.consulta_sql(sql)
    obj_estudiante.desconectar_mysql()
    print("Datos cargados correctamente")

def insertar_estudiante():
    obj_MySQL = MySQL(variables)
    print(" == INSERTAR ESTUDIANTES ==")
    ctrl = input("Dame el numero de control: ")
    nombre = input("Dame el nombre del estudiante: ")
    clave = input("Dame la clave de acceso: ")
    obj_usuario = Password(longitud=len(clave), contrasena=clave)
    sql_estudiante = f"INSERT INTO estudiantes values('{ctrl}','{nombre}');"
    sql_usuario = f'INSERT INTO usuarios(control,clave,clave_cifrada) values("{ctrl}","{clave}","{obj_usuario.contrasena_cifrada.decode()}");'
    # print(sql_usuario)
    obj_MySQL.conectar_mysql()
    obj_MySQL.consulta_sql(sql_estudiante)
    obj_MySQL.consulta_sql(sql_usuario)
    obj_MySQL.desconectar_mysql()
    print("Datos insertados correctamente")

def actualizar_calificacion():
    obj_MySQL = MySQL(variables)
    print(" == ACTUALIZAR PROMEDIO ==")
    ctrl = input("Dame el numero de control: ")
    materia = input("Dame la materia a actualizar: ")
    sql_buscar_materia = f"SELECT 1 FROM kardex" \
                         f" WHERE control='{ctrl}' AND materia='{materia.strip()}';"
    print(sql_buscar_materia)
    obj_MySQL.conectar_mysql()
    respuesta = obj_MySQL.consulta_sql(sql_buscar_materia)
    obj_MySQL.desconectar_mysql()
    if respuesta:
        promedio = float(input("Dame el nuevo promedio: "))
        sql_actualiza_prom = f"UPDATE kardex set calificacion={promedio} " \
                             f"WHERE control='{ctrl}' and materia='{materia.strip()}';"
        obj_MySQL.conectar_mysql()
        obj_MySQL.consulta_sql(sql_actualiza_prom)
        obj_MySQL.desconectar_mysql()
        print("Promedia ha sido actualizado")
    else:
        print(f"El estudiante con numero de control {ctrl} o la materia: {materia} NO EXISTE")


def consultar_materias():
    obj_MySQL = MySQL(variables) # *********************************
    obj_MySQL.conectar_mysql()
    print(" == CONSULTAR MATERIAS POR ESTUDIANTE ==")
    ctrl = input("Dame el numero de control: ")
    sql_materias =f"SELECT estudiantes.nombre, kardex.materia, kardex.calificacion FROM estudiantes, kardex WHERE estudiantes.control = kardex.control and estudiantes.control='{ctrl}';"
    print(sql_materias)
    resp = obj_MySQL.consulta_sql(sql_materias)
    obj_MySQL.desconectar_mysql()
    if resp:
        print("Estudiante: ", resp[0][0])
        for mat in resp:
            print("Materias",
                                  [
                                    {
                                        "promedio": {format(mat[2])},
                                        "materias": {mat[1]}

                                    }


            ],)
    else:
        print (f"El estudiante con Número de control: {ctrl} NO existe")

def consulta_general():
    obj_MySQL = MySQL(variables)
    obj_MySQL.conectar_mysql()
    sql_general = "SELECT E.control, E.nombre, format(avg(K.calificacion),1) as promedio " \
                  "FROM estudiantes E, kardex K " \
                  "WHERE E.control = K.control " \
                  "GROUP BY K.control;"
    estudiantes = obj_MySQL.consulta_sql(sql_general)
    obj_MySQL.desconectar_mysql()
    print("CONTROL        NOMBRE              PROMEDIO")
    for est in estudiantes:
        print(est[0], est[1], est[2])

def eliminar_estudiante():
    obj_MySQL = MySQL(variables)
    obj_MySQL.conectar_mysql()
    print(" == ELIMINAR ESTUDIANTE ==")
    ctrl = input("Dame el numero de control: ")
    sql_eliminar1 = f"delete from kardex where control='{ctrl}';"
    sql_eliminar2 = f"delete from usuarios where control='{ctrl}';"
    sql_eliminar3 = f"delete from estudiantes where control='{ctrl}';"
    obj_MySQL.consulta_sql(sql_eliminar1)
    obj_MySQL.consulta_sql(sql_eliminar2)
    obj_MySQL.consulta_sql(sql_eliminar3)
    obj_MySQL.desconectar_mysql()
    print(f"El estudiante con numero de control {ctrl} ha sidp eliminado")


def menu():
    while True:
        print(" ===============  Menú Principal  ===================")
        print("1. Insertar estudiante ")
        print("2. Actualizar calificación ")
        print("3. Consultar materias por estudiante")
        print("4. Consulta general de estudiantes")
        print("5. Eliminar a un estudiante ")
        print("6. Salir ")
        print("Dame la opcion que deseas? ")
        try:
            opcion = int(input(""))
        except Exception as error:
            print("ERROR: ", error)
            break
        else:
            if opcion == 1:
                insertar_estudiante()
            elif opcion == 2:
                actualizar_calificacion()
            elif opcion == 3:
                consultar_materias()
            elif opcion == 4:
                consulta_general()
            elif opcion == 5:
                eliminar_estudiante()
            elif opcion == 6:
                break
            else:
                print("Opcion incorrecta ")


#cargar_datos()
menu()
