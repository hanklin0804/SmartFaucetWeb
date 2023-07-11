'use client'
import * as React from 'react';
import TiTle from '../components/title';
export default function HomePageLayout({ children }) {

    return (
        <section>
            <TiTle content="Water Saving DashBoard" href="/home"></TiTle>
            {children}
        </section>

    )
}