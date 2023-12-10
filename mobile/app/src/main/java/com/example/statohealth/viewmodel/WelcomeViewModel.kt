package com.example.statohealth.viewmodel

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Pages


class WelcomeViewModel : ViewModel() {
    var welcomeText by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun getWelcomeText(context: Context) {
        welcomeText = "    Мы рады приветствовать Вас в нашем приложении, созданном специально для оценки Вашего самочувствия и благополучия на рабочем месте.\n" +
                "    Мы искренне хотим помочь Вам и Вашему работодателю создать комфортные условия для Вашей работы.\n" +
                "    Ваше мнение очень важно для нас, и мы уверены, что Ваше участие поможет сделать мир лучше!"
    }

    fun navigateToInstructions() {
        navController.navigate(Pages.instructionsPage+"/true")
    }

}