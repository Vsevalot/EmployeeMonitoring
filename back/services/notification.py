from logging import Logger

from firebase_admin import messaging, initialize_app, credentials


class NotificationService:
    def __init__(self, path_to_cert: str, logger: Logger):
        self._path_to_cert = path_to_cert
        self._logger = logger
        self._creds = credentials.Certificate(path_to_cert)
        self._app = initialize_app(self._creds)

    def notify(self, device_token: str, title: str, body: str) -> None:
        msg = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=device_token,
        )
        response = messaging.send(message=msg, app=self._app)
        self._logger.info(dict(message="Message sent", response=response))
