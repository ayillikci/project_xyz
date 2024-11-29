import React, { useEffect, useState } from "react";
import { getUserOffers } from "../api";

const UserProfile = () => {
  const [offers, setOffers] = useState([]);
  const [error, setError] = useState("");

  const userId = localStorage.getItem("userId"); // Assume userId is stored after login
  const token = localStorage.getItem("token");   // Assume token is stored after login

  useEffect(() => {
    const fetchOffers = async () => {
      try {
        const data = await getUserOffers(userId, token);
        setOffers(data);
      } catch (err) {
        console.error(err.message);
        setError("Failed to load offers. Please try again later.");
      }
    };

    fetchOffers();
  }, [userId, token]);

  if (!userId || !token) {
    return <p>Please log in to view your profile.</p>;
  }

  return (
    <div style={{ maxWidth: "800px", margin: "50px auto" }}>
      <h2>Your Offers</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {offers.length === 0 ? (
          <p>No offers available.</p>
        ) : (
          offers.map((offer) => (
            <li key={offer.id} style={{ marginBottom: "20px", listStyle: "none" }}>
              <h3>{offer.title}</h3>
              <p>{offer.description}</p>
              <p>Price: ${offer.price}</p>
              <p>Status: {offer.status}</p>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default UserProfile;
