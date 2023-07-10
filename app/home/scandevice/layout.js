'use client'

import * as React from 'react';
import TiTle from '../components/title';
import Table from '../components/selecttable';
export default function HomePageLayout({ children }) {

    return (
        <section>
            <TiTle content="Connected SOC Device" href="/home"></TiTle>
            <Table href="/home/savewater/50"></Table>
            {children}
        </section>

    )
}