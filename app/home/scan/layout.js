'use client'

import * as React from 'react';
import TiTle from '../components/title';
import Table from '../components/selecttable';
export default function HomePageLayout({ children }) {

    return (
        <section>
            <TiTle content="Connected SOC Device"></TiTle>
            <Table></Table>
            {children}
        </section>

    )
}