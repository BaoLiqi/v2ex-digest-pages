import "./App.css";
import postsIndex from "./posts_index.json"; // Changed to relative import
import { BrowserRouter, Route, Routes, Link } from "react-router-dom";
import PostDetailPage from "./components/PostDetailPage";

// Define the type for a post index entry
interface PostIndex {
  id: number;
  date: string;
  filename: string;
  title: string;
}

function App() {
  // Cast postsIndex to the correct type
  const postsData: PostIndex[] = postsIndex as PostIndex[];
  const basename = "/v2ex-digest-pages"; // Define the basename here

  return (
    <BrowserRouter basename={basename}>
      <div>
        <h1>Posts</h1>
        <ul>
          {postsData.map((post, index) => (
            <li key={index}>
              {/*  Use the basename with Link.  This is unnecessary, but shows conceptually. */}
              {/*  <Link to={`${basename}/post/${post.id}`}> */}
              {/*  Use simple relative paths that don't start with slash. Better approach. */}
              <Link to={`post/${post.id}`}>
                {post.title || `Post ID: ${post.id}`}
              </Link>
            </li>
          ))}
        </ul>
        <Routes>
          {/* Corrected path to not include the base URL. */}
          <Route path="post/:postId" element={<PostDetailPage />} />
          <Route path="/"  element={ <div>home route</div> } />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;