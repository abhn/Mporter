import React from 'react';

class Settings extends React.Component {

    componentDidMount() {
        if(!localStorage.getItem('token')) {
            this.props.history.push('/login');
        }
    }

    render() {
        return <div>settings</div>
    }
}

export default Settings;