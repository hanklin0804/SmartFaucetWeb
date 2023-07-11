'use client'
import * as React from 'react';
import SOCTable from './components/selectSOCtable';
import TiTle from '../components/title';
export default function ScanPage() {

    return (
        <>
            <TiTle content="Connected SOC Device" href="/home"></TiTle>
            <SOCTable></SOCTable>
        </>

    );
} 