from enum import Enum


class KosmoyEnvironment(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def api_url(self) -> str:
        if self == KosmoyEnvironment.LOCAL:
            return "http://localhost:8000"
        elif self == KosmoyEnvironment.DEVELOPMENT:
            return "https://api.develop.kosmoy.io"
        elif self == KosmoyEnvironment.STAGING:
            return "https://api.staging.kosmoy.io"
        elif self == KosmoyEnvironment.PRODUCTION:
            return "https://api.kosmoy.io"
        return "https://api.staging.kosmoy.io"