package com.example.statohealth.viewmodel

import android.content.Context
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Network
import com.example.statohealth.Pages
import com.example.statohealth.data.LoginModelRequest
import com.example.statohealth.data.ResultResponse


class LoginViewModel : ViewModel() {
    var login by mutableStateOf("")
    var password by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    lateinit var navController: NavHostController

    fun setLoginProperty(newLogin: String) {
        login = newLogin
    }

    fun setPasswordProperty(newPassword: String) {
        password = newPassword
    }

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun login(context: Context) {
        Network(context)
            .sendPostRequest(
                "login",
                LoginModelRequest(login, password),
                ::updateProgressVisibility,
                ::successLoginAction,
                false
            )
    }

    fun successLoginAction(response: ResultResponse) {
        Log.d("MyLog", "OnSuccess $response")
        Network.authorizationToken = response.result
        navController.navigate(Pages.instructionsPage)
    }

    fun register() {
        navController.navigate(Pages.registerPage)
    }
}