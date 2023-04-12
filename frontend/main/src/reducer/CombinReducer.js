import { combineReducers } from 'redux';

import LoginReducer from './LoginReducer';
import SignupReducer from './SignupReducer';
//將所有reducer都結合起來
const Website = combineReducers({

    LoginReducer,
    SignupReducer,
});

export default Website;