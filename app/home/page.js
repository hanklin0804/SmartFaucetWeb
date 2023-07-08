'use client'
import * as React from 'react';
import Card from './components/card';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

export default function HomePage() {

    return (
        <>
            <Container maxWidth='xl'>
                <Box display="flex" flexWrap="wrap" gap={2}>
                    <Card title="Scanning Device" content="開啟行動裝置的Wi-Fi或藍芽搜尋附近的感應式水龍頭，可即時查看水龍頭相關資訊與調整設定，如 :感應距離、出水時間。" image="/home/scaning_device.png" href="/home/scan"></Card>
                    <Card title="Water Saving" content="您可透過此量表即時查看水龍頭每天、每周、每月甚至是每年用水量之情況。" image="/home/saving_water.png" img_mt={-2} href="/save"></Card>
                    <Card title="Maintenance" content="開啟行動裝置的Wi-Fi或藍芽搜尋附近的感應式水龍頭，可即時查看水龍頭相關資訊與調整設定，如 :感應距離、出水時間。" image="/home/setting.png" href="/maintain"></Card>
                    <Card title="Event Statistics" content="您可以透過事件統計查看所有裝置過去的維修、設定紀錄。" image="/home/event_statistics.png" img_mt={-5} href="/event"></Card>
                </Box>
            </Container>

        </>
    );
}