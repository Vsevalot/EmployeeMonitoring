package com.example.statohealth.view

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material.icons.filled.PermIdentity
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
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.paint
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.statohealth.R
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.viewmodel.TimePickerViewModel

@Composable
fun TimePicker(
    timePickerViewModel: TimePickerViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    timePickerViewModel.navController = navController

    LaunchedEffect(Unit) {
        timePickerViewModel.getFeedbacks(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Выберите время")
                    },
                    navigationIcon = {
                        IconButton(onClick = { timePickerViewModel.exit(context) }) {
                            Icon(Icons.Filled.ExitToApp, "")
                        }
                    },
                    actions = {
                        IconButton(onClick = { timePickerViewModel.goToAccount() }) {
                            Icon(Icons.Filled.PermIdentity, "")
                        }
                    }
                )
            }, content = { padd ->
                padd
                Box(
                    modifier = with(Modifier) {
                        fillMaxSize()
                            .paint(
                                painterResource(id = R.drawable.urfu),
                                contentScale = ContentScale.FillHeight
                            )
                    })
                {
                    ProgressIndicator(timePickerViewModel.progressVisible)
                    Column(
                        modifier = Modifier
                            .fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(
                            20.dp,
                            Alignment.CenterVertically
                        ),
                    )
                    {
                        Button(enabled = timePickerViewModel.morningEnabled(), onClick = {
                            timePickerViewModel.morningClick()
                        })
                        {
                            Text("Утро", fontSize = 25.sp)
                        }
                        Button(enabled = timePickerViewModel.eveningEnabled(), onClick = {
                            timePickerViewModel.eveningClick()
                        })
                        {
                            Text("Вечер", fontSize = 25.sp)
                        }
                    }
                }
            })
    }
}