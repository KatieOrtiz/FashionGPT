import React from 'react';

function Login() {
  return (
    <div>
      <h2>Login Page</h2>
      <form>
        {/* Add form inputs and buttons here */}
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
