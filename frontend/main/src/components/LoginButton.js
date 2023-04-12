import styled from 'styled-components';
import { useSpring, animated } from 'react-spring';
import React from 'react';

export default function LoginButton(props) {

    const [springProps, setSpringProps] = useSpring(() => ({
        scale: 1,
    }));

    return (
        <Button onClick={() => props.onclick()} style={{ transform: springProps.scale.interpolate(scale => `scale(${scale})`) }}
            onMouseEnter={() => setSpringProps({ scale: 1.1 })}
            onMouseLeave={() => setSpringProps({ scale: 1 })}>登入</Button>
    );
};

const Button = styled(animated.button)`
    grid-column-start:5;
    grid-row-start:8;
    background-color: #62B4FF;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
    font-size: 24px;
    width:298px;
    height:59px;
    cursor: pointer;
`;


