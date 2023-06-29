'use client'
import AppBar from './components/appbar';
import * as React from 'react';

export default function HomePageLayout({ children }) {

    return (
        // <html lang="en">
        <section>
            {children}
            <AppBar></AppBar>
        </section>

    )
}