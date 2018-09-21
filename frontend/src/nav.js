import React, { Component } from 'react';
import { Menu, Segment, Icon } from 'semantic-ui-react';

class Nav extends Component {
    constructor() {
        super();
        this.state = {
            activeItem: 'tasks'
        }
    }

    handleItemClick = (e, { name }) => { 
        this.setState({ activeItem: name })
        window.location.href = '#/' + name;
    }

    logout = () => {
        localStorage.clear();
        window.location.href = '/';
    }

    goToAdmin = () => {
        window.location.href = '/admin';
    }

    render() {
        const { activeItem } = this.state;

        return (
            <nav>
                <Menu inverted>
                    <Menu.Item name='tasks' 
                        active={activeItem === 'tasks'} 
                        onClick={this.handleItemClick} />
                    <Menu.Item
                        name='mentors'
                        active={activeItem === 'mentors'}
                        onClick={this.handleItemClick} />

                    <Menu.Menu position="right">
                        
                        {localStorage.getItem('is_admin') ? 
                            <Menu.Item
                                name='admin'
                                active={activeItem === 'admin'}
                                onClick={this.goToAdmin} />
                        : ''}

                        <Menu.Item
                            name='settings'
                            active={activeItem === 'settings'}
                            onClick={this.handleItemClick}>
                            <Icon name="setting"/>    
                        </Menu.Item>

                        <Menu.Item
                            name='logout'
                            active={activeItem === 'logout'}
                            onClick={this.logout}>
                            <Icon name="sign-out"/>    
                        </Menu.Item>

                    </Menu.Menu>
                </Menu>
            </nav>    
        )
    }
}

export default Nav;