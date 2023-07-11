'use client'
import * as React from 'react';
import Box from '@mui/material/Box';
import ArrowBackIosSharpIcon from '@mui/icons-material/ArrowBackIosSharp';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { useRouter } from 'next/navigation'
export default function Title({ content, href }) {
    const router = useRouter();
    return (
        <Box sx={{ display: "flex", alignItems: 'center', justifyContent: 'flex-start', margin: '0 auto', mt: 5 }}>
            <IconButton aria-label="Example" type="button" onClick={() => router.push(href)}>
                <ArrowBackIosSharpIcon fontSize="large"></ArrowBackIosSharpIcon>
            </IconButton>
            <Typography textAlign="center" sx={{ fontFamily: "Prompt", fontWeight: 700, fontSize: 25 }}>{content}</Typography>
        </Box >
    );
} 