

# API Documentation

This document outlines all the available API endpoints for interacting with the backend services. The backend is built using FastAPI and provides functionalities for managing products, suppliers, and orders.

## Base URL

```
http://127.0.0.1:8000
```

---

## Product APIs

### 1. **Add Product**
- **URL**: `/add_product/`
- **Method**: `GET`
- **Parameters** (Query):
  - `name` (str): Name of the product.
  - `quantity` (int): Quantity in stock.
  - `purchase_price` (float): Purchase price of the product.
  - `selling_price` (float): Selling price of the product.
  - `barcode` (str): Unique identifier for the product.
  - `date` (str): Date added (format: `YYYY-MM-DD`).
  - `images` (str): URL or path to product images.

**Example**:
```plaintext
http://127.0.0.1:8000/add_product/?name=Milk&quantity=10&purchase_price=5.5&selling_price=7.0&barcode=1234567890&date=2024-11-12&images=image.jpg
```

---

### 2. **Get Product**
- **URL**: `/get_product/`
- **Method**: `GET`
- **Parameters** (Query):
  - `barcode` (str): The barcode of the product to retrieve.

**Example**:
```plaintext
http://127.0.0.1:8000/get_product/?barcode=1234567890
```

---

### 3. **Delete Product**
- **URL**: `/delete_product/`
- **Method**: `GET`
- **Parameters** (Query):
  - `barcode` (str): The barcode of the product to delete.

**Example**:
```plaintext
http://127.0.0.1:8000/delete_product/?barcode=1234567890
```

---

### 4. **Decrement Product Quantity**
- **URL**: `/decrement_quantity/`
- **Method**: `GET`
- **Parameters** (Query):
  - `barcode` (str): The barcode of the product.
  - `amount` (int): Amount to decrement.

**Example**:
```plaintext
http://127.0.0.1:8000/decrement_quantity/?barcode=1234567890&amount=2
```

---

### 5. **Increment Product Quantity**
- **URL**: `/increment_quantity/`
- **Method**: `GET`
- **Parameters** (Query):
  - `barcode` (str): The barcode of the product.
  - `amount` (int): Amount to increment.

**Example**:
```plaintext
http://127.0.0.1:8000/increment_quantity/?barcode=1234567890&amount=5
```

---

### 6. **Get All Products**
- **URL**: `/get_all_products/`
- **Method**: `GET`

**Example**:
```plaintext
http://127.0.0.1:8000/get_all_products/
```

---

## Supplier APIs

### 1. **Add Supplier**
- **URL**: `/add_supplier/`
- **Method**: `GET`
- **Parameters** (Query):
  - `name` (str): Supplier's name.
  - `phone` (str): Supplier's phone number.
  - `address` (str): Supplier's address.

**Example**:
```plaintext
http://127.0.0.1:8000/add_supplier/?name=ABC&phone=123456789&address=Main Street
```

---

### 2. **Get Supplier**
- **URL**: `/get_supplier/`
- **Method**: `GET`
- **Parameters** (Query):
  - `name` (str): Supplier's name.

**Example**:
```plaintext
http://127.0.0.1:8000/get_supplier/?name=ABC
```

---

### 3. **Delete Supplier**
- **URL**: `/delete_supplier/`
- **Method**: `GET`
- **Parameters** (Query):
  - `name` (str): Supplier's name.

**Example**:
```plaintext
http://127.0.0.1:8000/delete_supplier/?name=ABC
```

---

## Order APIs

### 1. **Create Order**
- **URL**: `/create_order/`
- **Method**: `GET`
- **Parameters** (Query):
  - `supplier_name` (str): Name of the supplier.
  - `products` (str): Comma-separated barcodes of products.
  - `quantities` (str): Comma-separated quantities corresponding to the products.

**Example**:
```plaintext
http://127.0.0.1:8000/create_order/?supplier_name=ABC&products=1234567890,9876543210&quantities=5,3
```

---

### 2. **Update Order State**
- **URL**: `/update_order_state/`
- **Method**: `GET`
- **Parameters** (Query):
  - `order_id` (int): The ID of the order to update.
  - `new_state` (str): The new state of the order (e.g., `pending`, `completed`, `cancelled`).

**Example**:
```plaintext
http://127.0.0.1:8000/update_order_state/?order_id=1&new_state=completed
```

---

### 3. **Get Order**
- **URL**: `/get_order/`
- **Method**: `GET`
- **Parameters** (Query):
  - `order_id` (int): The ID of the order to retrieve.

**Example**:
```plaintext
http://127.0.0.1:8000/get_order/?order_id=1
```

---

### 4. **Delete Order**
- **URL**: `/delete_order/`
- **Method**: `GET`
- **Parameters** (Query):
  - `order_id` (int): The ID of the order to delete.

**Example**:
```plaintext
http://127.0.0.1:8000/delete_order/?order_id=1
```

---

### Notes for Frontend Developers:
1. **Date Format**: Ensure that all date values follow the `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS` format.
2. **Error Handling**: All APIs return error messages in JSON format with appropriate HTTP status codes.
3. **Testing**: Test the endpoints using tools like Postman or directly in the browser by appending query parameters.

---
