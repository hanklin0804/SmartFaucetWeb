'use client'
import * as React from 'react';
import PropTypes from 'prop-types';
import ArrowBackIosSharpIcon from '@mui/icons-material/ArrowBackIosSharp';
import { faEllipsisV } from '@fortawesome/free-solid-svg-icons/faEllipsisV';
import IconButton from '@mui/material/IconButton';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Button from '@mui/material/Button';
// import Card from '../components/card';
// import Box from '@mui/material/Box';
// import Container from '@mui/material/Container';

const FontAwesomeSvgIcon = React.forwardRef((props, ref) => {
    const { icon } = props;

    const {
        icon: [width, height, , , svgPathData],
    } = icon;

    return (
        <SvgIcon ref={ref} viewBox={`0 0 ${width} ${height}`}>
            {typeof svgPathData === 'string' ? (
                <path d={svgPathData} />
            ) : (
                /**
                 * A multi-path Font Awesome icon seems to imply a duotune icon. The 0th path seems to
                 * be the faded element (referred to as the "secondary" path in the Font Awesome docs)
                 * of a duotone icon. 40% is the default opacity.
                 *
                 * @see https://fontawesome.com/how-to-use/on-the-web/styling/duotone-icons#changing-opacity
                 */
                svgPathData.map((d, i) => (
                    <path style={{ opacity: i === 0 ? 0.4 : 1 }} d={d} />
                ))
            )}
        </SvgIcon>
    );
});

FontAwesomeSvgIcon.propTypes = {
    icon: PropTypes.any.isRequired,
};
export default function HomePage() {

    return (
        <>
            <IconButton aria-label="Example">
                <ArrowBackIosSharpIcon />
            </IconButton>
        </>
    );
} 