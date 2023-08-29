package com.example.statohealth.data

import com.google.gson.annotations.SerializedName

data class RegisterModelRequest(
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val surname: String,
    val birthdate: String,
    val phone: String,
    val position: String,
    val email: String,
    val password: String,
    @SerializedName("manager_id") val managerId: Int)