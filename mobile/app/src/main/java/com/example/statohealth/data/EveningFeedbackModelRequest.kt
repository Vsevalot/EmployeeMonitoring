package com.example.statohealth.data

import com.google.gson.annotations.SerializedName

data class EveningFeedbackModelRequest(
    @SerializedName("state_id") val stateId: Int,
    @SerializedName("factor_id") val factorId: Int? = null
)