import app
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from database import DatabaseConnector
from excel_exporter import ExcelExporter
from product import Product
from Supplier import Supplier
from order import Order
from PDFManager import PDFManager
from login import LoginManager  # Import the LoginManager class
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Initialize database connection and classes
db_connector = DatabaseConnector()
product = Product(db_connector)
supplier = Supplier(db_connector)
order = Order(db_connector)
pdf_manager = PDFManager(db_connector)
login_manager = LoginManager(db_connector=db_connector, session={})

# Jinja2 template rendering
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


# ---------------------------
# Product APIs
# ---------------------------
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


# ---------------------------
# Supplier APIs
# ---------------------------
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


# ---------------------------
# Order APIs
# ---------------------------
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
        filename=file_path.split("/")[-1],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# PDF Export API
@app.get("/create_products_pdf/")
async def create_products_pdf():
    file_path = pdf_manager.generate_products_pdf()
    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/pdf"
    )


# ---------------------------
# Login APIs
# ---------------------------
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/home")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Handle login logic.
    """
    result = login_manager.authenticate_user(username, password)
    if result["status"] == "success":
        # Set the session
        request.session["user"] = result["user"]
        return RedirectResponse(url="/home", status_code=303)
    else:
        # Render login page with error message
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": result["message"]}
        )

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("home.html", {"request": request, "user": user["username"]})
@app.get("/logout" )
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/admin")
async def admin_dashboard(request: Request):
    if not login_manager.is_logged_in():
        return RedirectResponse(url="/login")
    if not login_manager.has_role("admin"):
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Welcome to the admin dashboard"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Product, Supplier, and Order API!"}
