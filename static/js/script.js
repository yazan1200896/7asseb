// Handle login form submission
document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    if (response.ok) {
      const data = await response.json();
      document.getElementById("message").style.color = "green";
      document.getElementById("message").textContent = data.message;
    } else {
      const error = await response.json();
      document.getElementById("message").textContent = error.detail;
    }
  } catch (err) {
    console.error("Error:", err);
    document.getElementById("message").textContent = "An error occurred. Please try again.";
  }
});

// Product search function
document.getElementById("search-product-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const barcode = document.getElementById("product-barcode").value;

  try {
    const response = await fetch(`/get_product/?barcode=${encodeURIComponent(barcode)}`);

    if (response.ok) {
      const data = await response.json();
      if (data.message) {
        document.getElementById("product-details").textContent = data.message;
      } else {
        // Display product details
        const productDetails = `
          Name: ${data.name}<br>
          Quantity: ${data.quantity}<br>
          Price: ${data.selling_price}<br>
          Barcode: ${data.barcode}
        `;
        document.getElementById("product-details").innerHTML = productDetails;
      }
    } else {
      const error = await response.json();
      document.getElementById("product-details").textContent = error.detail;
    }
  } catch (err) {
    console.error("Error:", err);
    document.getElementById("product-details").textContent = "An error occurred. Please try again.";
  }
});

// Add product to cart
let cart = [];

document.getElementById("add-to-cart").addEventListener("click", () => {
  const productBarcode = document.getElementById("product-barcode").value;
  const productQuantity = document.getElementById("quantity").value;

  if (productBarcode && productQuantity) {
    cart.push({ barcode: productBarcode, quantity: parseInt(productQuantity) });
    displayCart();
  } else {
    alert("Please select a product and quantity.");
  }
});

// Display cart details
function displayCart() {
  const cartContainer = document.getElementById("cart-container");
  cartContainer.innerHTML = '';

  cart.forEach(item => {
    const listItem = document.createElement('li');
    listItem.textContent = `Barcode: ${item.barcode}, Quantity: ${item.quantity}`;
    cartContainer.appendChild(listItem);
  });

  updateTotalAmount();
}

// Calculate the total amount
async function updateTotalAmount() {
  let totalAmount = 0;

  for (const item of cart) {
    const response = await fetch(`/get_product/?barcode=${encodeURIComponent(item.barcode)}`);

    if (response.ok) {
      const data = await response.json();
      if (data.selling_price) {
        totalAmount += data.selling_price * item.quantity;
      }
    }
  }

  document.getElementById("total-amount").textContent = `Total: $${totalAmount.toFixed(2)}`;
}

// Checkout (Finalizing purchase)
document.getElementById("checkout").addEventListener("click", async () => {
  if (cart.length === 0) {
    alert("Your cart is empty.");
    return;
  }

  try {
    const response = await fetch("/checkout/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ cart }),
    });

    if (response.ok) {
      const data = await response.json();
      alert("Checkout successful: " + data.message);
      cart = []; // Clear the cart
      displayCart();
    } else {
      const error = await response.json();
      alert("Checkout failed: " + error.detail);
    }
  } catch (err) {
    console.error("Error:", err);
    alert("An error occurred during checkout.");
  }
});

// Loading navbar when the page loads
document.addEventListener("DOMContentLoaded", () => {
  fetch("././templates/navbar.html")
    .then(response => response.text())
    .then(html => {
      document.getElementById("navbar").innerHTML = html;

      // Highlight the active link
      const links = document.querySelectorAll("nav a");
      links.forEach(link => {
        if (link.href === window.location.href) {
          link.style.fontWeight = "bold";
          link.style.textDecoration = "underline";
        }
      });
    })
    .catch(error => console.error("Error loading navbar:", error));
});
