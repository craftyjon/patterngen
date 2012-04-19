# Creates presets.db for you
import sqlite3
import inspect
import os
import sys

if __name__=="__main__":
    print "OpenLights Database Bootstrapper"
    print "--------------------------------"

    if not os.path.exists('./presets/'):
        print "Error: I don't see a presets/ subdirectory here, are you running me from the right directory?"
        sys.exit(1)

    if os.path.exists('presets.db'):
        print "Warning: presets.db exists."
        ans = raw_input("Overwrite? [Y/n]")
        if str(ans).lower()=='n':
            print "Exiting..."
            sys.exit(0)
        try:
            os.remove('presets.db')
        except:
            print "Error removing old presets.db.  Make sure you have closed any tools that are accessing it!"
            sys.exit(1)

    print "Creating new presets.db in %s" % os.getcwd()
    try:
        con = sqlite3.connect('presets.db')
        cur = con.cursor()
        con.row_factory = sqlite3.Row
    except sqlite3.Error, e:
        log.error("Sqlite Error: %s" % e.args[0])
        if con:
            con.close()

    cur.execute("CREATE TABLE presets (id integer primary key autoincrement, classname text, active integer)")
    con.commit()

    print "Loading presets..."
    try:
        import presets
    except ImportError:
        print "Could not import presets.  Is your presets/ directory a real package?"
        sys.exit(1)

    for name,obj in inspect.getmembers(presets, inspect.isclass):
        print "Adding %s" % name
        cur.execute("INSERT INTO presets (classname, active) VALUES (?, 1)", [name])

    con.commit()
    con.close()