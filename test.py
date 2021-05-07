import flask
from app import get

blueprint = flask.Blueprint(
    'geo_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/geo/<float:longitude>/<float:latitude>')
def get_jobs(longitude, latitude):
    return get(longitude, latitude)


@blueprint.route("/api/geo/<float:longitude>/<float:latitude>/<voltage>/<int:couht>/<int:distance>")
def get_one_job(longitude, latitude, voltage, couht, distance):
    return get(longitude, latitude, voltage, couht, distance)