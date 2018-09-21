import React from 'react';
import { Input, Button } from 'semantic-ui-react';
import styled from 'styled-components';

const Wrapper = styled.div`
    max-width: 400px;
    margin: 30px auto;
`;

class Login extends React.Component {

    constructor() {
        super();
        this.state = {
            email: '',
            password: ''
        };
    }

    componentDidMount() {
        if (localStorage.getItem('token')) {
            this.props.history.push('/tasks');
        }
    }

    emailChange = (e) => {
        this.setState({
            email: e.target.value
        })
    }

    passwordChange = (e) => {
        this.setState({
            password: e.target.value
        })
    }

    submit = () => {
        fetch('/api/auth', {
            method: 'post',
            body: JSON.stringify({
                email: this.state.email,
                password: this.state.password
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            localStorage.setItem('token', data.token);
            localStorage.setItem('is_admin', data.is_admin);
            this.props.history.push('/tasks');
        })
    }

    render() {
        return (
            <Wrapper>
                <h3>Login into Mporter</h3>
                <Input fluid placeholder="Email" type="email" value={this.state.email} onChange={this.emailChange} />
                <br/>
                <Input fluid placeholder="Password" type="password" value={this.state.password} onChange={this.passwordChange} />
                <br/>
                <center>
                    <Button onClick={this.submit}>Login</Button>
                    <br/>
                    Don't have an account? <a href="/register">Register</a>
                </center>
                <div>
                </div>
            </Wrapper>
        )
    }
}

export default Login;