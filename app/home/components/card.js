import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import Image from 'next/image'
export default function ActionAreaCard({ title, content, image }) {
    return (
        <Card sx={{ maxWidth: 345 }}>
            <CardActionArea>

                <Image
                    src={image}
                    width={250}
                    height={250}
                    alt="Picture of the author"
                />
                {/* <>{image}</> */}
                <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                        {title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {content}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}