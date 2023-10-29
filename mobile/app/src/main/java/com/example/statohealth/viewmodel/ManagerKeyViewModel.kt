package com.example.statohealth.viewmodel

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Manager
import com.example.statohealth.Pages
import com.example.statohealth.data.ManagerModelResponse
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network

class ManagerKeyViewModel : ViewModel() {
    lateinit var navController: NavHostController
    var managerKey by mutableStateOf("")
    var progressVisible by mutableStateOf(false)

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun setManagerKeyProperty(value: String) {
        managerKey = value
    }

    fun isCorrectInput(): Boolean {
        return managerKey.isNotEmpty()
    }

    fun getManager(context: Context) {
        Network(context)
            .sendGetRequest(
                "managers/${managerKey}",
                ::updateProgressVisibility,
                ::successGetManagerAction,
                false
            )
    }

    fun successGetManagerAction(response: ManagerModelResponse) {
        Logger.log("OnSuccessGetManager $response")
        Manager.choosenManager = response.result
        navController.navigate(Pages.registerPage)
    }
}