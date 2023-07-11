'use client'
import FaucetTable from './/../components/selectFaucettable';
import TiTle from '../../components/title';
import * as React from 'react';
export default function FaucetsPage() {
    return (
        <>
            <TiTle content="Connected Faucets" href="/home"></TiTle>
            <FaucetTable></FaucetTable>
        </>
    )
}