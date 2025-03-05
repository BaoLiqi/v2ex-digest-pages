import React from "react";

interface ChunkProps {
  chunk: {
    zh: string;
    en: string;
  };
}

const Chunk: React.FC<ChunkProps> = ({ chunk }) => {
  return (
    <>
      <p>{chunk.en}</p>
      <details>
        <summary>Show Chinese</summary>
        <p>{chunk.zh}</p>
      </details>
    </>
  );
};

export default Chunk;
