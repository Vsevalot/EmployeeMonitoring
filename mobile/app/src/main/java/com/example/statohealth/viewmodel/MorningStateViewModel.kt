package com.example.statohealth.viewmodel

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Pages
import com.example.statohealth.data.FeedbackModel
import com.example.statohealth.data.MorningFeedbackModelRequest
import com.example.statohealth.data.ResultResponse
import com.example.statohealth.data.StatesModelResponse
import com.example.statohealth.infrastructure.CurrentDate
import com.example.statohealth.infrastructure.Network

class MorningStateViewModel : ViewModel() {
    var progressVisible by mutableStateOf(false)
    var states by mutableStateOf(arrayOf(FeedbackModel(-1,"",0)))
    var choosenState by mutableStateOf(states[0])
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun sendButtonEnabled(): Boolean {
        return choosenState.id != -1
    }

    fun sendButtonClick(context: Context) {
        val currentdate = CurrentDate()
        Network(context)
            .sendPostRequest(
                "feedbacks/${currentdate.toStringDate()}/morning",
                MorningFeedbackModelRequest(choosenState.id),
                ::updateProgressVisibility,
                ::successPostMorningStateAction
            )
    }

    fun successPostMorningStateAction(response: ResultResponse?) {
        Log.d("MyLog", "OnSuccess $response")
        navController.navigate(Pages.accountPage)
    }

    fun getStates(context: Context) {
        Network(context)
            .sendGetRequest(
                "states",
                ::updateProgressVisibility,
                ::successGetStatesAction
            )
    }

    fun successGetStatesAction(response: StatesModelResponse) {
        Log.d("MyLog", "OnSuccess $response")
        states = response.result
    }
}