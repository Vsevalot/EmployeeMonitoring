package com.example.statohealth.viewmodel

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Feedbacks
import com.example.statohealth.Pages
import com.example.statohealth.data.EveningFeedbackModelRequest
import com.example.statohealth.data.FactorModel
import com.example.statohealth.data.FactorsModelResponse
import com.example.statohealth.data.StatusResponse
import com.example.statohealth.data.SubFactorModel
import com.example.statohealth.data.SubFactorType
import com.example.statohealth.infrastructure.CurrentDate
import com.example.statohealth.infrastructure.Network

class FactorsViewModel : ViewModel() {
    var progressVisible by mutableStateOf(false)
    var factors by mutableStateOf(arrayOf(FactorModel(-1, "", arrayOf(SubFactorModel(-1, "", SubFactorType.SINGLE)))))
    var choosenFactor by mutableStateOf(factors[0])
    var choosenSubFactor by mutableStateOf(factors[0].factors[0])
    var subFactorText by mutableStateOf("")

    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun sendButtonEnabled(): Boolean {
        return choosenSubFactor.id != -1 && (choosenSubFactor.type == SubFactorType.SINGLE
                || (choosenSubFactor.type == SubFactorType.TEXT && subFactorText.isNotEmpty()))
    }

    fun sendButtonClick(context: Context) {
        val currentdate = CurrentDate()
        Network(context)
            .sendPostRequest(
                "feedbacks/${currentdate.year}.${currentdate.month}.${currentdate.day}/evening",
                EveningFeedbackModelRequest(
                    Feedbacks.evening?.id ?: throw Exception("Feedbacks.evening was null"),
                    choosenSubFactor.id,
                    subFactorText.ifEmpty { null }
                ),
                ::updateProgressVisibility,
                ::successPostEveningStateAction
            )
    }

    fun successPostEveningStateAction(response: StatusResponse) {
        Log.d("MyLog", "OnSuccess $response")
        navController.navigate(Pages.accountPage)
    }

    fun getFactors(context: Context) {
        Network(context)
            .sendGetRequest(
                "factors",
                ::updateProgressVisibility,
                ::successGetFactorsAction
            )
    }

    fun successGetFactorsAction(response: FactorsModelResponse) {
        Log.d("MyLog", "OnSuccess $response")
        factors = response.result
    }
}