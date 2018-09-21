import React from 'react';
import { Input, Button, Table } from 'semantic-ui-react';
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
        newTask: ''
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

                {tasks.map((task, i) => 
                    <Table.Body>
                        <Table.Row key={task.at_created}>
                            <Table.Cell>{i+1}</Table.Cell>
                            <Table.Cell>{task.task}</Table.Cell>
                            <Table.Cell>{task.at_created}</Table.Cell>
                            <Table.Cell></Table.Cell>
                        </Table.Row>
                    </Table.Body>
                )}
            </Table>
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
                <InputDiv>
                    <Input placeholder="New task..." value={this.state.newTask} onChange={this.newTaskChange} action>
                        <input/>
                        <Button onClick={this.newTaskSubmit}>Add</Button>
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