from dataclasses import dataclass


@dataclass
class ActorConfig:
    name: str
    description: str = ""
    enabled: bool = True
