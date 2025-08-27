import os, json
from flask_bcrypt import Bcrypt
from flask import Blueprint, request, jsonify, send_from_directory, Response, current_app
from flask_cors import cross_origin
from sqlalchemy import inspect
from sqlalchemy.ext.automap import automap_base
from app import db
from werkzeug.utils import secure_filename
from flasgger import swag_from

tablas = automap_base()
bcrypt = Bcrypt()
print(tablas.classes.keys())

def get_fk_display(obj):
    cols = [c.name for c in obj.__table__.columns if 'name' in c.name.lower() or 'nombre' in c.name.lower()]
    if cols:
        return getattr(obj, cols[0])
    pks = [c.name for c in obj.__table__.primary_key]
    return getattr(obj, pks[0])

def serializar_con_fk_lookup(objetos):
    fk_tablas = {
        'categoria':    'categorias',
        'subcategoria': 'subcategoria',
        'membresia':    'membresias',
        'medio_pago':   'medios_pago',
        'rol':          'roles'
    }
    lista = []
    for o in objetos:
        data = {}
        for col in o.__table__.columns:
            valor = getattr(o, col.name)
            
            if col.name in fk_tablas and valor is not None:
                try:
                    clase_fk = getattr(tablas.classes, fk_tablas[col.name])
                    obj_fk = db.session.get(clase_fk, valor)
                    if obj_fk:
                        data[col.name] = {
                            'id': valor,
                            'value': get_fk_display(obj_fk)
                        }
                        continue
                except Exception:
                    pass
            
            data[col.name] = valor
        lista.append(data)
    return lista

bp_tablas = Blueprint("tablas", __name__)
UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp_tablas.route("/images/<path:filename>", methods=["GET", "OPTIONS"])
@swag_from('../controllers/Doc/Tablas/images.yml')
def images(filename):
    if request.method == "OPTIONS":
        return Response(status=200)
    ruta = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(ruta):
        return jsonify({"error": "Imagen no encontrada", "filename": filename}), 404
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp_tablas.route("/registro", methods=["POST","OPTIONS"])
@swag_from('../controllers/Doc/Tablas/registros.yml')
def registros():
    if request.method == "OPTIONS":
        return Response(status=200)
    tablaActual = tablas.classes[request.form["table"]]
    registro = tablaActual()
    print(request.form)
    for clave, valor in request.form.items():
        try: 
            lista = json.loads(valor)
            if "password" in lista:
                valor = bcrypt.generate_password_hash(lista.get("text")).decode('utf-8')
            elif "text" in lista:
                valor = lista.get("text")
            setattr(registro, clave, valor)
        except(json.JSONDecodeError, TypeError):
            if clave not in ("table", "req"):
                setattr(registro, clave, valor)
    for clave, archivo in request.files.items():
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(UPLOAD_FOLDER, filename))
        setattr(registro, clave, filename)
    db.session.add(registro)
    db.session.commit()
    return jsonify({"respuesta": "Se registro correctamente"})

@bp_tablas.route("/consultas", methods=["POST","OPTIONS"])
@swag_from('../controllers/Doc/Tablas/consultas.yml')
def consultas():
    if request.method == "OPTIONS":
        return Response(status=200)
    objeto = request.get_json()
    respuestas = {}
    if "foreign" in objeto:
        tablaActual = tablas.classes[objeto["table"]]
        get = serializar_con_fk_lookup(
            db.session.query(tablaActual)
                      .filter(getattr(tablaActual, objeto["columnDependency"]) == objeto["foreign"])
                      .all()
        )
        respuestas[objeto["table"]] = get
    else:
        for tabla in objeto:
            tablaActual = tablas.classes[tabla["table"]]
            respuestas[tabla["table"]] = serializar_con_fk_lookup(
                db.session.query(tablaActual).all()
            )
    return jsonify(respuestas)

@bp_tablas.route("/consultaTabla", methods=["POST","OPTIONS"])
@swag_from('../controllers/Doc/Tablas/consultaTabla.yml')
def consultaTabla():
    if request.method == "OPTIONS":
        return Response(status=200)
    req = request.get_json()
    tabla = tablas.classes[req["table"].lower()]
    objetos = db.session.query(tabla).all()
    filas = serializar_con_fk_lookup(objetos)
    columnas = [{
        "name": col.name.replace("_", " ").title(),
        "field": col.name
    } for col in tabla.__table__.columns]
    return jsonify({"filas": filas, "columnas": columnas})

@bp_tablas.route("/eliminar", methods=["POST","OPTIONS"])
@swag_from('../controllers/Doc/Tablas/eliminar.yml')
def eliminar():
    if request.method == "OPTIONS":
        return Response(status=200)
    datos = request.get_json()
    table = tablas.classes[datos["table"]]
    elemento = db.session.get(table, datos["id"])
    db.session.delete(elemento)
    db.session.commit()
    return jsonify({"respuesta": "se ha eliminado el registro"})

@bp_tablas.route("/consultaFilas", methods=["POST","OPTIONS"])
@swag_from('../controllers/Doc/Tablas/consultaFilas.yml')
def consultaFilas():
    if request.method == "OPTIONS":
        return Response(status=200)
    datos = request.get_json()
    tabla = tablas.classes[datos["table"]]
    elemento = db.session.get(tabla, datos["id"])
    if not elemento:
        return jsonify({}), 404
    fila = serializar_con_fk_lookup([elemento])[0]
    return jsonify(fila)

@bp_tablas.route("/editar", methods=["POST","OPTIONS"])
@swag_from('../controllers/Doc/Tablas/editar.yml')
def editar():
    if request.method == "OPTIONS":
        return Response(status=200)
    tablaActual = tablas.classes[request.form["table"]]
    elementoG = db.session.get(tablaActual, request.form["id"])
    for clave, valor in request.form.items():
        try:
            lista = json.loads(valor)
            if "password" in lista:
                valor = bcrypt.generate_password_hash(lista.get("text")).decode('utf-8')
            elif "text" in lista:
                valor = lista.get("text")
            setattr(elementoG, clave, valor)
        except (json.JSONDecodeError, TypeError):
            if clave not in ("table", "id", "req"):
                setattr(elementoG, clave, valor)
    for clave, archivo in request.files.items():
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(UPLOAD_FOLDER, filename))
        setattr(elementoG, clave, filename)
    db.session.commit()
    return jsonify({"respuesta": "Se actualizo el registro"})