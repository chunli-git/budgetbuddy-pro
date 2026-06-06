import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/client";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");

    try {
      await api.post("/auth/register", formData);

      setSuccess("Compte créé avec succès. Tu peux maintenant te connecter.");

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (error) {
      setError("Impossible de créer le compte. Vérifie les informations.");
    }
  }

  return (
    <div>
      <h1>Créer un compte</h1>
      <p>Commence à gérer ton budget avec BudgetBuddy Pro.</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Nom complet</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Mot de passe</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && <p>{error}</p>}
        {success && <p>{success}</p>}

        <button type="submit">Créer mon compte</button>
      </form>

      <p>
        Déjà un compte ? <Link to="/login">Se connecter</Link>
      </p>
    </div>
  );
}

export default Register;