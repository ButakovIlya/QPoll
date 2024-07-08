import { useState } from 'react';

const usePagination = (defaultPageSize = 6) => {
  const [pageSize, setPageSize] = useState(defaultPageSize);
  const [currPage, setCurrPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const handlePageSizeChange = (size) => {
    setPageSize(size);
    setCurrPage(1);
  };

  const handlePageChange = (page) => {
    setCurrPage(page);
  };

  return {
    pageSize,
    currPage,
    totalPages,
    setTotalPages,
    handlePageSizeChange,
    handlePageChange,
  };
};

export default usePagination;
