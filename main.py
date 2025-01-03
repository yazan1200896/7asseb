from aifc import Error
from pathlib import Path

from fastapi import FastAPI
from ai import AI, InferenceHTTPClient

from inference_sdk import InferenceHTTPClient

from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from database import DatabaseConnector
from excel_exporter import ExcelExporter
from product import Product
from Supplier import Supplier
from order import Order
#from PDFManager import PDFManager
from login import LoginManager  # Import the LoginManager class
from fastapi.staticfiles import StaticFiles
from user import User
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Initialize database connection and classes
db_connector = DatabaseConnector()
product = Product(db_connector)
supplier = Supplier(db_connector)
order = Order(db_connector)
#pdf_manager = PDFManager(db_connector)
login_manager = LoginManager(db_connector=db_connector, session={})

# Jinja2 template rendering
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")





CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Vg1cHJhZQ7cqNjnGSYVk"
)

result = CLIENT.infer("11.jpg", model_id="jordan-coins-detection-nqdbs/5")
print (result)

@app.get("/cashier/", response_class=HTMLResponse)
async def get_cashier_page(request: Request):
    return templates.TemplateResponse("cashier.html", {"request": request})

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
#@app.get("/create_products_pdf/")
#async def create_products_pdf():
 #   file_path = pdf_manager.generate_products_pdf()
  #  return FileResponse(
   #     path=file_path,
    #    filename=file_path.split("/")[-1],
     #   media_type="application/pdf"
    #)


# ---------------------------
# Login APIs
# ---------------------------
# In your login route (assuming LoginManager handles authentication)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    result = login_manager.authenticate_user(username, password)

    if result["status"] == "success":
        user = result["user"]  # Assuming `user` contains 'username', 'email', and 'role'

        # Store user information and role in session
        request.session["user"] = {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],  # Ensure the role is stored
        }

        # Redirect to the home page or admin dashboard based on the role
        if user["role"] == "admin":
            return RedirectResponse(url="/admin", status_code=303)
        return RedirectResponse(url="/home", status_code=303)

    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": result["message"]}
        )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # Check if the user is already logged in by checking session
    if request.session.get("user"):
        # If session exists, redirect directly to the home page
        return RedirectResponse(url="/home")
    # If no session, show the login page
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    # Retrieve user data from session
    user = request.session.get("user")

    # If no user session exists, redirect to login page
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    print(request.session.get("user"))

    # Pass user data to the home page template
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@app.get("/logout" )
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not login_manager.is_logged_in():
        return RedirectResponse(url="/login")
    if not login_manager.has_role("admin"):
        raise HTTPException(status_code=403, detail="Access forbidden")

    try:
        cursor = db_connector.get_cursor(dictionary=True)
        # Query the database for users (using 'username' as the unique identifier)
        query = "SELECT username, email, role, password FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return templates.TemplateResponse("admin_dashboard.html", {"request": request, "users": users})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")
    finally:
        cursor.close()


@app.post("/delete_user/")
async def delete_user(user_id: int):
    try:
        cursor = db_connector.get_cursor()
        # Check the user's role before deleting
        query_check = "SELECT role FROM users WHERE username = %s"
        cursor.execute(query_check, (user_id,))
        user = cursor.fetchone()

        # Delete the user
        query_delete = "DELETE FROM users WHERE username = %s"
        cursor.execute(query_delete, (user_id,))
        db_connector.connection.commit()
        return {"message": "User deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")
    finally:
        cursor.close()

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str
@app.post("/add_user/")
async def add_user(user: UserCreateRequest):
    return User.add_user(db_connector, user.username, user.email, user.role, user.password)



@app.delete("/delete_user/{username}")
async def delete_user(username: str):  # Accept 'username' as a path parameter
    user_instance = User(db_connector)
    return user_instance.delete_user(username)

@app.post("/edit_password/")
async def edit_password(user_id: int, new_password: str):
    try:
        cursor = db_connector.get_cursor()
        query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query, (new_password, user_id))
        db_connector.connection.commit()
        return {"message": "Password updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating password: {e}")
    finally:
        cursor.close()


# Root endpoint

@app.get("/")
async def login_page(request: Request):
    # Check if the user is already logged in by checking session
    if request.session.get("user"):
        # If session exists, redirect directly to the home page
        return RedirectResponse(url="/home")
    # If no session, show the login page
    return templates.TemplateResponse("login.html", {"request": request})

user_manager = User(db_connector)

@app.get("/get_all_products/")
async def get_all_products():
    products = product.get_all_products()
    if "error" in products:
        return JSONResponse(content=products, status_code=500)

    # Transform product data to a JSON-friendly format
    product_list = []
    for prod in products:
        product_list.append({
            "id": prod[0],
            "name": prod[1],
            "quantity": prod[2],
            "purchase_price": prod[3],
            "selling_price": prod[4],
            "images": prod[5],
            "barcode": prod[6],
            "date": str(prod[7]) if prod[7] else None
        })

    return product_list
@app.post("/checkout/")
async def checkout(cart: list):
    try:
        cursor = db_connector.get_cursor()
        for item in cart:
            cursor.execute("UPDATE product SET quantity = quantity - %s WHERE barcode = %s", (item['quantity'], item['barcode']))
        db_connector.commit()
        return {"message": "Checkout successful"}
    except Error as e:
        db_connector.rollback()
        return {"error": f"Failed to process checkout: {e}"}


from fastapi import FastAPI, File, UploadFile
import cv2
import os


class Video:
    def __init__(self, save_dir: str = "frames"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def save_uploaded_file(self, file: UploadFile, temp_name: str) -> str:
        """
        Save the uploaded file temporarily.
        """
        video_path = f"{temp_name}_{file.filename}"
        with open(video_path, "wb") as f:
            f.write(file.file.read())
        return video_path

    def extract_frames(self, video_path: str, frame_interval: int = 30) -> list:
        """
        Extract frames from the video and save them.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Could not open the video file.")

        frame_count = 0
        saved_frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_path = os.path.join(self.save_dir, f"frame_{frame_count}.jpg")
                cv2.imwrite(frame_path, frame)
                saved_frames.append(frame_path)

            frame_count += 1

        cap.release()
        return saved_frames

    def clean_up(self, file_path: str):
        """
        Delete temporary files.
        """
        if os.path.exists(file_path):
            os.remove(file_path)

video_processor = Video()


@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file, extract frames, and save them with auto-incremented names based on the video name.
    """
    try:
        # Save uploaded video temporarily
        video_name = Path(file.filename).stem  # Get the video name without extension
        temp_video_path = video_processor.save_uploaded_file(file, "temp")

        # Extract frames with updated naming
        frames = video_processor.extract_frames(temp_video_path, frame_interval=30)

        # Rename frames based on the video file's name
        renamed_frames = []
        for idx, frame_path in enumerate(frames, start=1):
            new_name = f"{video_name}_{idx}.jpg"
            new_path = os.path.join(video_processor.save_dir, new_name)
            os.rename(frame_path, new_path)
            renamed_frames.append(new_path)

        # Clean up the temporary video file
        video_processor.clean_up(temp_video_path)

        return {"message": "Frames extracted successfully.", "frames": renamed_frames}
    except Exception as e:
        return {"error": str(e)}




# Configure the Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Vg1cHJhZQ7cqNjnGSYVk"
)

# Initialize AI with frames directory and client
ai_processor = AI(frames_dir="frames", client=CLIENT)


@app.get("/infer-images/")
def infer_images():
    """
    Get all images in the frames directory and infer them using the API,
    then return the image with the highest total value and its value.
    """
    try:
        # Call the method from the AI class
        model_id = "jordan-coins-detection-nqdbs/5"
        result = ai_processor.infer_images(model_id=model_id)

        if result["best_image"]:
            return {
                "message": "Inference completed successfully.",
                "best_image": result["best_image"],
                "total_value": result["total_value"]
            }
        else:
            return {"message": "No images found or processed."}
    except Exception as e:
        return {"error": str(e)}
