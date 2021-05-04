import sqlite3
import spatialite
conn = sqlite3.connect(":memory:")
conn.enable_load_extension(True)
with spatialite.connect('db1.sqlite') as db:
    print(db.execute('SELECT spatialite_version()').fetchone()[0])