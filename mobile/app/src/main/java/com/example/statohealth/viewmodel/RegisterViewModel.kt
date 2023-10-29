package com.example.statohealth.viewmodel

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Pages
import com.example.statohealth.data.ManagerModel
import com.example.statohealth.data.RegisterModelRequest
import com.example.statohealth.data.ResultResponse
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network

class RegisterViewModel : ViewModel() {
    lateinit var navController: NavHostController
    var manager by mutableStateOf(ManagerModel(-1, "", "", "", "", ""))
    var firstName by mutableStateOf("")
    var lastName by mutableStateOf("")
    var surname by mutableStateOf("")
    var birthdate by mutableStateOf("")
    var position by mutableStateOf("")
    var phone by mutableStateOf("")
    var email by mutableStateOf("")
    var password by mutableStateOf("")
    var passwordRepeat by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    var passwordVisible by mutableStateOf(false)
    var passwordRepeatVisible by mutableStateOf(false)
    var personalDataAgreement by mutableStateOf(false)

    fun setFirstNameProperty(value: String) {
        firstName = value
    }

    fun setLastNameProperty(value: String) {
        lastName = value
    }

    fun setSurnameProperty(value: String) {
        surname = value
    }

    fun setBirthdateProperty(value: String) {
        birthdate = value
    }

    fun setPositionProperty(value: String) {
        position = value
    }

    fun setPhoneProperty(value: String) {
        phone = value
    }

    fun setEmailProperty(value: String) {
        email = value
    }

    fun setPasswordProperty(value: String) {
        password = value
    }

    fun setPasswordRepeatProperty(value: String) {
        passwordRepeat = value
    }

    fun updatePersonalDataAgreement(value: Boolean) {
        personalDataAgreement = value
    }

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun invertPasswordVisible() {
        passwordVisible = !passwordVisible
    }

    fun invertPasswordRepeatVisible() {
        passwordRepeatVisible = !passwordRepeatVisible
    }

    fun isCorrectInput(): Boolean {
        return password == passwordRepeat
                && firstName.isNotEmpty()
                && lastName.isNotEmpty()
                && surname.isNotEmpty()
                && birthdate.isNotEmpty()
                && position.isNotEmpty()
                && phone.isNotEmpty()
                && email.isNotEmpty()
                && password.isNotEmpty()
                && passwordRepeat.isNotEmpty()
                && birthdate.length == 8
                && personalDataAgreement == true
    }

    fun register(context: Context) {
        Network(context)
            .sendPostRequest(
                "register/participants",
                RegisterModelRequest(
                    firstName,
                    lastName,
                    surname,
                    "${birthdate.take(4)}-${birthdate.drop(4).take(2)}-${birthdate.takeLast(2)}",
                    position,
                    phone,
                    email,
                    password,
                    manager.id,
                    personalDataAgreement
                ) as Any,
                ::updateProgressVisibility,
                ::successRegisterAction,
                false
            )
    }

    fun successRegisterAction(response: ResultResponse?) {
        Logger.log("OnSuccess $response")
        navController.navigate(Pages.loginPage)
    }
}