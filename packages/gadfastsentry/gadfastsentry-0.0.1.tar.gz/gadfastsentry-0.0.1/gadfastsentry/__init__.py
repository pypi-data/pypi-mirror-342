import logging

import sentry_sdk


class Sentry:
    def __init__(
        self,
        env: str,
        dsn: str,
        debug: bool = True,
        sample: float = 1.0,
        pii: bool = True,
        version: str = "0.0.1",
        loglevel: int = logging.ERROR,
    ) -> None:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=sample,
            environment=env,
            debug=debug,
            release=version,
            send_default_pii=pii,
            integrations=[sentry_sdk.integrations.logging.LoggingIntegration(level=None, event_level=loglevel)],
        )
        logging.getLogger("sentry_sdk.errors").setLevel(loglevel)


__all__ = ["Sentry"]
