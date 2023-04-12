import * as types from './ActionTypes';


function ConnectSuccess(msg) {
    return {
        type: types.CONNECT_SUCCESS,
        msg
    };
}

export function ResetSignupStatus(msg) {
    return {
        type: types.RESET_SIGNUP_STATUS,
        msg
    };
}

function ConnectFail(msg) {
    return {
        type: types.CONNECT_FAIL,
        msg
    };
}

export function SignupSuccess(msg) {
    return {
        type: types.SIGNUP_SUCCESS,
        msg
    };
}

export function SignupFail(error) {
    return {
        type: types.SIGNUP_FAIL,
        error
    };
}

// export function LogOut() {
//     return {
//         type: types.LOGOUT,
//     };
// }

export function Signup(form) {
    return (dispatch) => {
        return fetch("http://web:/api/accounts/signup/",
            {
                method: "POST",
                body: form,
            })
            .then(res => res.json())

            .then(response => {
                dispatch(SignupSuccess(response));
            })
            .catch(err => {
                dispatch(SignupFail(err));
            })
    };
}