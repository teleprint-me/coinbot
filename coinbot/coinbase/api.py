from dataclasses import dataclass, field


@dataclass
class API:
    settings: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return self.settings.get("key", "")

    @property
    def secret(self) -> str:
        return self.settings.get("secret", "")

    @property
    def version(self) -> int:
        return self.settings.get("version", 3)

    @property
    def rest(self) -> str:
        return self.settings.get("rest", "https://api.coinbase.com")

    def path(self, value: str) -> str:
        return f"/api/v{self.version}/brokerage/{value.lstrip('/')}"

    def url(self, value: str) -> str:
        return f"{self.rest}{self.path(value)}"
