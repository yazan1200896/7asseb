import logging
from fastapi import HTTPException
from fpdf import FPDF
from database import DatabaseConnector


class PDFManager:
    def __init__(self, db_connector):
        self.db_connector = DatabaseConnector
        logging.basicConfig(level=logging.INFO)

    def generate_products_pdf(self):
        logging.info("Connecting to the database...")
        conn = self.db_connector
        print(self.db_connector)
        if not conn:
            logging.error("Failed to connect to the database.")
            raise HTTPException(status_code=500, detail="Failed to connect to the database.")

        try:
            logging.info("Fetching products...")
            cursor = conn.get_cursor()
            query = "SELECT name, quantity, purchase_price, selling_price FROM product"
            cursor.execute(query)
            products = cursor.fetchall()
            logging.info(f"Products retrieved: {products}")

            if not products:
                logging.warning("No products found in the database.")
                raise HTTPException(status_code=404, detail="No products found.")

            logging.info("Creating PDF...")
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Products Report", ln=True, align="C")
            pdf.ln(10)

            # Add table headers
            pdf.set_font("Arial", size=10)
            pdf.cell(50, 10, txt="Name", border=1, align="C")
            pdf.cell(30, 10, txt="Quantity", border=1, align="C")
            pdf.cell(40, 10, txt="Purchase Price", border=1, align="C")
            pdf.cell(40, 10, txt="Selling Price", border=1, align="C")
            pdf.ln()

            # Add product rows
            for product in products:
                logging.info(f"Adding product to PDF: {product}")
                pdf.cell(50, 10, txt=str(product[0]), border=1)
                pdf.cell(30, 10, txt=str(product[1]), border=1)
                pdf.cell(40, 10, txt=f"${product[2]:.2f}", border=1)
                pdf.cell(40, 10, txt=f"${product[3]:.2f}", border=1)
                pdf.ln()

            # Save the PDF
            file_path = "products_report.pdf"
            pdf.output(file_path)
            logging.info(f"PDF successfully created at {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Error generating PDF: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
