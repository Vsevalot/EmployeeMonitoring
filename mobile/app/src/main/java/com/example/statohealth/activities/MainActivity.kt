package com.example.statohealth.activities

import android.Manifest
import android.app.AlertDialog
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.WindowManager
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.core.content.ContextCompat
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.statohealth.Pages
import com.example.statohealth.R
import com.example.statohealth.infrastructure.AuthTokenPreference
import com.example.statohealth.infrastructure.Logger
import com.example.statohealth.infrastructure.Network
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
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.messaging.FirebaseMessaging

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
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission(),
    ) { isGranted: Boolean ->
        if (isGranted) {
            getToken()
        } else {
            AlertDialog.Builder(this)
                .setTitle("Предупреждение")
                .setMessage("Вы не разрешили доступ к уведомлениям. Вы не будете получать уведомления.")
                .setPositiveButton("Ок") { _, _ -> }
                .show()
        }
    }

    private fun askNotificationPermission() {
        // This is only necessary for API level >= 33 (TIRAMISU)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) ==
                PackageManager.PERMISSION_GRANTED
            ) {
                getToken()
                // FCM SDK (and your app) can post notifications.
            } else if (shouldShowRequestPermissionRationale(Manifest.permission.POST_NOTIFICATIONS)) {
                // TODO: display an educational UI explaining to the user the features that will be enabled
                //       by them granting the POST_NOTIFICATION permission. This UI should provide the user
                //       "OK" and "No thanks" buttons. If the user selects "OK," directly request the permission.
                //       If the user selects "No thanks," allow the user to continue without notifications.
            } else {
                // Directly ask for the permission
                requestPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
    }

    private fun getToken() {
        FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
            if (!task.isSuccessful) {
                Logger.log("Fetching FCM registration token failed", task.exception)
                return@OnCompleteListener
            }

            // Get new FCM registration token
            val token = task.result

            // Log and toast
            Logger.log(token)
            var android_id = Settings.Secure.getString(this.contentResolver, Settings.Secure.ANDROID_ID)
            Toast.makeText(this, token, Toast.LENGTH_LONG).show()
        })
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        askNotificationPermission()
        if(Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU)
            getToken()
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
        setContent {
            val context = this
            val navController = rememberNavController()
            val savedAuthToken = AuthTokenPreference().getToken(context)
            val startDestination: String = if (savedAuthToken == null)
                Pages.loginPage
            else {
                Network.authorizationToken = savedAuthToken
                Pages.timePickerPage
            }
            StatoHealthTheme {
                NavHost(navController = navController, startDestination = startDestination)
                {
                    composable(Pages.loginPage) {
                        Login(loginViewModel, navController, context)
                    }
                    composable(Pages.registerPage) {
                        Register(registerViewModel, navController, context)
                    }
                    composable(Pages.instructionsPage) {
                        Instructions(instructionsViewModel, navController, context)
                    }
                    composable(Pages.timePickerPage) {
                        TimePicker(timePickerViewModel, navController, context)
                    }
                    composable(Pages.morningStatePage) {
                        MorningState(morningStateViewModel, navController, context)
                    }
                    composable(Pages.eveningStatePage) {
                        EveningState(eveningStateViewModel, navController, context)
                    }
                    composable(Pages.factorsPage) {
                        Factors(factorsViewModel, navController, context)
                    }
                    composable(Pages.accountPage) {
                        Account(accountViewModel, navController, context)
                    }
                    composable(Pages.recommendationsPage) {
                        Recommendations(recommendationsViewModel, navController, context)
                    }
                }
            }
        }
    }
}