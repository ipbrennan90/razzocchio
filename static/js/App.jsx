import React from 'react';
import Home from './containers/Home';
import Login from './containers/Login';

import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

export default class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Link to="/">Home</Link>
                    <Link to="/login">Login</Link>
                    <Route exact path="/" component={Home} />
                    <Route path="/login" component={Login} />
                </div>
            </Router>
        );
    }
}
