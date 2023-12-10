package com.example.statohealth.viewmodel

import android.content.Context
import android.os.Handler
import android.os.Looper
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Feedbacks
import com.example.statohealth.Pages
import com.example.statohealth.data.CategoryModel
import com.example.statohealth.data.EveningFeedbackModelRequest
import com.example.statohealth.data.FactorModel
import com.example.statohealth.data.FactorsModelResponse
import com.example.statohealth.data.ResultResponse
import com.example.statohealth.infrastructure.CurrentDate
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network
import java.util.Timer
import kotlin.concurrent.schedule

class FactorsViewModel : ViewModel() {
    var success by mutableStateOf(false)
    var progressVisible by mutableStateOf(false)
    var categories by mutableStateOf(arrayOf(CategoryModel(-1, "", arrayOf(FactorModel(-1, "")))))
    var choosenCategory by mutableStateOf(categories[0])
    var choosenFactor by mutableStateOf(categories[0].factors[0])

    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun sendButtonEnabled(): Boolean {
        return choosenFactor.id != -1
    }

    fun sendButtonClick(context: Context) {
        val currentdate = CurrentDate()
        Network(context)
            .sendPostRequest(
                "feedbacks/${currentdate.toStringDate()}/evening",
                EveningFeedbackModelRequest(
                    Feedbacks.evening?.id ?: throw Exception("Feedbacks.evening was null"),
                    choosenFactor.id
                ),
                ::updateProgressVisibility,
                ::successPostEveningStateAction
            )
    }

    fun successPostEveningStateAction(response: ResultResponse?) {
        Logger.log("OnSuccess $response")
        updateProgressVisibility(false)
        success = true
        val uiHandler = Handler(Looper.getMainLooper())
        val runnable = Runnable() {  navController.navigate(Pages.accountPage)}
        Timer().schedule(3000) {
            uiHandler.post(runnable);
        }
    }

    fun getCategories(context: Context) {
        Network(context)
            .sendGetRequest(
                "categories",
                ::updateProgressVisibility,
                ::successGetFactorsAction
            )
    }

    fun successGetFactorsAction(response: FactorsModelResponse) {
        Logger.log("OnSuccess $response")
        categories = response.result
    }
}