'use client'
import * as React from 'react';
import { Container } from '@mui/material';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import PersonOutlineIcon from '@mui/icons-material/PersonOutline';
// import theme from './theme';
export default function LoginPage() {
    return (
        <main>
            <Container maxWidth="sm">
                <Typography sx={{ fontSize: 40, my: 20 }}>WELCOME BACK</Typography>
                <br></br>
                <br></br>
                <br></br>
                <br></br>
                <PersonOutlineIcon sx={{ fontSize: 40, my: 1 }}></PersonOutlineIcon>
                <TextField id="outlined-basic" label="account" variant="outlined" />
                <TextField id="outlined-basic" label="password" variant="outlined" />

            </Container>
        </main>
    );
}