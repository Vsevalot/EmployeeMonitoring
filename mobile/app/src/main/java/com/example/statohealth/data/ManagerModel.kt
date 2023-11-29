package com.example.statohealth.data

import com.google.gson.annotations.SerializedName

data class ManagerModel(
    val id: Int,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val surname: String,
    val company: String,
    val department: String
)