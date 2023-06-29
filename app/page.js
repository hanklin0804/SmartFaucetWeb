'use client'
import * as React from 'react';
import { Container } from '@mui/material';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import LockIcon from '@mui/icons-material/Lock';
import Box from '@mui/material/Box';
import AccountCircle from '@mui/icons-material/AccountCircle';
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import IconButton from '@mui/material/IconButton';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import Button from '@mui/material/Button';

export default function LoginPage() {
    const [showPassword, setShowPassword] = React.useState(false);

    const handleClickShowPassword = () => setShowPassword((show) => !show);
    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };
    return (
        <main>
            <Container maxWidth="sm">
                <Typography
                    sx={{
                        fontSize: {
                            lg: 55,
                            md: 50,
                            sm: 40,
                            xs: 25
                        },
                        ml: {
                            lg: 6,
                            md: 6,
                            sm: 5,
                            xs: 3,
                        },
                        mt: 20,
                        fontWeight: 700,
                        fontFamily: "Prompt"
                    }}
                >WELCOME BACK!</Typography>


                <Typography
                    sx={{
                        fontSize: {
                            lg: 30,
                            md: 25,
                            sm: 20,
                            xs: 10
                        },
                        ml: {
                            lg: 7,
                            md: 7,
                            sm: 6,
                            xs: 4,
                        },
                        mt: 5,
                        fontWeight: 700,
                        fontFamily: "Prompt"
                    }}
                >LOGIN TO CONTINUE</Typography>

                <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
                    <AccountCircle sx={{ color: 'action.active', mr: 1, mb: 2, mt: 10 }} />
                    <TextField
                        id="input-account"
                        label="Account or Email"
                        variant="outlined"
                        sx={{
                            width: {
                                lg: '500px',
                                md: '450px',
                                sm: '350px',
                                xs: '250px',
                            },
                            ml: {
                                lg: 3,
                                md: 3,
                                sm: 2,
                                xs: 1,
                            },

                        }} />
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'flex-end', mt: 3 }}>
                    <LockIcon sx={{
                        color: 'action.active',
                        mr: {
                            lg: 3,
                            md: 3,
                            sm: 2,
                            xs: 1,
                        },
                        mb: 3,
                    }}></LockIcon>
                    <FormControl sx={{ m: 1, width: '25ch' }} variant="outlined">
                        <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
                        <OutlinedInput
                            id="outlined-adornment-password"
                            type={showPassword ? 'text' : 'password'}
                            endAdornment={
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label="toggle password visibility"
                                        onClick={handleClickShowPassword}
                                        onMouseDown={handleMouseDownPassword}
                                        edge="end"
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            }
                            label="Password"
                            sx={{
                                width: {
                                    lg: '496px',
                                    md: '450px',
                                    sm: '350px',
                                    xs: '250px',
                                },

                            }}
                        />
                    </FormControl>
                </Box>
                <Button
                    variant="outlined"

                    sx={{
                        color: "#000000",
                        borderRadius: 3,
                        ml: {
                            lg: 59,
                            md: 54,
                            sm: 40,
                            xs: 27,
                        },
                    }}>Login</Button>
            </Container>
        </main >
    );
}