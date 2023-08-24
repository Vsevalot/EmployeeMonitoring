package com.example.statohealth.activities

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.statohealth.Pages
import com.example.statohealth.ui.theme.StatoHealthTheme
import com.example.statohealth.view.Account
import com.example.statohealth.view.EveningState
import com.example.statohealth.view.Factors
import com.example.statohealth.view.Instructions
import com.example.statohealth.view.Login
import com.example.statohealth.view.MorningState
import com.example.statohealth.view.Recommendations
import com.example.statohealth.view.Register
import com.example.statohealth.view.TimePicker
import com.example.statohealth.viewmodel.AccountViewModel
import com.example.statohealth.viewmodel.EveningStateViewModel
import com.example.statohealth.viewmodel.FactorsViewModel
import com.example.statohealth.viewmodel.InstructionsViewModel
import com.example.statohealth.viewmodel.LoginViewModel
import com.example.statohealth.viewmodel.MorningStateViewModel
import com.example.statohealth.viewmodel.RecommendationsViewModel
import com.example.statohealth.viewmodel.RegisterViewModel
import com.example.statohealth.viewmodel.TimePickerViewModel

class MainActivity : ComponentActivity() {
    private val loginViewModel: LoginViewModel by viewModels()
    private val registerViewModel: RegisterViewModel by viewModels()
    private val instructionsViewModel: InstructionsViewModel by viewModels()
    private val timePickerViewModel: TimePickerViewModel by viewModels()
    private val morningStateViewModel: MorningStateViewModel by viewModels()
    private val eveningStateViewModel: EveningStateViewModel by viewModels()
    private val factorsViewModel: FactorsViewModel by viewModels()
    private val accountViewModel: AccountViewModel by viewModels()
    private val recommendationsViewModel: RecommendationsViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val context = this
            val navController = rememberNavController()

            StatoHealthTheme {
                NavHost(navController = navController, startDestination = Pages.loginPage)
                {
                    composable(Pages.loginPage) {
                        Login(loginViewModel, navController, context)
                    }
                    composable(Pages.registerPage) {
                        Register (registerViewModel, navController, context)
                    }
                    composable(Pages.instructionsPage) {
                        Instructions (instructionsViewModel, navController, context)
                    }
                    composable(Pages.timePickerPage) {
                        TimePicker (timePickerViewModel, navController, context)
                    }
                    composable(Pages.morningStatePage) {
                        MorningState (morningStateViewModel, navController, context)
                    }
                    composable(Pages.eveningStatePage) {
                        EveningState (eveningStateViewModel, navController, context)
                    }
                    composable(Pages.factorsPage) {
                        Factors (factorsViewModel, navController, context)
                    }
                    composable(Pages.accountPage) {
                        Account (accountViewModel, navController, context)
                    }
                    composable(Pages.recommendationsPage) {
                        Recommendations (recommendationsViewModel, navController, context)
                    }
                }
            }
        }
    }
}