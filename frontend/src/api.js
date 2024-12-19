//const BASE_URL = "http://localhost:8000";
const BASE_URL = process.env.API_URL //"http://localhost/api"

export const loginUser = async (email, password) => {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error("Login failed");
  }
  return response.json(); // Typically returns a token or user data
};

export const getUserOffers = async (userId, token) => {
    const response = await fetch(`${BASE_URL}/users/${userId}/offers`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error("Failed to fetch user offers");
    }
    return response.json();
  };  

export const signupUser = async (email, username, password, userType) => {
    const response = await fetch(`${BASE_URL}/auth/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, username, password, user_type: userType }),
    });
    if (!response.ok) {
      throw new Error("Signup failed");
    }
    return response.json();
  };