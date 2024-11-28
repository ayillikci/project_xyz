const BASE_URL = "http://localhost:8000";

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
  