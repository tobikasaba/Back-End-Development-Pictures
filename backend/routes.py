from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    # Check if the data variable contains any pictures
    if data:
        # Return the data as JSON with a 200 OK status code
        return jsonify(data), 200
    # Return an error message with a 500 Internal Server Error status if no data exists
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture["id"] == id:
                return jsonify(picture), 200
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.get_json()
    if not new_pic or "id" not in new_pic:
        return {"message": "Invalid request: 'id' is required"}, 400

    for pic in data:
        if new_pic["id"] == pic["id"]:
            return {"Message": f"picture with id {new_pic['id']} already present"}, 302
    else:
        data.append(new_pic)
        return jsonify(new_pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_data=request.get_json()

    for pic in data:
        if pic["id"] == id:
            pic.update(new_data)
            return jsonify(pic), 200
    return {"message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"]==id:
            data.remove(pic)
            return {"message": "Picture deleted"}, 204
    return {"message": "Picture not found"}, 404

