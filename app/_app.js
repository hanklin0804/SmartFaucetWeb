import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import { Inter } from 'next/font/google';

const inter = Inter({
    subsets: ['latin'],
    // weight: ['600', '500'],
})
function MyApp({ Component, pageProps }) {
    return (
        <main className={inter.className}>
            <Component {...pageProps} />
        </main>

    );
}

export default MyApp;
