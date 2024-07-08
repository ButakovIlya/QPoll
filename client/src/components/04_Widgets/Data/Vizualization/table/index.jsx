import { Paper, Table, TableBody, TableCell, TableRow } from '@mui/material';

import { StyledTableContainer, StyledTableHead } from './styled';

const CustomTable = ({ columns, data }) => {
  return (
    <StyledTableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="customized table">
        <StyledTableHead>
          <TableRow>
            {columns?.map((column) => (
              <TableCell key={column.id}>{column.caption}</TableCell>
            ))}
          </TableRow>
        </StyledTableHead>
        <TableBody>
          {data?.map((row) => (
            <TableRow key={row.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              {columns?.map((column) => (
                <TableCell key={column.id}>
                  {column.render ? column.render(row[column.key], row) : row[column.key]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </StyledTableContainer>
  );
};

export default CustomTable;
