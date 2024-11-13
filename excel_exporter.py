import pandas as pd
from database import DatabaseConnector
from datetime import datetime

class ExcelExporter:
    @staticmethod
    def export_products_to_excel():
        # Connect to the database and fetch the products data
        db_connector = DatabaseConnector()
        try:
            cursor = db_connector.get_cursor()
            cursor.execute("SELECT name, quantity, purchase_price, selling_price, barcode, date FROM product")  # Fetch only required columns
            products = cursor.fetchall()

            if not products:
                return None, "No products found."  # If no products are found, return an error message

            # Create a DataFrame from the products data
            df = pd.DataFrame(products, columns=["name", "quantity", "purchase_price", "selling_price", "barcode", "date"])

            # Add current date to the filename to avoid overwriting
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"products_{current_date}.xlsx"

            # Export DataFrame to Excel file
            df.to_excel(filename, index=False)
            return filename, None  # Return file path and no error
        except Exception as e:
            return None, str(e)  # Return error message if an exception occurs
