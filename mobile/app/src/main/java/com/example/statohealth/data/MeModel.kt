package com.example.statohealth.data

import com.google.gson.annotations.SerializedName

data class MeModel(
    val id: String,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val surname: String,
    val birthdate: String,
    val company: String,
    val position: String,
    val phone: String,
    val email: String
)
