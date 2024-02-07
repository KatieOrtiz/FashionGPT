import React from 'react';
import { Link } from 'react-router-dom';

const Layout = ({ children }) => {
  return (
    <div>
      <header className="App-header">
        <h1>Welcome to FashionGPT</h1>
        <p className="disc">we help our users create outfits based on certain factors the users input with the help of ChatGPT.</p>
        <div>
          <Link to="/login"><button>Login</button></Link>
          <button>Sign Up</button>
        </div>
      </header>
      <main>{children}</main>
      <footer>
        <p>&copy; {new Date().getFullYear()} My Website</p>
      </footer>
    </div>
  );
};

export default Layout;
