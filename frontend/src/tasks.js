import React from 'react';
import { Input, Button, Table, Icon, Modal } from 'semantic-ui-react';
import styled from 'styled-components';


const InputDiv = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
`;


class Tasks extends React.Component {
    state = {
        tasks: [],
        newTask: '',
        deleteLoading: false,
        addLoading: false
    }

    componentDidMount() {
        if(!localStorage.getItem('token')) {
            this.props.history.push('/login');
        }
        else {
            this.getTasks();
        }
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

    deleteTask = task => {
        this.setState({ deleteLoading: true })
        fetch('/api/task', {
            method: 'delete',
            body: JSON.stringify({
                // work here
                task_id: task.id
            }),
            headers: {
                "Content-Type": "application/json",
                "Authorization": localStorage.getItem('token')
            }
        })
        .then(res => res.json())
        .then(data => {
            this.setState({ deleteLoading: false })
            this.getTasks();
        })
    }

    formatTasks = () => {
        let { tasks } = this.state;
        return (
            <Table celled striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Serial</Table.HeaderCell>                        
                        <Table.HeaderCell>Task</Table.HeaderCell>
                        <Table.HeaderCell>Created Date</Table.HeaderCell>
                        <Table.HeaderCell>Actions</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>

                <Table.Body>
                    {tasks.map((task, i) => 
                        <Table.Row key={task.at_created}>
                            <Table.Cell>{i+1}</Table.Cell>
                            <Table.Cell>{task.task}</Table.Cell>
                            <Table.Cell>{task.at_created}</Table.Cell>
                            <Table.Cell>
                                <Button icon negative onClick={() => this.deleteTask(task)} loading={this.state.deleteLoading}>
                                    <Icon name='delete' />
                                </Button>
                            </Table.Cell>
                        </Table.Row>
                    )}
                </Table.Body>
            </Table>
        )
    }

    newTaskChange = (e) => {
        this.setState({
            newTask: e.target.value
        })
    }

    newTaskSubmit = () => {
        this.setState({ addLoading: true });
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
            this.setState({ newTask: '', addLoading: false })
            this.getTasks();
        })
    }

    render() {
        return (
            <div>
                <InputDiv>
                    <Input placeholder="New task..." value={this.state.newTask} onChange={this.newTaskChange} action>
                        <input/>
                        <Button onClick={this.newTaskSubmit} loading={this.state.addLoading}>Add</Button>
                    </Input>
                </InputDiv>
                <div>
                    {this.formatTasks()}
                </div>
            </div>
        )
    }
}

export default Tasks;