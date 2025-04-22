'''
    Note: docvs uses 3 seperate databases: docvs.db, wiki.db and log.db
    Reason for splitting is backup and multiprocess managment, also wiki.db can easily be shared, or backed up 

    docvs.db: Contains all the files and resources
        Deleting this file will result in full reindexing of all files and resources
        Note: this will remove all changes made to resources and remove all manual entries
    log.db: Contains all the log entries
        Deleting this file will result in loss of all log entries
        In an multi process environment, this file will be locked by the process that is writing to it
        Further logfiles will be written to a new file named log_x.db

'''

import aiosqlite
import os
async def connect_db(main):
    db = await aiosqlite.connect(os.path.join(main.path,"studlis.db"))
    await db.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            pw TEXT NOT NULL,
            permission INTEGER NOT NULL,
            last_login INTEGER,
            last_login_host TEXT
        )
    ''')
    await db.commit()
    return db