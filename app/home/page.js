'use client'
import * as React from 'react';
import Card from './components/card';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
// import Scaning_Device from '/home/scaning_device.png';
export default function HomePage() {

    return (
        <>
            <Container maxWidth='xl'>
                <Box display="flex" flexWrap="wrap" gap={2}>
                    <Card title="Scanning Device" content="開啟行動裝置的Wi-Fi或藍芽搜尋附近的感應式水龍頭，可即時查看水龍頭相關資訊與調整設定，如 :感應距離、出水時間。" image="/home/scaning_device.png"></Card>
                    <Card title="Scanning Device" content="開啟行動裝置的Wi-Fi或藍芽搜尋附近的感應式水龍頭，可即時查看水龍頭相關資訊與調整設定，如 :感應距離、出水時間。" image="/home/scaning_device.png"></Card>
                    <Card title="Scanning Device" content="開啟行動裝置的Wi-Fi或藍芽搜尋附近的感應式水龍頭，可即時查看水龍頭相關資訊與調整設定，如 :感應距離、出水時間。" image="/home/scaning_device.png"></Card>
                    <Card title="Scanning Device" content="開啟行動裝置的Wi-Fi或藍芽搜尋附近的感應式水龍頭，可即時查看水龍頭相關資訊與調整設定，如 :感應距離、出水時間。" image="/home/scaning_device.png"></Card>
                </Box>
            </Container>

        </>
    );
}