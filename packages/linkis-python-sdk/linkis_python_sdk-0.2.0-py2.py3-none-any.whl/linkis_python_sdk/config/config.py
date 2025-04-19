from dataclasses import dataclass


@dataclass
class LinkisConfig:
    base_url: str
    username: str
    password: str
