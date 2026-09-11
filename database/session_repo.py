import uuid
from datetime import datetime
from typing import List, Dict, Optional
from database.connection import get_db

def create_session(
    goal: str = "Healthy Maintenance",
    preference: str = "Vegetarian",
    calorie_target: int = 2000,
    title: str = "New Consultation"
) -> str:
    """
    Creates a new consultation session and returns the session_id (UUID string).
    """
    session_id = str(uuid.uuid4())
    db = get_db()
    now = datetime.now()
    
    doc = {
        "session_id": session_id,
        "title": title,
        "health_goal": goal,
        "diet_preference": preference,
        "calorie_target": calorie_target,
        "created_at": now,
        "updated_at": now,
        "message_count": 0
    }
    
    if db is not None:
        try:
            db.sessions.insert_one(doc)
        except Exception as e:
            print(f"[MongoDB Error] create_session: {e}")
            
    return session_id

def save_message(session_id: str, role: str, content: str) -> bool:
    """
    Persists a chat message and updates session metadata.
    """
    db = get_db()
    if db is None:
        return False
        
    now = datetime.now()
    msg_doc = {
        "message_id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": now
    }
    
    try:
        db.messages.insert_one(msg_doc)
        
        # Update session update timestamp and message count
        db.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {"updated_at": now},
                "$inc": {"message_count": 1}
            }
        )
        return True
    except Exception as e:
        print(f"[MongoDB Error] save_message: {e}")
        return False

def get_session_messages(session_id: str) -> List[Dict]:
    """
    Retrieves all messages for a session in chronological order.
    """
    db = get_db()
    if db is None:
        return []
        
    try:
        cursor = db.messages.find(
            {"session_id": session_id},
            {"_id": 0, "role": 1, "content": 1, "timestamp": 1}
        ).sort("timestamp", 1)
        
        return list(cursor)
    except Exception as e:
        print(f"[MongoDB Error] get_session_messages: {e}")
        return []

def list_sessions() -> List[Dict]:
    """
    Returns all consultation sessions sorted by last updated time (descending).
    """
    db = get_db()
    if db is None:
        return []
        
    try:
        cursor = db.sessions.find(
            {},
            {"_id": 0}
        ).sort("updated_at", -1)
        
        return list(cursor)
    except Exception as e:
        print(f"[MongoDB Error] list_sessions: {e}")
        return []

def get_session(session_id: str) -> Optional[Dict]:
    """
    Fetches a single session metadata document.
    """
    db = get_db()
    if db is None:
        return None
        
    try:
        return db.sessions.find_one({"session_id": session_id}, {"_id": 0})
    except Exception as e:
        print(f"[MongoDB Error] get_session: {e}")
        return None

def update_session_title(session_id: str, title: str) -> bool:
    """
    Updates the display title of a consultation session.
    """
    db = get_db()
    if db is None:
        return False
        
    try:
        clean_title = title[:50].strip()
        db.sessions.update_one(
            {"session_id": session_id},
            {"$set": {"title": clean_title, "updated_at": datetime.now()}}
        )
        return True
    except Exception as e:
        print(f"[MongoDB Error] update_session_title: {e}")
        return False

def delete_session(session_id: str) -> bool:
    """
    Permanently deletes a session, its messages, and any associated meal logs.
    """
    db = get_db()
    if db is None:
        return False
        
    try:
        db.messages.delete_many({"session_id": session_id})
        db.meal_logs.delete_many({"session_id": session_id})
        db.sessions.delete_one({"session_id": session_id})
        return True
    except Exception as e:
        print(f"[MongoDB Error] delete_session: {e}")
        return False

def log_meal(
    session_id: str,
    meal_type: str,
    items: str,
    calories: int,
    protein_g: float = 0.0,
    carbs_g: float = 0.0,
    fat_g: float = 0.0
) -> str:
    """
    Logs a recorded meal into MongoDB.
    """
    db = get_db()
    meal_id = str(uuid.uuid4())
    now = datetime.now()
    
    doc = {
        "meal_id": meal_id,
        "session_id": session_id,
        "meal_type": meal_type,
        "items": items,
        "calories": calories,
        "macros": {
            "protein": protein_g,
            "carbs": carbs_g,
            "fat": fat_g
        },
        "logged_at": now
    }
    
    if db is not None:
        try:
            db.meal_logs.insert_one(doc)
        except Exception as e:
            print(f"[MongoDB Error] log_meal: {e}")
            
    return meal_id

def get_meal_logs(session_id: str) -> List[Dict]:
    """
    Fetches all meals logged for a consultation session.
    """
    db = get_db()
    if db is None:
        return []
        
    try:
        cursor = db.meal_logs.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("logged_at", -1)
        return list(cursor)
    except Exception as e:
        print(f"[MongoDB Error] get_meal_logs: {e}")
        return []
