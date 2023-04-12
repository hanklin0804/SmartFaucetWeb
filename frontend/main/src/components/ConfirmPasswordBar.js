import styled from 'styled-components';
import React, { useRef } from "react";

import Password_icon from './assets/password_icon.png';

export default function ConfirmPasswordBar(props) {
    const passwordRef = useRef(null);
    function handleInputChange(event) {
        props.onChange(event);
    }
    const handleFocus = () => {
        passwordRef.current.type = 'password';
    };
    return (
        <Container>
            <IconBackground>
                <Icon src={Password_icon} alt="" />
            </IconBackground>
            <TextBarInput value={props.value} type="text" placeholder={props.placeholder} onChange={handleInputChange} onFocus={handleFocus} ref={passwordRef} />
        </Container>

    );
};

const Container = styled.div`
    display: flex;
    position: relative;
    left:33%;
    width: 100%;
    height: 50px;
`;

const TextBarInput = styled.input`
    position: relative;
    height: 48px;
    border: 0px solid black;
    left:2px;
    font-size: 20px;
    ::placeholder {
        opacity:0.5;
        text-align: center;
        font-family:'Istok Web';
        font-size: 20px;
        top:30px;
      };
    
    width: 100%;
    background-color: #D8E2FA;
    border-radius: 3px;
`;

const IconBackground = styled.div`
    position: relative;
    background:#7AA5E5;
    width: 50px;
    height: 50px;
    border-radius: 3px;
`;

const Icon = styled.img`
    position: relative;
    left:-2px;
    top:-2px;
    width: 54px;
    height: 54px;
`;



// const ViewPasswordButton = styled.button`
//     position: relative;
//     background: none;
//     border: none;
//     // left:-2px;
//     // top:-2px;
//     // width: 54px;
//     // height: 54px;
// `;

// const ViewPasswordImage = styled.img`
//   width: 50px;
//   height: 50px;
// `;
