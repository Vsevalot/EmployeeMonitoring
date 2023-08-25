package com.example.statohealth.data

import com.google.gson.annotations.SerializedName

data class MorningFeedbackModelRequest(
    @SerializedName("state_id") val stateId: Int
)