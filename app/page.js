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
import ButtonGroup from '@mui/material/ButtonGroup';

export default function LoginPage() {
    const [showPassword, setShowPassword] = React.useState(false);

    const handleClickShowPassword = () => setShowPassword((show) => !show);
    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };
    return (
        <main>
            <Container
                maxWidth="sm" sx={{ justifyContent: 'center', alignItems: 'center' }}>
                <Typography
                    sx={{
                        fontSize: {
                            lg: 55,
                            md: 50,
                            sm: 45,
                            xs: 30
                        },
                        ml: {
                            lg: 6,
                            md: 6,
                            sm: 10,
                            xs: 5,
                        },
                        mt: {
                            lg: 6,
                            md: 6,
                            sm: 5,
                            xs: 14,
                        },
                        fontWeight: 700,
                        fontFamily: "Prompt"
                    }}
                >WELCOME BACK!
                </Typography>
                <Typography
                    sx={{
                        fontSize: {
                            lg: 30,
                            md: 25,
                            sm: 25,
                            xs: 15
                        },
                        ml: {
                            lg: 7,
                            md: 7,
                            sm: 11,
                            xs: 5,
                        },
                        mt: 5,
                        fontWeight: 700,
                        fontFamily: "Prompt"
                    }}
                >LOGIN TO CONTINUE
                </Typography>
                <Box
                    sx={{ display: 'flex', alignItems: 'flex-end' }}>
                    <AccountCircle sx={{
                        color: 'action.active', mb: 2,
                        mt: {
                            lg: 10,
                            md: 10,
                            sm: 10,
                            xs: 4,
                        },
                        ml: {
                            lg: 3,
                            md: 3,
                            sm: 7,
                            xs: 5
                        },
                        mr: {
                            lg: -2,
                            md: -2,
                            sm: 1,
                            xs: -1,
                        },
                    }} />
                    <TextField
                        id="input-account"
                        label="Account or Email"
                        variant="outlined"
                        sx={{
                            width: {
                                lg: '500px',
                                md: '450px',
                                sm: '350px',
                                xs: '225px',
                            },
                            ml: {
                                lg: 3,
                                md: 3,
                                sm: 0,
                                xs: 1,
                            },
                            fontFamily: "Prompt"
                        }} />
                </Box>
                <Box
                    sx={{
                        display: 'flex', alignItems: 'flex-end', mt: 3,
                        ml: {
                            lg: 3,
                            md: 3,
                            sm: 7,
                            xs: 5,
                        },
                    }}>
                    <LockIcon sx={{
                        color: 'action.active',
                        mb: 3,
                        mr: {
                            lg: 0,
                            md: 0,
                            sm: 0,
                            xs: -1,
                        },
                    }}></LockIcon>
                    <FormControl sx={{ m: 1, width: '25ch' }} variant="outlined">
                        <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
                        <OutlinedInput
                            fontFamily="Prompt"
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
                                    xs: '225px',
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
                        mt: 1,
                        ml: {
                            lg: 59,
                            md: 54,
                            sm: 45,
                            xs: 27,
                        },
                        fontFamily: "Prompt"
                    }}>Login
                </Button>
                <br />
                <ButtonGroup
                    variant="text" aria-label="text button group" >
                    <Button size='small' color="inherit" sx={{ fontFamily: "Prompt" }}>Ch</Button>
                    <Button size='small' color="inherit" sx={{ fontFamily: "Prompt" }}>En</Button>
                </ButtonGroup>
                <Button
                    sx={{
                        color: "#000000",
                        borderRadius: 3,
                        ml: {
                            lg: 34,
                            md: 30,
                            sm: 22,
                            xs: 3,
                        },
                        mt: 0,
                        width: '200px',
                        fontSize: {
                            lg: 10,
                            md: 10,
                            sm: 1,
                            xs: 1
                        },
                        size: 'small',
                        fontFamily: "Prompt"
                    }}>Forget your password?
                </Button>
            </Container>
        </main >
    );
}