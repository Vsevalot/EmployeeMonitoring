package com.example.statohealth.view.model

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Network
import com.example.statohealth.Pages
import com.example.statohealth.data.ResultResponse


class InstructionsViewModel : ViewModel() {
    var instructionsText by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun getInstructions(context: Context) {
        Network(context)
            .sendGetRequest(
                "instructions",
                ::updateProgressVisibility,
                ::successAction
            )
    }

    fun successAction(response: ResultResponse) {
        Log.d("MyLog", "OnSuccess $response")
        instructionsText = response.result
    }

    fun start() {
        navController.navigate(Pages.timePickerPage)
    }

}