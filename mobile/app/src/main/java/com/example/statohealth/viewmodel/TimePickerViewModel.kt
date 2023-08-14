package com.example.statohealth.viewmodel

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.infrastructure.Network
import com.example.statohealth.Pages
import com.example.statohealth.data.FeedbackModel
import com.example.statohealth.data.FeedbacksModelResponse
import com.example.statohealth.infrastructure.CurrentDate


class TimePickerViewModel : ViewModel() {
    var progressVisible by mutableStateOf(false)
    var morningFeedback by mutableStateOf<FeedbackModel?>(null)
    var eveningFeedback by mutableStateOf<FeedbackModel?>(null)
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun morningEnabled(): Boolean {
        val currentDate = CurrentDate()
        return morningFeedback == null && eveningFeedback == null && currentDate.isMorning()
    }

    fun eveningEnabled(): Boolean {
        val currentDate = CurrentDate()
        return eveningFeedback == null && morningFeedback != null && currentDate.isEvening()
    }

    fun morningClick() {
        navController.navigate(Pages.morningStatePage)
    }

    fun eveningClick() {
        navController.navigate(Pages.eveningStatePage)
    }

    fun getFeedbacks(context: Context) {
        val currentdate = CurrentDate()
        Network(context)
            .sendGetRequest(
                "feedbacks/${currentdate.year}.${currentdate.month}.${currentdate.day}",
                ::updateProgressVisibility,
                ::successAction
            )
    }

    fun successAction(response: FeedbacksModelResponse) {
        Log.d("MyLog", "OnSuccess $response")
        morningFeedback = response.morning
        eveningFeedback = response.evening
    }
}