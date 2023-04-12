import styled from 'styled-components';
import Verify_icon from './assets/verification_code.png';

export default function VerifyCodeBar() {

    return (
        <Template>
            <Container>
                <Icon_background>
                    <Icon src={Verify_icon} alt="" />
                </Icon_background>
                <TextBarInput type="text" placeholder="請先輸入驗證碼"></TextBarInput>
            </Container>
        </Template>
    );
};


const Template = styled.div`
    position: relative;
    grid-column-start:3;
    grid-row-start:7;
    top:-10%;
    left:12%;
    width: 395px;
    height: 50px;
`;
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

const Icon_background = styled.div`
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

