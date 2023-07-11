import * as React from 'react';
import LoadingButton from '@mui/lab/LoadingButton';
// import SaveIcon from '@mui/icons-material/Save';
import Stack from '@mui/material/Stack';

export default function LoadingButtons() {
    return (
        <Stack direction="row" spacing={2}>

            <LoadingButton loading loadingIndicator="select" variant="outlined">
                Fetch data
            </LoadingButton>

        </Stack>
    );
}