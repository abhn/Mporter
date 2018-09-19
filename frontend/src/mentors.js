import React from 'react';

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
        this.getMentors();
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
            <ul>
                {mentors.map(mentor => <li key={mentor.mentor_email}>{mentor.mentor_name} - {mentor.mentor_email}</li>)}
            </ul>
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
                <div>
                    <input type="text" placeholder="Mentor name" value={this.state.newMentorName} onChange={this.newMentorNameChange}/>
                    <input type="text" placeholder="Mentor email" value={this.state.newMentorEmail} onChange={this.newMentorEmailChange}/>
                    <button onClick={this.newMentorSubmit}>Add</button>
                </div>
                <div>
                    {this.formatMentors()}
                </div>
            </div>
        )
    }
}

export default Mentors;