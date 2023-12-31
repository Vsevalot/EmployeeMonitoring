package com.example.statohealth.viewmodel

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.data.ResultResponse
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network


class RecommendationsViewModel : ViewModel() {
    var recommendationsText by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun getRecommendations(context: Context) {
        Network(context)
            .sendGetRequest(
                "participants/me/recommendations",
                ::updateProgressVisibility,
                ::successAction
            )
    }

    fun successAction(response: ResultResponse) {
        Logger.log("OnSuccess $response")
        recommendationsText = response.result
    }
}