import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/client";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchCurrentUser() {
      try {
        const response = await api.get("/auth/me");
        setUser(response.data);
      } catch (error) {
        setError("Impossible de charger l'utilisateur.");
      }
    }

    fetchCurrentUser();
  }, []);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div>
      <h1>Dashboard</h1>

      {user && (
        <p>
          Bienvenue, <strong>{user.full_name}</strong>
        </p>
      )}

      {error && <p>{error}</p>}

      <button onClick={handleLogout}>Se déconnecter</button>
    </div>
  );
}

export default Dashboard;