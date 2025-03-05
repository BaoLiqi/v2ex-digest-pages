import React from "react";
import "./App.css";
import allPosts from "../src/all_posts.json";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import PostDetailPage from "./components/PostDetailPage";

// Define the type for a chunk
interface Chunk {
  zh: string;
  en: string;
}

// Define the type for a block
interface Block {
  chunks: Chunk[];
  type: string;
}

// Define the type for a post
interface Post {
  id: number;
  blocks: Block[];
}

function App() {
  // Cast allPosts to the correct type
  const postsData: Post[] = allPosts as Post[];

  return (
    <Router>
      <div>
        <h1>Posts</h1>
        <ul>
          {postsData.map((post, index) => (
            <li key={index}>
              <Link to={`/post/${post.id}`}>
                {post.blocks[0]?.chunks[0]?.zh || `Post ID: ${post.id}`}
              </Link>
            </li>
          ))}
        </ul>
        <Routes>
          <Route path="/post/:postId" element={<PostDetailPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
