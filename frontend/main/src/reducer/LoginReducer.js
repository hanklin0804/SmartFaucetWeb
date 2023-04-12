import { CONNECT_SUCCESS, LOGIN_SUCCESS, LOGIN_FAIL, RESET_LOGIN_STATUS, LOGOUT } from "../actions/ActionTypes";


// 定義初始狀態
const initState = {
    status: "",
    message: "",
    user: "",
    // jwt_token: "",
};

// 實現 reducer 函數
const LoginReducer = (state = initState, action) => {
    switch (action.type) {
        case CONNECT_SUCCESS:
            return {
                ...state,
                status: action.msg.status,
                user: action.msg.user
            };
        case LOGIN_SUCCESS:
            return {
                ...state,
                status: action.msg.status,
                user: action.msg.user
            };
        case LOGIN_FAIL:
            return {
                ...state,
            };
        case RESET_LOGIN_STATUS:
            return {
                ...state,
                status: "",
                message: "",
                user: "",
            };
        case LOGOUT:
            return {
                ...state,
                status: "",
                message: "",
                user: "",
            };
        default:
            return state;
    }
};

export default LoginReducer;