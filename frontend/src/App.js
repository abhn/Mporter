import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';
import Login from "./login";
import Tasks from "./tasks";
import Mentors from "./mentors";
import Settings from "./settings";

class App extends React.Component {
  render () {
    return (
      <Router>
        <Route exact path="/login" component={Login} />
        {/* <Route exact path="/tasks" component={Tasks} />
        <Route exact path="/mentors" component={Mentors} />
        <Route exact path="/settings" component={Settings} /> */}
      </Router>
    )
  }
}

export default App;