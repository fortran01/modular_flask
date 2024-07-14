function login() {
  const customerId = document.getElementById("customer-id").value;

  axios
    .post("/login", { customer_id: customerId })
    .then(function (response) {
      if (response.data.success) {
        document.getElementById("login-form").style.display = "none";
        document.getElementById("shopping-window").style.display = "block";
        loadProducts();
      } else {
        document.getElementById("result").innerHTML =
          "Error: " + response.data.error;
      }
    })
    .catch(function (error) {
      document.getElementById("result").innerHTML =
        "Error: " + error.response.data.error;
    });
}

function logout() {
  axios
    .get("/logout")
    .then(function (response) {
      if (response.data.success) {
        document.getElementById("login-form").style.display = "block";
        document.getElementById("shopping-window").style.display = "none";
        document.getElementById("product-list").innerHTML = "";
      }
    })
    .catch(function (error) {
      document.getElementById("result").innerHTML =
        "Error: " + error.response.data.error;
    });
}

function loadProducts() {
  axios
    .get("/products")
    .then(function (response) {
      const products = response.data.products;
      const productList = document.getElementById("product-list");

      products.forEach(function (product) {
        const productElement = document.createElement("div");
        productElement.innerHTML = `
              <img src="${product.image_url}" alt="${product.name}" width="100" height="100">
              <p>${product.name}</p>
              <p>Price: $${product.price}</p>
              <button onclick="addToCart(${product.id})">Add to Cart</button>
          `;
        productList.appendChild(productElement);
      });
    })
    .catch(function (error) {
      document.getElementById("result").innerHTML =
        "Error: " + error.response.data.error;
    });
}

function addToCart(productId) {
  // Add the selected product to the cart
  // You can implement the cart functionality as needed
  console.log("Added product to cart: " + productId);
}

function checkout() {
  const productIds = getProductIdsFromCart(); // Implement this function to get product IDs from the cart
  axios
    .post("/checkout", { product_ids: productIds })
    .then((response) => {
      if (
        response.data.invalid_products &&
        response.data.invalid_products.length > 0
      ) {
        displayInvalidProducts(response.data.invalid_products);
      }
      if (
        response.data.products_missing_category &&
        response.data.products_missing_category.length > 0
      ) {
        displayMissingCategoryProducts(response.data.products_missing_category);
      }
      document.getElementById(
        "result"
      ).innerHTML = `Checkout successful! You earned ${response.data.total_points_earned} points.`;
    })
    .catch((error) => {
      document.getElementById(
        "result"
      ).innerHTML = `Error: ${error.response.data.error}`;
    });
}

function displayInvalidProducts(invalidProducts) {
  const errorMessagesDiv = document.getElementById("error-messages");
  errorMessagesDiv.innerHTML =
    "<h3>Warning: Some products could not be processed</h3>";
  const ul = document.createElement("ul");
  invalidProducts.forEach((productId) => {
    const li = document.createElement("li");
    li.textContent = `Product ID ${productId} is invalid or not available.`;
    ul.appendChild(li);
  });
  errorMessagesDiv.appendChild(ul);
}

function displayMissingCategoryProducts(missingCategoryProducts) {
  const errorMessagesDiv = document.getElementById("error-messages");
  errorMessagesDiv.innerHTML +=
    "<h3>Warning: Some products are missing categories</h3>";
  const ul = document.createElement("ul");
  missingCategoryProducts.forEach((productId) => {
    const li = document.createElement("li");
    li.textContent = `Product ID ${productId} has no category defined.`;
    ul.appendChild(li);
  });
  errorMessagesDiv.appendChild(ul);
}
