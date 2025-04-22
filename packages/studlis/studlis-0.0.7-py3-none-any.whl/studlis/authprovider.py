import abc
from enum import Enum
import aiosqlite
import hashlib
class AuthPermission(Enum):
    USER = 0        
    MODERATOR = 5       # basic edit permission (category permission needed)
    MODERATOR_USER = 6  # basic edit permission and can grant others permissions (category permission needed)
    EDITOR = 8          # can edit everything and can grant others permissions  (category permission not needed)
    ADMIN = 10          # can do everything

class AuthProvider():
  
    @abc.abstractmethod
    async def authenticate(self,app,*args,**kwargs):
        pass
    @abc.abstractmethod
    async def authorize(self, username: str, permission: AuthPermission) -> bool:
        pass
    @abc.abstractmethod
    async def needs_credentials(self) -> bool:
        pass

class NoAuth(AuthProvider):
    async def authenticate(self, app, *args,**kwargs) -> bool:
        username = "admin"
        user_id=0
    
        
        
        return  {"username":username,"user_id":user_id}
    async def authorize(self, username: str, permission: AuthPermission) -> bool:
        return True
    async def needs_credentials(self) -> bool:return False


class SimpleAuth(AuthProvider):
    async def authenticate(self, app, username: str, password: str, *args, **kwargs) -> bool:
       
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        async with app.db.execute("SELECT * FROM user WHERE username = ? AND pw = ?", (username, hashed_password)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"username": username, "user_id": row[0], "permission": AuthPermission(row[3])}
        return None

    async def authorize(self, username: str, permission: AuthPermission) -> bool:
        return True
    
    async def needs_credentials(self) -> bool:
        return True

    async def create_user(self, db: aiosqlite.Connection, username: str, password: str, permission: AuthPermission) -> bool:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor = await db.execute("SELECT * FROM user WHERE username = ?", (username,))
        row = await cursor.fetchone()
        if row:
            return False
        
        
        await db.execute("INSERT INTO user (username, pw, permission) VALUES (?, ?, ?)", (username, hashed_password, permission.value))
        await db.commit()
        return True
