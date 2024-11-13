from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse

from database import DatabaseConnector
from excel_exporter import ExcelExporter
from product import Product
from Supplier import Supplier
from order import Order

app = FastAPI()

# Initialize database connection and classes
db_connector = DatabaseConnector()
product = Product(db_connector)
supplier = Supplier(db_connector)
order = Order(db_connector)

# Product APIs
@app.get("/add_product/")
async def add_product(name: str, quantity: int, purchase_price: float, selling_price: float, images: str, barcode: str, date: str):
    return product.add_product(name, quantity, purchase_price, selling_price, images, barcode, date)

@app.get("/get_product/")
async def get_product(barcode: str):
    return product.get_product(barcode)

@app.get("/update_product/")
async def update_product(barcode: str, **kwargs):
    return product.update_product(barcode, **kwargs)

@app.get("/delete_product/")
async def delete_product(barcode: str):
    return product.delete_product(barcode)

@app.get("/increment_quantity/")
async def increment_quantity(barcode: str, amount: int):
    return product.increment_quantity(barcode, amount)

@app.get("/decrement_quantity/")
async def decrement_quantity(barcode: str, amount: int):
    return product.decrement_quantity(barcode, amount)

# Supplier APIs
@app.get("/add_supplier/")
async def add_supplier(name: str, phone: str, address: str):
    return supplier.add_supplier(name, phone, address)

@app.get("/get_supplier/")
async def get_supplier(supplier_id: int):
    return supplier.get_supplier(supplier_id)

@app.get("/update_supplier/")
async def update_supplier(supplier_id: int, **kwargs):
    return supplier.update_supplier(supplier_id, **kwargs)

@app.get("/delete_supplier/")
async def delete_supplier(supplier_id: int):
    return supplier.delete_supplier(supplier_id)

# Order APIs
@app.get("/create_order/")
async def create_order(supplier_id: int, barcodes: str, quantities: str, state: str = "Pending"):
    barcodes_list = barcodes.split(",")
    quantities_list = [int(q) for q in quantities.split(",")]
    return order.create_order(supplier_id, barcodes_list, quantities_list, state)

@app.get("/get_order/")
async def get_order(order_id: int):
    return order.get_order(order_id)

@app.get("/update_order_state/")
async def update_order_state(order_id: int, new_state: str):
    return order.update_order_state(order_id, new_state)

@app.get("/delete_order/")
async def delete_order(order_id: int):
    return order.delete_order(order_id)
@app.get("/create_products_excel/")
async def create_products_excel():
    file_path, error = ExcelExporter.export_products_to_excel()
    if error:
        raise HTTPException(status_code=500, detail=f"Failed to create Excel file: {error}")
    if not file_path:
        raise HTTPException(status_code=404, detail="No products found.")
    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],  # Use the filename directly
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Welcome to the Product, Supplier, and Order API!"}
