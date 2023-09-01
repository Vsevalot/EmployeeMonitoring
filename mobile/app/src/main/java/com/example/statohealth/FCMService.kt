package com.example.statohealth

import com.example.statohealth.infrastructure.Logger
import com.google.firebase.messaging.FirebaseMessagingService

class FCMService: FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        Logger.log("Refreshed token: $token")

        // If you want to send messages to this application instance or
        // manage this apps subscriptions on the server side, send the
        // FCM registration token to your app server.
    }
}