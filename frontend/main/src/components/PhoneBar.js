import styled from 'styled-components';
import name_icon from './assets/phone_icon.png';

export default function PhoneBar(props) {

    function handleInputChange(event) {
        props.onChange(event);
    }
    return (
        <Container>
            <IconBackground>
                <Icon src={name_icon} alt="" />
            </IconBackground>
            <TextBarInput type="text" placeholder={props.placeholder} onChange={handleInputChange}></TextBarInput>
        </Container>
    );
};

const Container = styled.div`
    display: flex;
    position: relative;
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
    width: 50px;
    height: 50px;
`;

