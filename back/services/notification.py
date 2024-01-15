from firebase_admin import messaging, initialize_app, credentials


class NotificationService:
    def __init__(self, path_to_cert: str):
        self._path_to_cert = path_to_cert
        self._creds = credentials.Certificate(path_to_cert)
        self._app = initialize_app(self._creds)

    def notify(self, device_token: str, title: str, body: str) -> None:
        msg = messaging.Message(
            messaging.Notification(
                title=title,
                body=body,
            ),
            token=device_token,
        )
        response = messaging.send(message=msg, app=self._app)
        print("Message sent", response)
