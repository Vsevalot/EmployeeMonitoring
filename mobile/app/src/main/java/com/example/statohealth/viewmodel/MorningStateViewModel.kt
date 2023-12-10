package com.example.statohealth.viewmodel

import android.content.Context
import android.os.Handler
import android.os.Looper
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
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network
import java.util.Timer
import kotlin.concurrent.schedule


class MorningStateViewModel : ViewModel() {
    var success by mutableStateOf(false)
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
        Logger.log("OnSuccess $response")
        updateProgressVisibility(false)
        success = true
        val uiHandler = Handler(Looper.getMainLooper())
        val runnable = Runnable() {  navController.navigate(Pages.accountPage)}
            Timer().schedule(3000) {
                uiHandler.post(runnable);
        }
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
        Logger.log("OnSuccess $response")
        states = response.result
    }
}