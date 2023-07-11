import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { useRouter } from 'next/navigation'
const columns = [
    { id: 'name', label: 'Group Name', minWidth: 100, headerAlign: 'center', align: 'center' },
    { id: 'id', label: 'Group ID', minWidth: 100, headerAlign: 'center', align: 'center' },
    { id: 'faucetCount', label: 'The Number Of Faucets', minWidth: 170, headerAlign: 'center', align: 'center' },
    {
        id: 'totalWaterConsumption',
        label: 'Total Usage Water(L)',
        minWidth: 170,
        headerAlign: 'center',
        align: 'center',
        format: (value) => value.toLocaleString('en-US'),
    },
    {
        id: 'leakingFaucetCount',
        label: 'The Number Of Leaking Faucets',
        minWidth: 200,
        headerAlign: 'center',
        align: 'center',
        format: (value) => value.toLocaleString('en-US'),
    },
];

function createData(name, id, faucetCount, totalWaterConsumption, leakingFaucetCount) {
    return { name, id, faucetCount, totalWaterConsumption, leakingFaucetCount };
}

const rows = [
    createData('台科大一餐', 'LIeBZ', 2, 1324171354, 1),
    createData('彰一興', 'yoXgp', 2, 1403500365, 1),
];

export default function ColumnGroupingTable() {
    const router = useRouter();
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    return (
        <Paper sx={{ width: '100%' }}>
            <TableContainer sx={{ maxHeight: 440 }}>
                <Table stickyHeader aria-label="sticky table" >
                    <TableHead>
                        <TableRow>
                            <TableCell align="center" colSpan={2}>
                                GROUP
                            </TableCell>
                            <TableCell align="center" colSpan={3}>
                                Details
                            </TableCell>
                        </TableRow>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell
                                    key={column.id}
                                    align={column.align}
                                    style={{ top: 57, minWidth: column.minWidth }}
                                >
                                    {column.label}
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody >
                        {rows
                            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                            .map((row) => {
                                return (
                                    <TableRow hover role="checkbox" tabIndex={-1} key={row.code} >
                                        {columns.map((column) => {
                                            const value = row[column.id];
                                            return (
                                                <TableCell key={column.id} align={column.align} type="button" onClick={() => router.push(`/home/soc/${row.id}`)}>
                                                    {column.format && typeof value === 'number'
                                                        ? column.format(value)
                                                        : value}
                                                </TableCell>
                                            );
                                        })}
                                    </TableRow>
                                );
                            })}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPageOptions={[10, 25, 100]}
                component="div"
                count={rows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </Paper>
    );
}