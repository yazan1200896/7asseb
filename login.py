from database import DatabaseConnector
from fastapi import HTTPException

class LoginManager:
    def __init__(self, db_connector: DatabaseConnector, session: dict):
        self.db_connector = db_connector
        self.session = session

    def authenticate_user(self, username: str, password: str):
        """
        Authenticate the user by username and password.
        """
        try:
            cursor = self.db_connector.get_cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                # Store user in session if authentication succeeds
                self.session["user"] = user
                return {"status": "success", "user": user}
            else:
                return {"status": "failure", "message": "Invalid username or password"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Authentication error: {e}")
        finally:
            cursor.close()

    def is_logged_in(self) -> bool:
        """
        Check if the user is logged in by verifying the session.
        """
        return "user" in self.session

    def has_role(self, role: str) -> bool:
        """
        Check if the logged-in user has the required role.
        """
        if not self.is_logged_in():
            return False
        return self.session["user"].get("role") == role

    def logout(self):
        """
        Clear the user's session to log out.
        """
        self.session.clear()
