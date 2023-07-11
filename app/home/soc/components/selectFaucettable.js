import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Avatar } from '@mui/material';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
function ImageCell(params) {
    const { value } = params;

    return (
        <Avatar src={value} />
    );
}
const columns = [
    {
        field: 'avatar',
        headerName: 'Faucet_Image',
        width: 120,
        headerAlign: 'center',
        align: 'center',
        flex: 0.2,
        renderCell: (params) => <ImageCell value={params.value} />,
    },
    { field: 'model', headerName: 'Product number', width: 120, headerAlign: 'center', align: 'center', flex: 0.2, },
    { field: 'id', headerName: 'Faucet ID', width: 50, headerAlign: 'center', align: 'center', flex: 0.2, },

    {
        field: 'totalWaterConsumption', headerName: 'Total Usage Water(L)', type: 'number', width: 170, headerAlign: 'center',
        align: 'center', flex: 0.2,
    },
    {
        field: 'infraredSensorFstatus',
        headerName: 'Infrared Sensor Status',
        width: 180,
        headerAlign: 'center',
        align: 'center', flex: 0.2,
    },

];

const rows = [
    { avatar: "/home/scaning_device.png", id: 'lAelv', totalWaterConsumption: 30, model: '145015', infraredSensorFstatus: 'error' },
    { avatar: "/home/scaning_device.png", id: 'lBJIe', totalWaterConsumption: 32, model: '145015', infraredSensorFstatus: 'error' },
];

export default function DataTable() {
    const [selectedRow, setSelectedRow] = React.useState(null);
    const [rowSelectionModel, setRowSelectionModel] = React.useState([]);

    const handleRowSelection = (params) => {
        const selectedRowId = params.selectionModel[0];
        setSelectedRow(selectedRowId);
    };
    return (
        <div style={{ height: 400, width: '100%' }}>
            <DataGrid
                rows={rows}
                columns={columns}
                initialState={{
                    pagination: {
                        paginationModel: { page: 0, pageSize: 5 },
                    },
                }}
                pageSizeOptions={[5, 10]}
                checkboxSelection
                rowHeight={90}
                onRowSelectionModelChange={(newRowSelectionModel) => {
                    setRowSelectionModel(newRowSelectionModel);
                }}
                rowSelectionModel={rowSelectionModel}
            />
            {rowSelectionModel.length !== 0 && (
                <Box sx={{ '& button': { m: 1 } }}>
                    <div>
                        <Button variant="outlined" size="medium">
                            Continue
                        </Button>
                    </div>
                </Box>
            )}
        </div>

    );
}