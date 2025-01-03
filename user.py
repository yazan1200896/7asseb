from aifc import Error


class User:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    @classmethod
    def add_user(cls, db_connector, username, email, role, password):
        try:
            cursor = db_connector.get_cursor()
            cursor.execute(
                """
                INSERT INTO users (username, email, role, password, company_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (username, email, role, password, 2)
            )
            db_connector.commit()
            return {"message": "User added successfully"}
        except Error as e:
            db_connector.rollback()
            return {"error": f"Failed to add user: {e}"}

    def delete_user(self, username):
        try:
            cursor = self.db_connector.get_cursor()
            cursor.execute(
                "DELETE FROM users WHERE username = %s",  # Target 'username' column
                (username,)
            )
            self.db_connector.commit()
            if cursor.rowcount == 0:
                return {"message": "No user found with the given username"}
            return {"message": "User deleted successfully"}
        except Error as e:
            self.db_connector.rollback()
            return {"error": f"Failed to delete user: {e}"}
