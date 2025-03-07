import "./App.css";
import {
  HashRouter,
  Route,
  Routes,
  Link,
  useLocation,
  useSearchParams,
} from "react-router-dom";
import PostDetailPage from "./components/PostDetailPage";
import AnalyzedPostDetailPage from "./components/AnalyzedPostDetailPage";
import Pagination from "./components/Pagination";
import { useEffect, useState } from "react";
import postsIndex from "./posts_index.json";
import analyzedPostsIndex from "./posts_index_analyzed.json";

// Define the type for a post index entry
interface PostIndex {
  id: number;
  date: string;
  filename: string;
  title: string;
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
  const pageParam = searchParams.get("page");
  const currentPage = pageParam ? parseInt(pageParam) : 1;

  // Get current posts
  const indexOfLastPost: number = currentPage * postsPerPage;
  const indexOfFirstPost: number = indexOfLastPost - postsPerPage;

  const sortedPosts = [...postsData].sort((a, b) => {
    const aIsAnalyzed = analyzedPosts.some(
      (analyzedPost) => analyzedPost.id === a.id
    );
    const bIsAnalyzed = analyzedPosts.some(
      (analyzedPost) => analyzedPost.id === b.id
    );

    if (aIsAnalyzed && !bIsAnalyzed) {
      return -1;
    }
    if (!aIsAnalyzed && bIsAnalyzed) {
      return 1;
    }
    return 0;
  });
  const currentPosts = sortedPosts.slice(
    indexOfFirstPost || 0,
    indexOfLastPost || 0
  );

  // Change page
  const handlePageChange = (pageNumber: number) => {
    setSearchParams({ page: pageNumber.toString() });
    window.scrollTo(0, 0);
  };

  // Ensure valid page number
  useEffect(() => {
    if (
      isHomePage &&
      (isNaN(currentPage) || currentPage < 1 || currentPage > totalPages)
    ) {
      setSearchParams({ page: "1" });
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
                  <div className="post-title">
                    {post.title || `Post ID: ${post.id}`}
                  </div>
                  <div className="post-meta">
                    <span className="post-date">{post.date}</span>
                    <span className="post-id">#{post.id}</span>
                  </div>
                </Link>
                {analyzedPosts.some(
                  (analyzedPost) => analyzedPost.id === post.id
                ) && (
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
  return (
    <HashRouter>
      <MainContent />
    </HashRouter>
  );
}

export default App;
