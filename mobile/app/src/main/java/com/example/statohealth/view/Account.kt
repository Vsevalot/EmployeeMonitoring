package com.example.statohealth.view

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckBox
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material.icons.filled.IndeterminateCheckBox
import androidx.compose.material.icons.filled.IntegrationInstructions
import androidx.compose.material.icons.filled.Nightlight
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion.Start
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.statohealth.Feedbacks
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
        accountViewModel.getFeedbacks(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Личный кабинет")
                    },
                    actions = {
                        IconButton(onClick = { accountViewModel.navigateToInstructions() }) {
                            Icon(Icons.Filled.IntegrationInstructions, "")
                        }
                    },
                    navigationIcon = {
                        IconButton(onClick = { accountViewModel.exit(context) }) {
                            Icon(Icons.Filled.ExitToApp, "")
                        }
                    }
                )
            }, content = { padd ->
                ProgressIndicator(accountViewModel.progressVisible)
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(top = padd.calculateTopPadding()),
                    horizontalAlignment = Alignment.CenterHorizontally
                )
                {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .weight(0.9f),
                        horizontalAlignment = Alignment.CenterHorizontally
                    )
                    {
                        Text(
                            "Состояние на сегодня (${accountViewModel.currentDay.toStringDateRu()}):", fontSize = 25.sp, modifier = Modifier.padding(top = 20.dp, start = 10.dp, end = 10.dp).align(Start)
                        )
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.align(Start).padding(start = 20.dp)) {
                            Icon(Icons.Filled.WbSunny, "", tint = Color.Yellow)
                            if (Feedbacks.morning != null) {
                                Text(
                                    "Пройдено", fontSize = 22.sp, modifier = Modifier
                                )
                                Icon(Icons.Filled.CheckBox, "", tint = Color.Green)
                            } else {
                                Text(
                                    "Не пройдено", fontSize = 22.sp, modifier = Modifier
                                )
                                Icon(Icons.Filled.IndeterminateCheckBox, "", tint = Color.Red)
                            }
                        }
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.align(Start).padding(start = 20.dp)) {
                            Icon(Icons.Filled.Nightlight, "", tint = Color.Blue)
                            if (Feedbacks.evening != null) {
                                Text(
                                    "Пройдено", fontSize = 22.sp, modifier = Modifier
                                )
                                Icon(Icons.Filled.CheckBox, "", tint = Color.Green)
                            } else {
                                Text(
                                    "Не пройдено", fontSize = 22.sp, modifier = Modifier
                                )
                                Icon(Icons.Filled.IndeterminateCheckBox, "", tint = Color.Red)
                            }
                        }
                    }
                    Box(modifier = Modifier.weight(0.1f), contentAlignment = Alignment.Center)
                    {
                        Button(onClick = {
                            accountViewModel.getRecommendationsClick()
                        })
                        {
                            Text("Получить рекомендации", fontSize = 25.sp)
                        }
                    }
                }
            })
    }
}