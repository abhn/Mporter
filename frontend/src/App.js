import React from "react";
import {
  BrowserRouter as Router,
  Route,
  HashRouter,
  Switch,
  Link
} from 'react-router-dom';
import Login from "./login";
import Tasks from "./tasks";
import Mentors from "./mentors";
import Settings from "./settings";
import Footer from "./footer";
import Nav from "./nav";
import styled from 'styled-components';

const Container = styled.div`
    max-width: 768px;
    width: 100%;
    margin: 0 auto;

    display: flex;
    min-height: 100vh;
    flex-direction: column;
`;

const MainContent = styled.div`
    flex: 1;
`;

class App extends React.Component {

    componentDidMount() {
        if(!localStorage.getItem('token')) {
            window.location.href = '#/login'
        }
    }

    render () {
        return (
            <Container>
                <Nav/>
                <MainContent>
                    <HashRouter>
                        <Switch>
                            <Route exact path="/login" component={Login} />
                            <Route exact path="/tasks" component={Tasks} />
                            <Route exact path="/mentors" component={Mentors} />
                            <Route exact path="/settings" component={Settings} />
                        </Switch>
                    </HashRouter>
                </MainContent>
                <Footer/>
            </Container>
        )
    }
}

export default App;