from dataclasses import dataclass

@dataclass
class Tag:
    name: str
    category: str
    confidence: float