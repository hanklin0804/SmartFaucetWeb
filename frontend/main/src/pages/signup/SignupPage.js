import React, { useState, useEffect } from "react";
import styled from 'styled-components';
// import { useSpring, animated } from 'react-spring';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, unstable_HistoryRouter } from 'react-router-dom';
import NameBar from "../../components/NameBar";
import EmailBar from "../../components/EmailBar";
import PhoneBar from "../../components/PhoneBar";
import AccountBar from "../../components/AccountBar";
import PasswordBar from "../../components/PasswordBar";
import ConfirmPasswordBar from "../../components/ConfirmPasswordBar";

import VerifyEmailButton from "../../components/VerifyEmailButton";
// import VerifyCodeBar from "../../components/VerifyCodeBar";
// import LoginButton from "../../components/LoginButton";
// import CreateAccountButton from "../../components/CreateAccountButton";

import Company_icon from './login_assets/company_icon.PNG';
import LeftWater_icon from './login_assets/left_water.png';
import RightWater_icon from './login_assets/right_water.png';

import * as actions from "../../actions/SignupAction";



export default function SignupPage() {

    //設置account password欄位的初始值
    //輸入事件傳遞進component
    const [Name, setName] = useState("");
    function handleNameChange(event) {
        setName(event.target.value);
    }

    const [Account, setAccount] = useState("");
    function handleAccountChange(event) {
        setAccount(event.target.value);
    }

    const [Password, setPassword] = useState("");

    function handlePasswordChange(event) {
        setPassword(event.target.value);
    }

    const [ConfirmPassword, setConfirmPassword] = useState("");

    const handleConfirmPasswordChange = (event) => {
        setConfirmPassword(event.target.value);
    }

    const [Email, setEamil] = useState("");

    const handleEmailChange = (event) => {
        setEamil(event.target.value);
    }

    const [Phone, setPhone] = useState("");

    const handlePhoneChange = (event) => {
        setPhone(event.target.value);
    }
    //回傳密碼跟確認密碼的布林值
    const passwordsMatch = () => {
        return Password === ConfirmPassword;
    }

    const handleSignupClick = () => {

        if (Name === '' || Password === '' || ConfirmPassword === '' || Email === '' || Phone === '') {
            alert("請勿留空欄位");
        }
        else {
            if (!passwordsMatch()) {

                alert("帳號密碼輸入不一致");
                return;

            }
            let form = new FormData();
            form.append("account", Account);
            form.append("password", Password);
            form.append("email", Email);
            form.append("name", Name);
            form.append("phone", Phone);

            dispatch(actions.Signup(form));
        }
    }

    //redux的分派事件機制
    //設定跳轉頁面的變數
    const dispatch = useDispatch();
    const state = useSelector(state => state.SignupReducer);
    const navigate = useNavigate();

    useEffect(() => {
        switch (state.signupstatus) {
            case "error":
                alert("註冊失敗！");
                dispatch(actions.ResetSignupStatus(state));
                return;
            case "success":

                dispatch(actions.SignupSuccess(state));
                console.log(state);
                dispatch(actions.ResetSignupStatus(state));

                setTimeout(() => {
                    navigate("/login");
                }, 1000);
                return;
            default:
                dispatch(actions.ResetSignupStatus(state));
                return;
        }
    }
        , [state.signupstatus]);


    return (
        <Display>
            <Template>
                <LeftWater src={LeftWater_icon} alt="" r />
                <RightWater src={RightWater_icon} alt="" r />
                <Company src={Company_icon} alt="" />
                <Text1>開始註冊</Text1>
                <Text2>水電工程師註冊新帳號</Text2>
                <NameText>姓名:</NameText>
                <AccountText>帳號:</AccountText>
                <PasswordText>密碼:</PasswordText>
                <EmailText>電子郵件:</EmailText>
                <PhoneText>手機號碼:</PhoneText>
                <NameContainer>
                    <NameBar value={Name} onChange={handleNameChange} placeholder="請輸入姓名" />
                </NameContainer>
                <AccountContainer>
                    <AccountBar value={Account} onChange={handleAccountChange} placeholder="請輸入帳號" />
                </AccountContainer>
                <PasswordContainer>
                    <PasswordBar onChange={handlePasswordChange} value={Password} placeholder="請輸入密碼" />
                </PasswordContainer>
                <ConfirmPasswordContainer>
                    <ConfirmPasswordBar onChange={handleConfirmPasswordChange} value={ConfirmPassword} placeholder="請再次輸入密碼" />
                </ConfirmPasswordContainer>
                <EmailContainer>
                    <EmailBar onChange={handleEmailChange} value={Email} placeholder="請輸入電子郵件" />
                </EmailContainer>
                <PhoneContainer>
                    <PhoneBar onChange={handlePhoneChange} value={Phone} placeholder="請輸入手機號碼" />
                </PhoneContainer>
                <VerifyEmailButton onclick={handleSignupClick} />
            </Template >
        </Display>
    );

};

const LeftWater = styled.img`
    position: relative;
    top:20%;
    left:0%;
    justify-content: center;
    align-items: center;
    grid-column-start:1;
    grid-row-start:3;
    width: 750px;
    height: 360px;
`;

const RightWater = styled.img`
    position: relative;
    top:20%;
    left:0%;
    grid-column-start:7;
    grid-row-start:6;
    width: 750px;
    height: 635px;
`;

const NameContainer = styled.div`
    position: relative;
    top:107%;
    left:-20%;
    grid-column-start:6;
    grid-row-start:2;
    width: 395px;
    height: 50px;
`;


const AccountContainer = styled.div`
    position: relative;
    top:70%;
    left:-20%;
    grid-column-start:6;
    grid-row-start:3;
    width: 395px;
    height: 50px;
`;

const PasswordContainer = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:4;
    top:30%;
    left:12.5%;
    width: 395px;
    height: 50px;
`;

const ConfirmPasswordContainer = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:5;
    top:-5%;
    left:12.5%;
    width: 395px;
    height: 50px;
`;

const EmailContainer = styled.div`
    position: relative;
    grid-column-start:6;
    grid-row-start:6;
    top:-35%;
    left:-21%;
    width: 395px;
    height: 50px;
`;

const PhoneContainer = styled.div`
    position: relative;
    grid-column-start:6;
    grid-row-start:7;
    top:-70%;
    left:-21%;
    width: 395px;
    height: 50px;
`;

const Template = styled.div`
    display: grid;
    grid-template-columns:10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    grid-template-rows: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
    position: relative;
    left:0%;
    width: 1920px;
    height: 1280px;
`;

const Display = styled.div`
    justify-content: center;
    align-items: center;
    width: 1920px;
    height: 1280px;
    height: 80vh;
    margin: 0;
`;

const Company = styled.img`
    position: relative;
    grid-column-start:6;
    grid-row-start:1;
    left:20%;
    width: 110px;
    height: 145px;
`;

const Text1 = styled.div`
    position: relative;
    grid-column-start:6;
    grid-row-start:2;
    font-family:'Inter';
    font-size: 32px;
    font-weight:700;
    left:20%;
    top:15%;
`;

const Text2 = styled.div`
    position: relative;
    grid-column-start:6;
    grid-row-start:2;
    font-family:'Inter';
    font-size: 18px;
    font-weight:bold;
    left:5%;
    top:50%;
`;

const NameText = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:3;
    font-family:'Inter';
    font-size: 20px;
    font-weight:700;
    left:20%;
    top:20%;
`;

const AccountText = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:4;
    font-family:'Inter';
    font-size: 20px;
    font-weight:700;
    left:20%;
    top:-20%;
`;

const PasswordText = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:5;
    font-family:'Inter';
    font-size: 20px;
    font-weight:700;
    left:20%;
    top:-60%;
`;

const EmailText = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:6;
    font-family:'Inter';
    font-size: 20px;
    font-weight:700;
    left:20%;
    top:-25%;
`;

const PhoneText = styled.div`
    position: relative;
    grid-column-start:5;
    grid-row-start:6;
    font-family:'Inter';
    font-size: 20px;
    font-weight:700;
    left:20%;
    top:40%;
`;