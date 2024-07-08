import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';

import CustomTable from '../index';

describe('CustomTable', () => {
  const columns = [
    { id: 'name', caption: 'Name', key: 'name' },
    { id: 'age', caption: 'Age', key: 'age', render: (data) => <strong>{data}</strong> },
  ];
  const data = [
    { id: 1, name: 'John Doe', age: 30 },
    { id: 2, name: 'Jane Doe', age: 25 },
  ];

  it('renders table headers and rows correctly', () => {
    render(<CustomTable columns={columns} data={data} />);

    columns.forEach((column) => {
      expect(screen.getByText(column.caption)).toBeInTheDocument();
    });

    data.forEach((row) => {
      expect(screen.getByText(row.name)).toBeInTheDocument();
      expect(screen.getByText(row.age.toString())).toHaveStyle('font-weight: bold');
    });
  });

  it('handles empty data gracefully', () => {
    render(<CustomTable columns={columns} data={[]} />);

    columns.forEach((column) => {
      expect(screen.getByText(column.caption)).toBeInTheDocument();
    });

    data.forEach((row) => {
      expect(screen.queryByText(row.name)).toBeNull();
      expect(screen.queryByText(row.age.toString())).toBeNull();
    });
  });

  it('renders without data if no data prop is provided', () => {
    render(<CustomTable columns={columns} />);

    columns.forEach((column) => {
      expect(screen.getByText(column.caption)).toBeInTheDocument();
    });

    const rowgroups = screen.getAllByRole('rowgroup');
    const tbody = rowgroups[1];
    expect(tbody).toBeEmptyDOMElement();
  });
});
