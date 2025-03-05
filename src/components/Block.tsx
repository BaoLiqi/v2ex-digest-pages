import React from "react";
import Chunk from "./Chunk";

interface BlockProps {
  block: {
    type: string;
    chunks: {
      zh: string;
      en: string;
    }[];
  };
}

const Block: React.FC<BlockProps> = ({ block }) => {
  const renderBlockContent = () => {
    switch (block.type) {
      case "title":
        return (
          <h2>
            {block.chunks.map((chunk, index) => (
              <Chunk key={index} chunk={chunk} />
            ))}
          </h2>
        );
      case "content":
        return (
          <>
            {block.chunks.map((chunk, index) => (
              <Chunk key={index} chunk={chunk} />
            ))}
          </>
        );
      case "replies":
        return (
          <ul>
            {block.chunks.map((chunk, index) => (
              <li key={index}>
                <Chunk chunk={chunk} />
              </li>
            ))}
          </ul>
        );
      default:
        return null;
    }
  };

  return <div>{renderBlockContent()}</div>;
};

export default Block;
