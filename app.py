import sqlite3
import spatialite
import json


def get(longitude,
        latitude,
        voltage="'220 кВ', '6 кВ', '10 кВ', '20 кВ', '35 кВ'", 
        couht=15,
        distance=100):
    db = sqlite3.connect("db1.sqlite")
    db.enable_load_extension(True)
    db.load_extension('mod_spatialite')
    db.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    strsql = f"""
    select Distance(GeomFromText('POINT ({longitude} {latitude})', 4326),
                GEOMETRYPLACE, 1) AS DIST, TYPETM, NAMETM, KLASSVOLTAGE, PARTVL, NAMEVL, MANAGE,
                DIVISION,
                ID, astext(GEOMETRYPLACE) AS POINT from TECHPLACE where KLASSVOLTAGE IN({voltage})
                and PtDistWithin(GeomFromText('POINT ({longitude} {latitude})', 4326),
                GEOMETRYPLACE, {distance},1)
    """
    curr = db.cursor()
    curr.execute(strsql)
    data = curr.fetchall()
    db.close()
    return json.dumps(sorted([dict(el) for el in data], key=lambda x: x['DIST'])[:couht])