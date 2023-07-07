import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

export default function ActionAreaCard({ title, content, image, img_mt }) {
    // const [img_mt1, setimg_mt1] = React.useState(-1);
    const total_mt = -1 + img_mt;

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
                lg: 6,
                md: 20,
                sm: 5,
                xs: 8,
            }
        }}>
            <CardActionArea sx={{
                width:
                {
                    lg: 250,
                    md: 300,
                    sm: 300,
                    xs: 200,
                },
                height:
                {
                    lg: 450,
                    md: 400,
                    sm: 300,
                    xs: 300,
                }
            }}>
                <CardMedia
                    component="img"
                    image={image}
                    sx={{
                        width:
                        {
                            lg: 200,
                            md: 200,
                            sm: 150,
                            xs: 100,
                        },
                        height:
                        {
                            lg: 200,
                            md: 200,
                            sm: 150,
                            xs: 100,
                        },
                        mt: total_mt,
                        ml:
                        {
                            lg: 3,
                            md: 5,
                            sm: 9,
                            xs: 6,
                        },
                        mb: 8
                    }}
                />
                <CardContent>
                    <Typography gutterBottom component="div" align='center'
                        sx={{
                            mt: -8,
                            fontSize:
                            {
                                lg: 20,
                                md: 20,
                                sm: 15,
                                xs: 15,
                            },
                            fontWeight: 700,
                            fontFamily: 'Prompt'
                        }}>
                        {title}
                    </Typography>
                    <div
                        style={{
                            width: '100%',
                            height: '2px',
                            background: 'black',
                            margin: '8px 0',
                        }}
                    ></div>
                    <Typography variant="body2" color="text.secondary"
                        sx={{
                            fontSize:
                            {
                                lg: 15,
                                md: 15,
                                sm: 10,
                                xs: 10,
                            },
                            fontWeight: 700,
                            fontFamily: 'Prompt'
                        }}>
                        {content}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}