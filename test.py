import flask
from app import get

blueprint = flask.Blueprint(
    'geo_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/geo/<float:longitude>/<float:latitude>')
def get_pillars_1(longitude, latitude):
    return get(longitude, latitude)


@blueprint.route("/api/geo/<float:longitude>/<float:latitude>/<voltage>/<int:couht>/<int:distance>")
def get_pillars_2(longitude, latitude, voltage, couht, distance):
    return get(longitude, latitude, voltage, couht, distance)


@blueprint.route('/api/geo/<int:longitude>/<int:latitude>')
def get_pillars_3(longitude, latitude):
    return get(longitude, latitude)


@blueprint.route("/api/geo/<int:longitude>/<int:latitude>/<voltage>/<int:couht>/<int:distance>")
def get_pillars_4(longitude, latitude, voltage, couht, distance):
    return get(longitude, latitude, voltage, couht, distance)


@blueprint.route("/api/geo/<float:longitude>/<float:latitude>/<voltage>/<int:couht>/<distance>")
def get_pillars_5(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad distance'})


@blueprint.route("/api/geo/<float:longitude>/<float:latitude>/<voltage>/<couht>/<int:distance>")
def get_pillars_6(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad count'})


@blueprint.route("/api/geo/<float:longitude>/<float:latitude>/<voltage>/<couht>/<distance>")
def get_pillars_7(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad count and distance'})


@blueprint.route("/api/geo/<float:longitude>/<latitude>/<voltage>/<int:couht>/<int:distance>")
def get_pillars_8(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad latitude'})


@blueprint.route("/api/geo/<float:longitude>/<latitude>/<voltage>/<int:couht>/<distance>")
def get_pillars_9(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad latitude and distance'})


@blueprint.route("/api/geo/<float:longitude>/<latitude>/<voltage>/<couht>/<int:distance>")
def get_pillars_10(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad latitude and count'})


@blueprint.route("/api/geo/<float:longitude>/<latitude>/<voltage>/<couht>/<distance>")
def get_pillars_11(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad latitude and count and distance'})


@blueprint.route("/api/geo/<longitude>/<float:latitude>/<voltage>/<int:couht>/<int:distance>")
def get_pillars_12(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude'})


@blueprint.route("/api/geo/<longitude>/<float:latitude>/<voltage>/<int:couht>/<distance>")
def get_pillars_13(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and distance'})


@blueprint.route("/api/geo/<longitude>/<float:latitude>/<voltage>/<couht>/<int:distance>")
def get_pillars_14(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and count'})


@blueprint.route("/api/geo/<longitude>/<float:latitude>/<voltage>/<couht>/<distance>")
def get_pillars_15(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and count and distance'})


@blueprint.route("/api/geo/<longitude>/<latitude>/<voltage>/<int:couht>/<int:distance>")
def get_pillars_16(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and latitude'})


@blueprint.route("/api/geo/<longitude>/<latitude>/<voltage>/<int:couht>/<distance>")
def get_pillars_17(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and latitude and distance'})


@blueprint.route("/api/geo/<longitude>/<latitude>/<voltage>/<couht>/<int:distance>")
def get_pillars_18(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and latitude and count'})


@blueprint.route("/api/geo/<longitude>/<latitude>/<voltage>/<couht>/<distance>")
def get_pillars_19(longitude, latitude, voltage, couht, distance):
    return flask.jsonify({'error': 'bad longitude and latitude and count and distance'})


