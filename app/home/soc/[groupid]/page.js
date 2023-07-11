'use client'
import * as React from 'react';
import FaucetTable from './/../components/selectFaucettable';
import TiTle from '../../components/title';
import Moveonbutton from '../components/moveonbutton';
export default function FaucetsPage() {
    return (
        <>
            <TiTle content="Connected Faucets" href="/home"></TiTle>
            <FaucetTable></FaucetTable>
            {/* <Moveonbutton></Moveonbutton> */}
        </>
    )
}