import aiosqlite
import asyncio
import time
from enum import Enum

class LogType(Enum):

    # System Messages
    VERBOSE           =  0
    INFO              =  1  # Minor events, to be deleted after 6h, i.e. index update
    EVENT             =  2  # Major events, to be deleted after 30d
    NOTIFICATION      =  3  # Major notification, persistent    
    WARNING           =  6
    ERROR             =  7
    CRITICAL          =  8

    # User Actions
    RESOURCE_ACCESSED     = 10
    USER_ELEVATED_LOGIN   = 11 # User logged in with elevated permissions (= edit mode)
    RESOURCE_EDIT         = 20 
    USER_EDIT             = 21




class AsyncDBLogger:
    def __init__(self, db_path='logs.db'):
        self.db_path = db_path
        self.connection = None

    async def initialize(self):
        """Initialize the database connection and create the logs table."""
        self.connection = await aiosqlite.connect(self.db_path)
        await self._create_table()

    async def _create_table(self):
        """Create the logs table if it does not exist.
        
        The created_at and expiry fields are stored as UNIX timestamps (REAL).
        """
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type VARCHAR(16),
                severity INTEGER,
                expiry INTEGER,
                message TEXT,
                data TEXT,
                created_at INTEGER,
                user INTEGER,
                object_id INTEGER                            
                
            )
        ''')
        await self.connection.execute('''
            CREATE INDEX IF NOT EXISTS idx_type ON logs (type);
            CREATE INDEX IF NOT EXISTS idx_severity ON logs (severity);
            CREATE INDEX IF NOT EXISTS idx_expiry ON logs (expiry);
            CREATE INDEX IF NOT EXISTS idx_user ON logs (user);
            CREATE INDEX IF NOT EXISTS idx_object_id ON logs (object_id);
        ''')
        await self.connection.commit()

    async def log(self, log_type, severity, message, data=None, expiry=None, user=None, object_id=None):
        """Log a message to the database."""
        asyncio.create_task(self._log(log_type, severity, message, data, expiry, user, object_id))
    async def _log(self, log_type, severity, message, data=None, expiry=None, user=None, object_id=None):
        """Log a message to the database."""    
        await self.connection.execute('''
            INSERT INTO logs (type, severity, expiry, message, data, created_at, user, object_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (log_type.name, severity, expiry, message, data, time.time(), user, object_id))
        await self.connection.commit()

    async def info(self,  message, data=None, expiry=None, user=None, object_id=None):
        """Log an INFO message."""
        await self.log(LogType.INFO,message, data, expiry, user, object_id)
        print("INFO: "+message)
    

    async def delete_expired_logs(self):
        """Delete all log entries with an expiry time that has passed."""
        now = time.time()
        await self.connection.execute('''
            DELETE FROM logs 
            WHERE expiry < ? AND expiry NOT NULL
        ''', (now,))
        await self.connection.commit()


    async def close(self):
        """Close the database connection."""
        await self.connection.close()