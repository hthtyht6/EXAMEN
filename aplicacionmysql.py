from crudmysql import MySQL
import json

variables = {}
variables["host"] = "localhost" # Servidor de la base de datos
variables["user"] = "root"
variables["pws"] = ""
variables["bd"] = "itj_estudiante"

def consulta(control):
    obj_mysql = MySQL(variables)
    sql_materias = f"SELECT estudiantes.nombre FROM estudiantes WHERE estudiantes.control='{control}';"
    sql_materias2 = f"SELECT kardex.materia, kardex.calificacion FROM kardex WHERE kardex.control='{control}';"
    obj_mysql.conectar_mysql()
    resp = obj_mysql.consulta_sql(sql_materias)
    resp2 = obj_mysql.consulta_sql(sql_materias2)
    obj_mysql.desconectar_mysql()

    lista = {}
    directorio = []
    lista["estudiante"]=resp[0][0]

    for mat in resp2:
        temporal={}
        temporal["materia"]=mat[0]
        temporal["calificacion"] = int(mat[1])
        directorio.append(temporal)
    lista["materias"] = directorio
    alumno = json.dumps(lista)
    return alumno

print(consulta("21420007")
