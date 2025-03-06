from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass
class Chunk:
    en: str
    zh: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)  # Use asdict for simple dataclasses

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Chunk':
        return cls(**data)


@dataclass
class Block:
    chunks: List[Chunk]
    type: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunks": [chunk.to_dict() for chunk in self.chunks],
            "type": self.type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        return cls(
            chunks=[Chunk.from_dict(chunk_data)
                    for chunk_data in data["chunks"]],
            type=data["type"]
        )


@dataclass
class Post:
    id: int
    blocks: List[Block] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "blocks": [block.to_dict() for block in self.blocks]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        return cls(
            id=data["id"],
            blocks=[Block.from_dict(block_data)
                    for block_data in data["blocks"]]
        )


def main():
    # Example usage
    data = {
        "id": 1112469,
        "blocks": [
            {
                "chunks": [{"en": "Hello, World!", "zh": "你好，世界！"}],
                "type": "title",
            },
            {
                "chunks": [{"en": "Today, Cat Dad is very busy.", "zh": "今天猫爸爸很忙。"}],
                "type": "content",
            },
            {
                "chunks": [
                    {"en": "He needs to take care of the kittens.", "zh": "他要照顾小猫。"}
                ],
                "type": "replies",
            },
            {
                "chunks": [
                    {
                        "en": "And also earn money to support the family.",
                        "zh": "还要赚钱养家糊口。",
                    }
                ],
                "type": "replies",
            },
        ],
    }

    # --- Deserialization (Dict to Objects) ---
    post = Post.from_dict(data)

    # --- Serialization (Objects to Dict) ---
    serialized_data = post.to_dict()

    re_deserialized_post = Post.from_dict(serialized_data)

    # --- Check for equality (Important!) ---
    print("\nAre the original and re-deserialized posts equal?",
          post == re_deserialized_post)


if __name__ == "__main__":
    main()
