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
import com.example.statohealth.data.ManagerModel
import com.example.statohealth.data.ManagersModelResponse
import com.example.statohealth.data.RegisterModelRequest
import com.example.statohealth.data.StatusResponse

class RegisterViewModel : ViewModel() {
    lateinit var navController: NavHostController
    var managers by mutableStateOf(arrayOf(ManagerModel(-1,"","","","","")))
    var choosenManager by mutableStateOf(managers[0])
    var expanded by mutableStateOf(false)
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
            && choosenManager.id != -1
            && position.isNotEmpty()
            && phone.isNotEmpty()
            && email.isNotEmpty()
            && password.isNotEmpty()
            && passwordRepeat.isNotEmpty()
    }

    fun register(context: Context) {
        Network(context)
            .sendPostRequest(
                "register/employees",
                RegisterModelRequest(firstName,lastName,surname,birthdate,position,phone,email,password,choosenManager.id) as Any,
                ::updateProgressVisibility,
                ::successRegisterAction,
                false
            )
    }

    fun successRegisterAction(response: StatusResponse) {
        Log.d("MyLog", "OnSuccess $response")
        navController.navigate(Pages.loginPage)
    }

    fun getManagers(context: Context) {
        Network(context)
            .sendGetRequest(
                "managers",
                ::updateProgressVisibility,
                ::successGetManagersAction,
                false
            )
    }

    fun successGetManagersAction(response: ManagersModelResponse) {
        Log.d("MyLog", "OnSuccessGetManagers $response")
        managers = response.result
    }
}