import sqlite3
import spatialite
#conn = sqlite3.connect(":memory:")
#conn.enable_load_extension(True)
db = sqlite3.connect("db1.sqlite")
db.enable_load_extension(True)
db.load_extension('mod_spatialite')
print(db.execute('SELECT spatialite_version()').fetchone()[0])
strsql = """
select Distance(GeomFromText('POINT (50.97598 60.43534)', 4326),
            GEOMETRYPLACE, 1) AS DIST, TYPETM, NAMETM, KLASSVOLTAGE, PARTVL, NAMEVL, MANAGE,
            DIVISION,
            ID, astext(GEOMETRYPLACE) AS POINT from TECHPLACE where KLASSVOLTAGE IN('220 кВ'
            , '6 кВ', '10 кВ', '20 кВ', '35 кВ')
            and PtDistWithin(GeomFromText('POINT (50.97598 60.43534)', 4326),
            GEOMETRYPLACE, 100,1)
"""
curr = db.cursor()
for row in curr.execute(strsql):
    print(row)
