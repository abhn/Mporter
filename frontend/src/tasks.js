import React from 'react';

class Tasks extends React.Component {
    state = {
        tasks: [],
        newTask: ''
    }

    componentDidMount() {
        if(!localStorage.getItem('token')) {
            this.props.history.push('/login');
        }
        this.getTasks();
    }

    getTasks = () => {
        fetch('/api/task', {
            headers: {
                "Authorization": localStorage.getItem('token')
            }
        })
        .then(res => res.json())
        .then(data => this.setState({ tasks: data.tasks }));
    }

    formatTasks = () => {
        let { tasks } = this.state;
        return (
            <ul>
                {tasks.map(task => <li key={task.at_created}>{task.task} - {task.at_created}</li>)}
            </ul>
        )
    }

    newTaskChange = (e) => {
        this.setState({
            newTask: e.target.value
        })
    }

    newTaskSubmit = () => {
        fetch('/api/task', {
            method: 'post',
            body: JSON.stringify({
                task: this.state.newTask
            }),
            headers: {
                "Content-Type": "application/json",
                "Authorization": localStorage.getItem('token')
            }
        })
        .then(res => {
            this.setState({newTask: ''})
            this.getTasks();
        })
    }

    render() {
        return (
            <div>
                <div>
                    <input type="text" value={this.state.newTask} onChange={this.newTaskChange}/>
                    <button onClick={this.newTaskSubmit}>Add</button>
                </div>
                <div>
                    {this.formatTasks()}
                </div>
            </div>
        )
    }
}

export default Tasks;