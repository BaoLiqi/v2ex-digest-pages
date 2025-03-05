import React from "react";
import "./App.css";
import Post from "./components/Post";

function App() {
  return (
    <>
      <div>
        <h1>Vite + React</h1>
        <Post jsonFile="/posts_json/2025-02-16_1111723_crawler_v2_translate_v2.json" />
      </div>
    </>
  );
}

export default App;
