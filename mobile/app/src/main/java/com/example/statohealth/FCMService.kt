package com.example.statohealth

import android.content.Context
import android.provider.Settings
import com.example.statohealth.data.ResultResponse
import com.example.statohealth.data.UpdateTokenModelRequest
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network
import com.google.firebase.messaging.FirebaseMessagingService

class FCMService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        Logger.log("Refreshed token: $token")

        var deviceId =
            Settings.Secure.getString(this.contentResolver, Settings.Secure.ANDROID_ID)
        putTokenToServer(this, deviceId, token)
    }

    fun putTokenToServer(context: Context, deviceId: String, token: String) {
        Network(context)
            .sendPutRequest(
                "devices/${deviceId}/token",
                UpdateTokenModelRequest(token),
                ::successPutTokenToServerAction,
                false
            )
    }

    fun successPutTokenToServerAction(response: ResultResponse?) {
        Logger.log("OnSuccess $response")
    }
}