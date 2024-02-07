import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './Login';
import Layout from './Layout'; // Import the Layout component
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/hello')
      .then(response => response.json())
      .then(data => setMessage(data.message));
  }, []);

  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/">
          <Layout>
            <p>{message || "Loading message from the backend..."}</p>
          </Layout>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
