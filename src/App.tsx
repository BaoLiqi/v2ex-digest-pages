import "./App.css";
import postsIndex from "./posts_index.json";
import { BrowserRouter, Route, Routes, Link, useLocation, useSearchParams } from "react-router-dom";
import PostDetailPage from "./components/PostDetailPage";
import AnalyzedPostDetailPage from "./components/AnalyzedPostDetailPage";
import { useEffect, useState } from "react";
import analyzedPostsIndex from "./analyzed_posts_index.json";

// Define the type for a post index entry
interface PostIndex {
  id: number;
  date: string;
  filename: string;
  title: string;
}

// Pagination component
function Pagination({ currentPage, totalPages, onPageChange }: { 
  currentPage: number; 
  totalPages: number; 
  onPageChange: (page: number) => void 
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
        {getPageNumbers().map((page, index) => (
          page < 0 ? (
            <span key={index} className="pagination-ellipsis">...</span>
          ) : (
            <button
              key={index}
              onClick={() => onPageChange(page)}
              className={`pagination-number ${currentPage === page ? 'active' : ''}`}
            >
              {page}
            </button>
          )
        ))}
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

// Main content component that conditionally renders based on route
function MainContent() {
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams();
  const isHomePage = location.pathname === "/";
  const postsData: PostIndex[] = postsIndex as PostIndex[];
  const [analyzedPosts] = useState(analyzedPostsIndex as PostIndex[]);

  // Pagination state
  const postsPerPage = 10;
  const totalPages = Math.ceil(postsData.length / postsPerPage);
  const pageParam = searchParams.get('page');
  const currentPage = pageParam ? parseInt(pageParam) : 1;

  // Get current posts
  const indexOfLastPost: number = currentPage * postsPerPage;
  const indexOfFirstPost: number = indexOfLastPost - postsPerPage;

  const sortedPosts = [...postsData].sort((a, b) => {
    const aIsAnalyzed = analyzedPosts.some((analyzedPost) => analyzedPost.id === a.id);
    const bIsAnalyzed = analyzedPosts.some((analyzedPost) => analyzedPost.id === b.id);

    if (aIsAnalyzed && !bIsAnalyzed) {
      return -1;
    }
    if (!aIsAnalyzed && bIsAnalyzed) {
      return 1;
    }
    return 0;
  });
  const currentPosts = sortedPosts.slice(indexOfFirstPost || 0, indexOfLastPost || 0);
  
  // Change page
  const handlePageChange = (pageNumber: number) => {
    setSearchParams({ page: pageNumber.toString() });
    window.scrollTo(0, 0);
  };
  
  // Ensure valid page number
  useEffect(() => {
    if (isHomePage && (isNaN(currentPage) || currentPage < 1 || currentPage > totalPages)) {
      setSearchParams({ page: '1' });
    }
  }, [currentPage, isHomePage, totalPages, setSearchParams]);

  return (
    <div className="app-container">
      {isHomePage && (
        <>
          <header className="forum-header">
            <h1>V2EX Digest</h1>
          </header>
          <div className="post-list">
            {currentPosts.map((post, index) => (
              <div key={index} className="post-item">
                <Link to={`post/${post.id}`} className="post-link">
                  <div className="post-title">{post.title || `Post ID: ${post.id}`}</div>
                  <div className="post-meta">
                    <span className="post-date">{post.date}</span>
                    <span className="post-id">#{post.id}</span>
                  </div>
                </Link>
                {analyzedPosts.some((analyzedPost) => analyzedPost.id === post.id) && (
                  <div className="post-actions">
                    <Link to={`analyzed/${post.id}`} className="analyzed-link">
                      View Analysis
                    </Link>
                  </div>
                )}
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <Pagination 
              currentPage={currentPage} 
              totalPages={totalPages} 
              onPageChange={handlePageChange} 
            />
          )}
        </>
      )}
      
      <Routes>
        <Route path="post/:postId" element={<PostDetailPage />} />
        <Route path="analyzed/:postId" element={<AnalyzedPostDetailPage />} />
        <Route path="/" element={<div className="home-placeholder"></div>} />
      </Routes>
    </div>
  );
}

function App() {
  const basename = "/v2ex-digest-pages";

  return (
    <BrowserRouter basename={basename}>
      <MainContent />
    </BrowserRouter>
  );
}

export default App;
