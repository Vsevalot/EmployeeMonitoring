package com.example.statohealth.viewmodel

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Feedbacks
import com.example.statohealth.Pages
import com.example.statohealth.data.FeedbacksModelResponse
import com.example.statohealth.data.MeModel
import com.example.statohealth.data.MeResponse
import com.example.statohealth.infrastructure.CurrentDate
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network


class AccountViewModel : ViewModel() {
    var me by mutableStateOf(MeModel("","","","","","","","",""))
    var progressVisible by mutableStateOf(false)
    var currentDay by mutableStateOf(CurrentDate())
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
        me = response.result
    }

    fun getRecommendationsClick() {
        navController.navigate(Pages.recommendationsPage)
    }

    fun navigateToInstructions() {
        navController.navigate(Pages.instructionsPage+"/false")
    }

    fun getFeedbacks(context: Context) {
        currentDay = CurrentDate()
        Network(context)
            .sendGetRequest(
                "feedbacks/${currentDay.toStringDate()}",
                ::updateProgressVisibility,
                ::successActionGetFeedbacks
            )
    }

    fun successActionGetFeedbacks(response: FeedbacksModelResponse) {
        Logger.log("OnSuccess $response")
        Feedbacks.morning = response.morning
        Feedbacks.evening = response.evening
    }
}