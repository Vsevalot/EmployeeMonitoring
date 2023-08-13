package com.example.statohealth

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
import com.example.statohealth.view.model.InstructionsViewModel

@Composable
fun Instructions(
    instructionsViewModel: InstructionsViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    instructionsViewModel.navController = navController

    LaunchedEffect(Unit) {
        instructionsViewModel.getInstructions(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        ProgressIndicator(instructionsViewModel.progressVisible)
        Column(
            modifier = Modifier
                .fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally
        )
        {
            Text(
                instructionsViewModel.instructionsText, fontSize = 25.sp, modifier = Modifier
                    .weight(0.9f)
                    .padding(32.dp)
                    .verticalScroll(rememberScrollState())
            )
            Box(modifier = Modifier.weight(0.1f) ,contentAlignment = Alignment.Center)
            {

                Button(onClick = {
                    instructionsViewModel.start()
                })
                {
                    Text("Старт", fontSize = 25.sp)
                }
            }
        }
    }
}