import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import postsIndex from "../posts_index.json";

interface Chunk {
  zh: string;
  en: string;
}

interface Block {
  chunks: Chunk[];
  type: string;
}

interface Post {
  id: number;
  blocks: Block[];
}

interface PostIndex {
  id: number;
  date: string;
  filename: string;
  title: string;
}

function PostDetailPage() {
  const { postId } = useParams();
  const [post, setPost] = useState<Post | null>(null);
  const [postInfo, setPostInfo] = useState<PostIndex | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        setLoading(true);
        setError(null);

        const postIndex = (postsIndex as PostIndex[]).find(
          (p) => p.id === parseInt(postId || "")
        );

        if (!postIndex) {
          setError("Post not found in index");
          setLoading(false);
          return;
        }

        setPostInfo(postIndex);

        const response = await fetch(
          `${import.meta.env.BASE_URL}posts_json/${postIndex.filename}`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch post: ${response.statusText}`);
        }

        const postData = await response.json();
        setPost(postData);
      } catch (err) {
        setError(
          `Error loading post: ${
            err instanceof Error ? err.message : String(err)
          }`
        );
        console.error("Error fetching post:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [postId]);

  if (loading) {
    return <div className="loading-container">Loading post...</div>;
  }

  if (error) {
    return <div className="error-container">Error: {error}</div>;
  }

  if (!post || !postInfo) {
    return <div className="error-container">Post not found</div>;
  }

  return (
    <div className="post-detail-container">
      <div className="post-header">
        <Link to="/" className="back-button">← Back to Posts</Link>
        <h2 className="post-title">{postInfo.title || `Post #${post.id}`}</h2>
        <div className="post-meta">
          <span className="post-date">{postInfo.date}</span>
          <span className="post-id">#{post.id}</span>
        </div>
      </div>
      
      <div className="post-content">
        {post.blocks.map((block, blockIndex) => (
          <div key={blockIndex} className={`block block-${block.type}`}>
            {block.chunks.map((chunk, chunkIndex) => (
              <div key={chunkIndex} className="chunk">
                <div className="chunk-en">{chunk.en}</div>
                <details className="chunk-zh-details">
                  <summary>Original Text</summary>
                  <div className="chunk-zh">{chunk.zh}</div>
                </details>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PostDetailPage;
