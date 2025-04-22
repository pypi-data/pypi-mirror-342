import uuid
import time
class SimpleSessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, data = {}, expiration =7200):
        session_id = str(uuid.uuid4())
        session_object = data
        session_object["_expires"]= time.time() + expiration
        self.sessions[session_id] = session_object
        return session_id

    def get_session(self, session_id):
        if session_id not in self.sessions:
            return None
        return self.sessions.get(session_id)
    def get_session_autocreate(self, session_id, data = {}, expiration =7200):
        if session_id not in self.sessions:
            return self.create_session(data, expiration)
        return self.sessions[session_id]
    
    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
    def expire_sessions(self):
         self.sessions = {sid: s for sid, s in self.sessions.items() if s["_expires"] >= time.time()}