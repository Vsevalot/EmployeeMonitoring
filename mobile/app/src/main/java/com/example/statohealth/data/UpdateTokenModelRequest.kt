package com.example.statohealth.data

import com.google.gson.annotations.SerializedName

data class UpdateTokenModelRequest(
    @SerializedName("push_token") val pushToken: String
)