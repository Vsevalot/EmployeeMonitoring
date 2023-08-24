package com.example.statohealth.view

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.viewmodel.AccountViewModel

@Composable
fun Account(
    accountViewModel: AccountViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    accountViewModel.navController = navController

    LaunchedEffect(Unit) {
        accountViewModel.getMe(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        ProgressIndicator(accountViewModel.progressVisible)
        Column(
            modifier = Modifier
                .fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally
        )
        {
            Text(
                accountViewModel.meText, fontSize = 25.sp, modifier = Modifier
                    .weight(0.9f)
                    .padding(32.dp)
                    .verticalScroll(rememberScrollState())
            )
            Box(modifier = Modifier.weight(0.1f) ,contentAlignment = Alignment.Center)
            {

                Button(onClick = {
                    accountViewModel.getRecommendationsClick()
                })
                {
                    Text("Получить рекомендации", fontSize = 25.sp)
                }
            }
        }
    }
}