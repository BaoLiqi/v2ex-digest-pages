import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import analyzedPostsIndex from "../analyzed_posts_index.json";
import { colorPalette } from "./colorPalette";
import "./AnalyzedPostDetailPage.css";

interface TokenAnalysis {
  token: string;
  candidates: {
    token: string;
    probability: number;
  }[];
}

interface Chunk {
  zh: string;
  en: string;
  analysis: TokenAnalysis[];
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

function probabilityToColor(probability: number): string {
  const index = Math.floor(probability * (colorPalette.length - 1));
  return colorPalette[index];
}

function AnalyzedPostDetailPage() {
  const { postId } = useParams();
  const [post, setPost] = useState<Post | null>(null);
  const [postInfo, setPostInfo] = useState<PostIndex | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTokens, setActiveTokens] = useState<{ [key: string]: boolean }>(
    {}
  );

  useEffect(() => {
    const fetchPost = async () => {
      try {
        setLoading(true);
        setError(null);

        const postIndex = (analyzedPostsIndex as PostIndex[]).find(
          (p) => p.id === parseInt(postId || "")
        );

        if (!postIndex) {
          setError("Post not found in index");
          setLoading(false);
          return;
        }

        setPostInfo(postIndex);

        const response = await fetch(
          `${import.meta.env.BASE_URL}posts_json_analyzed/${postIndex.filename}`
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

  const toggleTokenActive = (
    blockIndex: number,
    chunkIndex: number,
    tokenIndex: number
  ) => {
    const tokenKey = `${blockIndex}-${chunkIndex}-${tokenIndex}`;
    setActiveTokens((prev) => {
      const newActiveTokens = { ...prev };

      // If this token is already active, deactivate it
      if (newActiveTokens[tokenKey]) {
        delete newActiveTokens[tokenKey];
      } else {
        // Otherwise activate it and deactivate all others
        Object.keys(newActiveTokens).forEach((key) => {
          delete newActiveTokens[key];
        });
        newActiveTokens[tokenKey] = true;
      }

      return newActiveTokens;
    });
  };

  // Close all tooltips when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      setActiveTokens({});
    };

    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

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
        <Link to="/" className="back-button">
          ← Back to Posts
        </Link>
        <h2 className="post-title">{postInfo.title || `Post #${post.id}`}</h2>
        <div className="post-meta">
          <span className="post-date">{postInfo.date}</span>
          <span className="post-id">#{post.id}</span>
        </div>
      </div>

      <div className="color-legend">
        <div className="color-legend-label">Token Probability:</div>
        <div className="color-gradient-container">
          <div className="color-gradient">
            {colorPalette.map((color, index) => (
              <div
                key={index}
                className="color-stop"
                style={{ backgroundColor: color }}
              />
            ))}
          </div>
          <div className="color-legend-values">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
        </div>
      </div>

      <div className="post-content">
        {post.blocks.map((block, blockIndex) => (
          <div key={blockIndex} className={`block block-${block.type}`}>
            {block.chunks.map((chunk, chunkIndex) => (
              <div key={chunkIndex} className="chunk">
                <div className="chunk-en analyzed-text">
                  {chunk.analysis.map((tokenAnalysis, tokenIndex) => {
                    // Find the probability of this token
                    let probability = 0;
                    for (const candidate of tokenAnalysis.candidates) {
                      if (
                        candidate.token.trim() === tokenAnalysis.token.trim()
                      ) {
                        probability = candidate.probability;
                        break;
                      }
                    }

                    const tokenKey = `${blockIndex}-${chunkIndex}-${tokenIndex}`;
                    const isActive = activeTokens[tokenKey] || false;

                    return (
                      <span
                        key={tokenIndex}
                        className={`token ${isActive ? "active" : ""}`}
                        style={{ color: probabilityToColor(probability) }}
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleTokenActive(blockIndex, chunkIndex, tokenIndex);
                        }}
                      >
                        {tokenAnalysis.token}
                        {isActive && (
                          <div className="token-tooltip">
                            {tokenAnalysis.candidates.map(
                              (candidate, candidateIndex) => (
                                <div key={candidateIndex} className="candidate">
                                  <span className="candidate-token">
                                    {candidate.token}
                                  </span>
                                  <span className="candidate-probability">
                                    {(candidate.probability * 100).toFixed(2)}%
                                  </span>
                                </div>
                              )
                            )}
                            {/* Variance Calculation and Display */}
                            <div className="candidate">
                              <span className="candidate-token">Variance:</span>
                              <span className="candidate-probability">
                                {(() => {
                                  const probabilities =
                                    tokenAnalysis.candidates.map(
                                      (c) => c.probability
                                    );
                                  const mean =
                                    probabilities.reduce((a, b) => a + b, 0) /
                                    probabilities.length;
                                  const variance =
                                    probabilities.reduce(
                                      (a, b) => a + (b - mean) ** 2,
                                      0
                                    ) / probabilities.length;
                                  return variance.toFixed(2) + "%";
                                })()}
                              </span>
                            </div>
                          </div>
                        )}
                      </span>
                    );
                  })}
                </div>
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

export default AnalyzedPostDetailPage;
