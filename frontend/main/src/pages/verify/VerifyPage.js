import styled from 'styled-components';
import AccountBar from "../../components/AccountBar";
import PasswordBar from "../../components/PasswordBar";
import VerifyCodeBar from "../../components/VerifyCodeBar";
import Company_icon from './login_assets/company_icon.PNG';
import LeftWater_icon from './login_assets/left_water.png';
import RightWater_icon from './login_assets/right_water.png';



export default function LoginPage() {
    return (
        <Template>
            <Company src={Company_icon} alt="" />
            <Text1>歡迎回來！</Text1>
            <Text2>登入以繼續</Text2>
            <AccountContainer>
                <AccountBar />
            </AccountContainer>
            <PasswordContainer>
                <PasswordBar />
            </PasswordContainer>
            <VerifyCodeContainer>
                <VerifyCodeBar />
            </VerifyCodeContainer>
            <LeftWater src={LeftWater_icon} alt="" r />
            <RightWater src={RightWater_icon} alt="" r />
        </Template >
    );

};

const LeftWater = styled.img`
    // display: grid;
    position: relative;
    // grid-template-columns:10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    // grid-template-rows: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    top:20%;
    left:0%;
    grid-column-start:1;
    grid-row-start:3;
    width: 750px;
    height: 360px;
`;

const RightWater = styled.img`
    // display: grid;
    position: relative;
    // grid-template-columns:10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    // grid-template-rows: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    top:20%;
    left:0%;
    grid-column-start:6;
    grid-row-start:6;
    width: 750px;
    height: 635px;
`;

const AccountContainer = styled.div`
    // display: grid;
    position: relative;
    // grid-template-columns:10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    // grid-template-rows: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    top:70%;
    left:-20%;
    grid-column-start:5;
    grid-row-start:5;
    width: 395px;
    height: 50px;
`;

const PasswordContainer = styled.div`
    // display: grid;
    position: relative;
    grid-column-start:4;
    grid-row-start:6;
    top:20%;
    left:-13%;
    width: 395px;
    height: 50px;
`;

const VerifyCodeContainer = styled.div`
    // display: grid;
    position: relative;
    grid-column-start:4;
    grid-row-start:7;
    top:0%;
    left:-13%;
    width: 395px;
    height: 50px;
`;

const Template = styled.div`
    display: grid;
    grid-template-columns:10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    grid-template-rows: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    // background:#7AA5E5;
    position: relative;
    // top:150px;
    left:0%;
    width: 1920px;
    height: 1280px;
`;

const Company = styled.img`
    // position: relative;
    grid-column-start:4;
    grid-row-start:1;
    // left:23%;
    // top:150px;
    // width: 592px;
    // height: 592px;
`;

const Text1 = styled.div`
    // position: relative;
    grid-column-start:6;
    grid-row-start:2;
    font-family:'Inter';
    font-size: 32px;
    font-weight:700;
    // left:23%;
    // top:150px;
    // width: 592px;
    // height: 592px;
`;

const Text2 = styled.div`
    position: relative;
    grid-column-start:6;
    grid-row-start:3;
    font-family:'Inter';
    font-size: 20px;
    font-weight:bold;
    left:10%;
    top:-30%;
    // width: 592px;
    // height: 592px;
`;