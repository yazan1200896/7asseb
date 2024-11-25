from mysql.connector import Error
from database import DatabaseConnector


class LoginManager:
    def __init__(self, db_connector: DatabaseConnector, session: dict):
        """
        Initialize LoginManager with a database connector and a session storage.
        :param db_connector: DatabaseConnector instance for database interactions.
        :param session: A dictionary-like object to manage session data.
        """
        self.db_connector = db_connector
        self.session = session

    def authenticate_user(self, username: str, password: str):
        """
        Authenticate a user by checking their credentials in the database.
        :param username: The username to authenticate.
        :param password: The password to authenticate.
        :return: A dictionary with user details if authenticated, or an error message.
        """
        try:
            cursor = self.db_connector.get_cursor(dictionary=True)
            query = """
            SELECT username, email, company_id, p_num, role
            FROM users
            WHERE username = %s AND password = %s
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                # User authenticated successfully, store session
                self.session["user"] = {
                    "username": user["username"],
                    "role": user["role"]
                }
                return {"status": "success", "user": user}
            else:
                # User not found or invalid credentials
                return {"status": "error", "message": "Invalid username or password."}
        except Error as e:
            return {"status": "error", "message": f"Database error: {e}"}
        finally:
            cursor.close()

    def is_logged_in(self):
        """
        Check if a user is currently logged in.
        :return: True if a user is logged in, False otherwise.
        """
        return "user" in self.session

    def get_logged_in_user(self):
        """
        Retrieve the currently logged-in user's information from the session.
        :return: A dictionary containing the user's session data, or None if not logged in.
        """
        return self.session.get("user", None)

    def logout_user(self):
        """
        Logout the currently logged-in user by clearing the session.
        """
        self.session.clear()

    def has_role(self, required_role: str):
        """
        Check if the currently logged-in user has the required role.
        :param required_role: The role to check.
        :return: True if the user has the required role, False otherwise.
        """
        if not self.is_logged_in():
            return False
        user_role = self.session["user"].get("role", None)
        return user_role == required_role
