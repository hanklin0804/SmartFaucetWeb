import { CONNECT_SUCCESS, SIGNUP_SUCCESS, SIGNUP_FAIL, RESET_SIGNUP_STATUS } from "../actions/ActionTypes";


// 定義初始狀態
const initState = {
    signupstatus: "",
    message: "",
    // jwt_token: "",
};

// 實現 reducer 函數
const SignupReducer = (state = initState, action) => {
    switch (action.type) {
        // case CONNECT_SUCCESS:
        //     return {
        //         ...state,
        //         signupstatus: action.msg.status,
        //     };
        case SIGNUP_SUCCESS:
            return {
                ...state,
                signupstatus: action.msg.status,
                message: action.msg.message
            };
        case SIGNUP_FAIL:
            return {
                ...state,
            };
        case RESET_SIGNUP_STATUS:
            return {
                ...state,
                signupstatus: "",
                message: "",
            };
        default:
            return state;
    }
};

export default SignupReducer;