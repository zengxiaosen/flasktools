from flask import jsonify, request
from . import web



@web.route('/url')
def login():
    uid = request.args['uid']
    print(uid)
    return jsonify({'msg':'url'})
