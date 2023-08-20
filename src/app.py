"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200 if members else 400

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is not None:
        
        return jsonify(member), 200
    else:
        return jsonify({"message":"not found"})

@app.route('/member/', methods =['POST'])
def add_member():
    try:
        data=request.get_json()
        jackson_family.add_member(data)
        return jsonify({"message":"member added"}),200
    except:
        return jsonify({"message":"member not added"}), 400

@app.route('/member/<int:id>' , methods=['DELETE'])
def delete_member(id):
    member_delete = jackson_family.delete_member(id)
    if member_delete is True:
        return jsonify({"done":member_delete}) , 200
    return jsonify("user not found")  ,201  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)