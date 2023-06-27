import { Barlow, Cormorant } from "next/font/google";
import { createTheme } from '@mui/material/styles';

export const barlow = Barlow({
    weight: ["200", "400", "500", "600", "700"],
    display: "swap",
    fallback: ["Helvetica", "Arial", "sans-serif"],
    subsets: ['latin']
});

export const cormorant = Cormorant({
    weight: ["300", "400", "500", "600", "700"],
    display: "swap",
    fallback: ["Times New Roman", "Times", "serif"],
    subsets: ['latin']
});

const theme = createTheme({
    typography: {
        fontFamily: barlow.style.fontFamily,
        body1: {
            fontFamily: barlow.style.fontFamily,
        },
        primary: {
            fontFamily: barlow.style.fontFamily,
        },
        secondary: {
            fontFamily: cormorant.style.fontFamily,
        },
    },
});