import os
import json
import ndfMaker as NDFMaker
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import pymongo as pymongo
# change this to your locations
sourceMod = "C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\OG"
desctinationMod = "C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\Seans Army Mod"

ndfMaker = None
status = "not loaded"
app = Flask(
    __name__,
    static_url_path="",
    static_folder="web/sean-modder/build",
    template_folder="web/templates",
)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sean-modder"]
collecitonMod = db["mods"]
mods = list(collecitonMod.find({}))
for mod in mods:
    print(mod)

if len(list(mods)) == 0:
    status = "No Mods"
    collecitonMod.insert_one(
        {
            "name": "OG",
            "source": sourceMod,
            "path": desctinationMod,
        }
    )

ndfMaker = NDFMaker.NDFMaker(
    sourceMod,
    desctinationMod,
)


@app.route("/api/delete-mod-decks", methods=["POST"])
def updateModdedDeckDelete():
    data = request.get_json()
    ndfMaker.deleteModdedDeck(data['namespace'])
    return jsonify(message="okay")

@app.route("/api/mod-decks", methods=["POST"])
def updateModdedDeck():
    #
    data = request.get_json()
    data.pop("_id", None)
    ndfMaker.saveModdedDeck(data)
    return jsonify(message="okay")
@app.route("/api/make-ndf", methods=["POST"])
def makeNDFFiles():
    #
    ndfMaker.makeNDF()
    return jsonify(message="okay")


@app.route("/api/mods", methods=["GET"])
def modsFilter():
    mods = ndfMaker.getMods()
    return mods

@app.route("/api/modded-decks", methods=["GET"])
def decksFilter():
    filter = json.loads(request.args.get("filter") or "{}")
    limit = int(request.args.get("limit") or "10")
    skip = int(request.args.get("skip") or "0")
    decks = ndfMaker.getModdedDecks(filter, limit, skip)
    return decks


@app.route("/api/decks", methods=["GET"])
def moddedDecksFilter():
    filter = json.loads(request.args.get("filter") or "{}")
    limit = int(request.args.get("limit") or "10")
    skip = int(request.args.get("skip") or "0")
    decks = ndfMaker.getDecks(filter, limit, skip)
    return decks


@app.route("/api/load", methods=["GET"])
def loadData():
    if ndfMaker is not None:
        ndfMaker.load()
    return jsonify(message="okay")


# Define your API endpoints
@app.route("/api/status", methods=["GET"])
def status():
    if ndfMaker is not None:
        status = ndfMaker.status
    # ndf parse load the data as cards

    return jsonify(message=status)


# Define your API endpoints


# export default paths
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run()
