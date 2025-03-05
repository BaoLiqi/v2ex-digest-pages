// import React from "react";
import { useParams } from "react-router-dom";
import allPosts from "../all_posts.json"; // Import merged JSON from src

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

function PostDetailPage() {
  const { postId } = useParams();
  const postsData: Post[] = allPosts as Post[];
  const post = postsData.find((p) => p.id === parseInt(postId || ""));

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
                <details>
                  <summary>▽</summary>
                  {chunk.zh}
                </details>
                <br />
                {chunk.en}
                <br />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PostDetailPage;
