import { useParams } from "react-router-dom";
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
    return <div>Loading post...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!post) {
    return <div>Post not found</div>;
  }

  return (
    <div>
      <h2>{post.id}</h2>
      <div>
        {post.blocks.map((block, blockIndex) => (
          <div key={blockIndex}>
            {block.chunks.map((chunk, chunkIndex) => (
              <div key={chunkIndex}>
                <br />
                {chunk.en}
                <br />
                <details>
                  <summary></summary>
                  {chunk.zh}
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