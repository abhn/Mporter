import React from 'react';

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
            <div>
                <input type="email" value={this.state.email} onChange={this.emailChange}/> 
                <input type="password" value={this.state.password} onChange={this.passwordChange}/> 
                <button onClick={this.submit}>Login</button>
            </div>
        )
    }
}

export default Login;