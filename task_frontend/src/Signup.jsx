import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import './App.css';

function App() {
  let [email, setEmail] = useState("");
  let [password, setPassword] = useState("");
  let [username, setUsername] = useState("");
  let [message, setMessage] = useState("");
  let [errorMessage, setError] = useState("");
  const navigate = useNavigate();

  async function signUp(event) {
    event.preventDefault();
    
    const url = 'http://127.0.0.1:8000/signup';
    const data = {
      username: username,
      email: email,
      password: password,
    }
    try {
    const response = await fetch(url, {
      method: "POST",
      headers: {'Content-Type': 'application/Json'},
      body: JSON.stringify(data)
    })
    const rez = await response.json();
    if (response.status === 200) {
      setMessage(rez.message);
      sessionStorage.setItem('token', rez.token);
      setTimeout(() => navigate("/home"), 2000);
    }
    else {
      setError(rez.error)
    }
  }catch(error) {
    setError('Unable to sign you up at this time, kindly try again later')
  }
  }
  
  return(
    <div className="container">
    <div className="rightSection">
    <h2>Hello, welcome to Task Management App</h2>
    <form className="signupForm" onSubmit={signUp}>
      <label htmlFor="username">Username</label><br/>
      <input required type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)}></input><br/>
      <label htmlFor="email">Email</label><br/>
      <input required type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)}></input><br/>
      <label htmlFor="password">Password</label><br/>
      <input required type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)}></input><br/>
      <button type="submit" className="signBut">Signup</button>
    </form>
    {errorMessage ? <p className="error">{errorMessage}</p> : <p className="success">{message}</p>}
    <p>Have an account?<Link to="/login">Sign in</Link></p>
    </div>
    <div className="imageBg">
    </div>
    </div>
  );
}

export default App
