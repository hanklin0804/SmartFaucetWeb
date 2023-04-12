import styled from 'styled-components';
import { useSpring, animated } from 'react-spring';

export default function VerifyEmailButton(props) {
    const [springProps, setSpringProps] = useSpring(() => ({
        scale: 1,
    }));
    return (
        <Button style={{ transform: springProps.scale.interpolate(scale => `scale(${scale})`) }}
            onMouseEnter={() => setSpringProps({ scale: 1.1 })}
            onMouseLeave={() => setSpringProps({ scale: 1 })} onClick={() => props.onclick()} > 完成註冊</Button >
    );
};

const Button = styled(animated.button)`
    grid-column-start:6;
    grid-row-start:8;
    background-color: #F09DB6;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
    font-size: 24px;
    width:298px;
    height:59px;
    cursor: pointer;
`;


