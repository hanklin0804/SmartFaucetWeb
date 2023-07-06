import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import Image from 'next/image'
export default function ActionAreaCard({ title, content, image }) {
    return (
        <Card sx={{
            maxWidth: 345,
            mt:
            {
                lg: 15,
                md: 14,
                sm: 10,
                xs: 5,
            },
            ml:
            {
                lg: 3,
                md: 5,
                sm: 5,
                xs: 8,
            }
        }}>
            <CardActionArea sx={{
                width:
                {
                    lg: 300,
                    md: 200,
                    sm: 175,
                    xs: 200,
                }
            }}>
                <CardMedia
                    component="img"
                    height="140"
                    image={image}
                    sx={{
                        width:
                        {
                            lg: 300,
                            md: 200,
                            sm: 150,
                            xs: 200,
                        },
                        height:
                        {
                            lg: 300,
                            md: 200,
                            sm: 150,
                            xs: 200,
                        },
                    }}
                />
                <CardContent>
                    <Typography gutterBottom component="div"
                        sx={{
                            mt: -4,
                            fontSize:
                            {
                                lg: 30,
                                md: 20,
                                sm: 15,
                                xs: 20,
                            },
                            fontWeight: 700

                        }}>
                        {title}
                    </Typography>
                    <div
                        style={{
                            width: '100%',
                            height: '1px',
                            background: 'black',
                            margin: '8px 0',
                        }}
                    ></div>
                    <Typography variant="body2" color="text.secondary">
                        {content}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}