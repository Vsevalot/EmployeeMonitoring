package com.example.statohealth.data

data class FactorModel(
    val id: Int,
    val name: String,
    val factors: Array<SubFactorModel>
)