const BASE_URL = "http://localhost:8000";

export const getOffers = async () => {
  const response = await fetch(`${BASE_URL}/offers`);
  return response.json();
};
