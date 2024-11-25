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
