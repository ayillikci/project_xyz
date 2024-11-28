import React, { useEffect, useState } from "react";
import { getOffers } from "./api";

function App() {
  const [offers, setOffers] = useState([]);

  useEffect(() => {
    getOffers().then(setOffers);
  }, []);

  return (
    <div>
      <h1>Offers</h1>
      <ul>
        {offers.map((offer) => (
          <li key={offer.id}>{offer.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

