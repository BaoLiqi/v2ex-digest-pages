// Pagination component
function Pagination({
  currentPage,
  totalPages,
  onPageChange,
}: {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}) {
  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages = [];
    const maxPagesToShow = 5;

    if (totalPages <= maxPagesToShow) {
      // If we have fewer pages than the max to show, display all pages
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Always include first page
      pages.push(1);

      // Calculate start and end of page range
      let start = Math.max(2, currentPage - 1);
      let end = Math.min(totalPages - 1, currentPage + 1);

      // Adjust if we're at the beginning or end
      if (currentPage <= 2) {
        end = Math.min(totalPages - 1, maxPagesToShow - 1);
      } else if (currentPage >= totalPages - 1) {
        start = Math.max(2, totalPages - maxPagesToShow + 2);
      }

      // Add ellipsis if needed
      if (start > 2) {
        pages.push(-1); // -1 represents ellipsis
      }

      // Add middle pages
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      // Add ellipsis if needed
      if (end < totalPages - 1) {
        pages.push(-2); // -2 represents ellipsis
      }

      // Always include last page
      if (totalPages > 1) {
        pages.push(totalPages);
      }
    }

    return pages;
  };

  return (
    <div className="pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="pagination-button"
      >
        ← Previous
      </button>

      <div className="pagination-numbers">
        {getPageNumbers().map((page, index) =>
          page < 0 ? (
            <span key={index} className="pagination-ellipsis">
              ...
            </span>
          ) : (
            <button
              key={index}
              onClick={() => onPageChange(page)}
              className={`pagination-number ${
                currentPage === page ? "active" : ""
              }`}
            >
              {page}
            </button>
          )
        )}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="pagination-button"
      >
        Next →
      </button>
    </div>
  );
}

export default Pagination;
