import React, { useState, useEffect } from "react";
import Block from "./Block";

interface PostProps {
  jsonFile: string; // Path to the JSON file
}

interface PostData {
  id: number;
  blocks: any[]; // Use 'any[]' for now, refine later based on actual data structure
}

const Post: React.FC<PostProps> = ({ jsonFile }) => {
  const [postData, setPostData] = useState<PostData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await fetch(jsonFile);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: PostData = await response.json();
        setPostData(data);
        setLoading(false);
      } catch (e: any) {
        setError(e.message);
        setLoading(false);
      }
    };

    fetchPost();
  }, [jsonFile]);

  if (loading) {
    return <p>Loading post...</p>;
  }

  if (error) {
    return <p>Error loading post: {error}</p>;
  }

  if (!postData) {
    return <p>Post data not found.</p>;
  }

  return (
    <div className="post">
      {postData.blocks.map((block, index) => (
        <Block key={index} block={block} />
      ))}
    </div>
  );
};

export default Post;
