from flask import Blueprint, request, session, current_app, jsonify
from flasgger import swag_from

catalogo_bp = Blueprint('catalogo_bp', __name__)

@catalogo_bp.route('/api/catalogo', methods=['GET'])
@swag_from('../../Doc/Catalogo/catalogo.yml')
def api_catalogo():
    connection = current_app.config['MYSQL_CONNECTION']
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM categorias AS cat 
                JOIN subcategoria AS sub ON sub.categoria = cat.id_categoria;""")
            catalogo = cursor.fetchall()
            return jsonify(catalogo)
    except Exception as e:
        return str(e)