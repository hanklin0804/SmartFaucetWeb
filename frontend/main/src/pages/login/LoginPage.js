import React, { useState, useEffect } from "react";
import styled from 'styled-components';
// import { useSpring, animated } from 'react-spring';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from 'react-router-dom';

import AccountBar from "../../components/AccountBar";
import PasswordBar from "../../components/PasswordBar";
// import VerifyCodeBar from "../../components/VerifyCodeBar";
import LoginButton from "../../components/LoginButton";
import CreateAccountButton from "../../components/CreateAccountButton";

import Company_icon from './login_assets/company_icon.PNG';
import LeftWater_icon from './login_assets/left_water.png';
import RightWater_icon from './login_assets/right_water.png';

import * as actions from "../../actions/LoginAction";



export default function LoginPage() {

    //設置account password欄位的初始值
    //輸入事件傳遞進component
    const [Account, setAccount] = useState("");
    function handleAccountChange(event) {
        // console.log(Account);
        setAccount(event.target.value);

    }

    const [Password, setPassword] = useState("");
    function handlePasswordChange(event) {
        // console.log(Password);
        setPassword(event.target.value);

    }

    const handleLogin = () => {

        if (Account === "" || Password === "") {
            alert("請輸入帳號或密碼");
            return;
        }
        let form = new FormData();
        form.append("account", Account);
        form.append("password", Password);
        dispatch(actions.Login(form));
    }
    const handleSignup = () => {
        dispatch(actions.ResetLoginStatus());
        navigate("/signup");
    }
    //redux的分派事件機制
    const dispatch = useDispatch();

    //讀取state由loginReducer所進入的state
    const state = useSelector(state => state.LoginReducer);

    //設定跳轉頁面的變數
    const navigate = useNavigate();

    useEffect(() => {
        switch (state.status) {
            case "error":
                alert("帳號或密碼輸入錯誤，請重新輸入");
                dispatch(actions.ResetLoginStatus());
                return;
            case "success":
                dispatch(actions.LoginSuccess(state));
                dispatch(actions.ResetLoginStatus());
                navigate("/home");
                return;
            default:
                return;
        }
    }
        , [state.status]);


    // if()
    return (
        <Display>
            <Template>
                <Company src={Company_icon} alt="" />
                <Text1>歡迎回來！</Text1>
                <Text2>登入以繼續</Text2>
                <AccountContainer>
                    <AccountBar onChange={handleAccountChange} placeholder="請輸入帳號" />
                </AccountContainer>
                <PasswordContainer>
                    <PasswordBar onChange={handlePasswordChange} value={Password} placeholder="請輸入密碼" />
                </PasswordContainer>
                {/* <VerifyCodeContainer>
                    <VerifyCodeBar />
                </VerifyCodeContainer> */}
                <LeftWater src={LeftWater_icon} alt="" r />
                <RightWater src={RightWater_icon} alt="" r />
                <LoginButton onclick={handleLogin} />
                <CreateAccountButton onclick={handleSignup} />
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

const AccountContainer = styled.div`
    position: relative;
    top:70%;
    left:-20%;
    grid-column-start:5;
    grid-row-start:5;
    width: 395px;
    height: 50px;
`;

const PasswordContainer = styled.div`
    position: relative;
    grid-column-start:4;
    grid-row-start:6;
    top:40%;
    left:12%;
    width: 395px;
    height: 50px;
`;

// const VerifyCodeContainer = styled.div`
//     // display: grid;
//     position: relative;
//     grid-column-start:4;
//     grid-row-start:7;
//     top:0%;
//     left:-13%;
//     width: 395px;
//     height: 50px;
// `;

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
    grid-column-start:4;
    grid-row-start:1;
`;

const Text1 = styled.div`
    // position: relative;
    grid-column-start:6;
    grid-row-start:2;
    font-family:'Inter';
    font-size: 32px;
    font-weight:700;
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
`;