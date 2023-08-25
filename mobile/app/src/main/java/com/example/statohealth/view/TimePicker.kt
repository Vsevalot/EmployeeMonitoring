package com.example.statohealth.view

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
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
            Button(enabled = timePickerViewModel.eveningEnabled(),onClick = {
                timePickerViewModel.eveningClick()
            })
            {
                Text("Вечер", fontSize = 25.sp)
            }
        }
    }
}