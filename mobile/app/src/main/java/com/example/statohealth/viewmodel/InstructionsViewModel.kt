package com.example.statohealth.viewmodel

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.navigation.NavHostController
import com.example.statohealth.Pages


class InstructionsViewModel : ViewModel() {
    var instructionsText by mutableStateOf("")
    var progressVisible by mutableStateOf(false)
    lateinit var navController: NavHostController

    fun updateProgressVisibility(state: Boolean) {
        progressVisible = state
    }

    fun getInstructions(context: Context) {
        instructionsText = "Данный опрос необходимо проходить 2 раза в день: утром и вечером.\n" +
                "Для оценки своего самочувствия необходимо выбрать один из вариант ответа:\n" +
                "1.\tчувствую себя хорошо\n" +
                "2.\tчто-то не очень, но жить можно \n" +
                "3.\tчувствую себя плохо, сил совсем нет\n" +
                "В случае ухудшения самочувствия в конце рабочего дня дополнительно необходимо выбрать из перечня фактор, который стал причиной этого ухудшения:\n" +
                "1) начальство\n" +
                "2) коллеги\n" +
                "3) условия работы\n" +
                "4) личные факторы и здоровье\n" +
                "Нажмите \"Начать\", чтобы перейти к опросу."
    }

    fun start() {
        navController.navigate(Pages.loginPage)
    }

}