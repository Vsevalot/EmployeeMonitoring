package com.example.statohealth.data

data class CategoryModel(
    val id: Int,
    val name: String,
    val factors: Array<FactorModel>
)