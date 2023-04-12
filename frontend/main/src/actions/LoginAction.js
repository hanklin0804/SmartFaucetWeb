import * as types from './ActionTypes';


function ConnectSuccess(msg) {
    return {
        type: types.CONNECT_SUCCESS,
        msg
    };
}

export function ResetLoginStatus() {
    return {
        type: types.RESET_LOGIN_STATUS,
    };
}

function ConnectFail(msg) {
    return {
        type: types.CONNECT_FAIL,
        msg
    };
}

export function LoginSuccess(msg) {
    return {
        type: types.LOGIN_SUCCESS,
        msg
    };
}

export function LoginFail(error) {
    return {
        type: types.LOGIN_FAIL,
        error
    };
}

export function LogOut() {
    return {
        type: types.LOGOUT,
    };
}

export function Login(form) {
    return (dispatch) => {
        return fetch("http://web:8787/api/accounts/login/",
            {
                method: "POST",
                body: form,
            })
            .then(res => res.json())

            .then(response => {
                dispatch(ConnectSuccess(response));
            })
            .catch(err => {
                dispatch(ConnectFail(err));
            })
    };
}