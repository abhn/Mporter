import React, { Component } from 'react';
import styled from 'styled-components';

const FooterDiv = styled.div`
    background-color: #1b1c1d;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;

    & > a {
        color: #fff;
        font-weight: 400;
    }
`;

class Footer extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <FooterDiv>
                <a href="https://mporter.co">Mporter</a>&nbsp;by&nbsp;<a href="https://github.com/abhn">Abhishek Nagekar</a>
            </FooterDiv>
        )
    }
}

export default Footer;