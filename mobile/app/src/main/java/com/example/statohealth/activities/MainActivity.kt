package com.example.statohealth.activities

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.statohealth.Instructions
import com.example.statohealth.Login
import com.example.statohealth.Pages
import com.example.statohealth.Register
import com.example.statohealth.ui.theme.StatoHealthTheme
import com.example.statohealth.view.model.InstructionsViewModel
import com.example.statohealth.view.model.LoginViewModel
import com.example.statohealth.view.model.RegisterViewModel

class MainActivity : ComponentActivity() {
    private val loginViewModel: LoginViewModel by viewModels()
    private val registerViewModel: RegisterViewModel by viewModels()
    private val instructionsViewModel: InstructionsViewModel by viewModels()

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
                }
            }
        }
    }
}