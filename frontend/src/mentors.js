import React from 'react';
import { Input, Button, Table } from 'semantic-ui-react';
import styled from 'styled-components';


const InputDiv = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
`;

class Mentors extends React.Component {

    state = {
        mentors: [],
        newMentorName: '',
        newMentorEmail: ''
    }

    componentDidMount() {
        if(!localStorage.getItem('token')) {
            this.props.history.push('/login');
        }
        else {
            this.getMentors();
        }
    }

    getMentors = () => {
        fetch('/api/mentor', {
            headers: {
                "Authorization": localStorage.getItem('token')
            }
        })
        .then(res => res.json())
        .then(data => this.setState({ mentors: data.mentors }));
    }

    formatMentors = () => {
        let { mentors } = this.state;
        return (

            <Table celled striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>Serial</Table.HeaderCell>                        
                        <Table.HeaderCell>Mentor Name</Table.HeaderCell>
                        <Table.HeaderCell>Mentor Email</Table.HeaderCell>
                        <Table.HeaderCell>Actions</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>

                {mentors.map((mentor, i) => 
                    <Table.Body>
                        <Table.Row key={mentor.mentor_email}>
                            <Table.Cell>{i+1}</Table.Cell>
                            <Table.Cell>{mentor.mentor_name}</Table.Cell>
                            <Table.Cell>{mentor.mentor_email}</Table.Cell>
                            <Table.Cell></Table.Cell>
                        </Table.Row>
                    </Table.Body>
                )}
            </Table>
        )
    }

    newMentorNameChange = (e) => {
        this.setState({
            newMentorName: e.target.value
        })
    }

    newMentorEmailChange = (e) => {
        this.setState({
            newMentorEmail: e.target.value
        })
    }

    newMentorSubmit = () => {
        fetch('/api/mentor', {
            method: 'post',
            body: JSON.stringify({
                mentor_name: this.state.newMentorName,
                mentor_email: this.state.newMentorEmail
            }),
            headers: {
                "Content-Type": "application/json",
                "Authorization": localStorage.getItem('token')
            }
        })
        .then(res => {
            this.setState({newMentorEmail: '', newMentorName: ''})
            this.getMentors();
        })
    }

    render() {
        return (
            <div>
                <InputDiv>
                    <Input placeholder="Mentor name" value={this.state.newMentorName} onChange={this.newMentorNameChange} />
                    <Input placeholder="Mentor email" value={this.state.newMentorEmail} onChange={this.newMentorEmailChange} action>
                        <input/>
                        <Button onClick={this.newMentorSubmit}>Add</Button>
                    </Input>
                </InputDiv>
                <div>
                    {this.formatMentors()}
                </div>
            </div>
        )
    }
}

export default Mentors;