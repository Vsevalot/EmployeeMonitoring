package com.example.statohealth.viewmodel

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Pages
import com.example.statohealth.data.MeResponse
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network


class AccountViewModel : ViewModel() {
    var meText by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun getMe(context: Context) {
        Network(context)
            .sendGetRequest(
                "participants/me",
                ::updateProgressVisibility,
                ::successAction
            )
    }

    fun successAction(response: MeResponse) {
        Logger.log("OnSuccess $response")
        meText = response.result.firstName + response.result.lastName
    }

    fun getRecommendationsClick() {
        navController.navigate(Pages.recommendationsPage)
    }

}