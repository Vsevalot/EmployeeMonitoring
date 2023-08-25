package com.example.statohealth.view

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RadioButton
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
import com.example.statohealth.viewmodel.EveningStateViewModel

@Composable
fun EveningState(
    eveningStateViewModel: EveningStateViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    eveningStateViewModel.navController = navController

    LaunchedEffect(Unit) {
        eveningStateViewModel.getStates(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        ProgressIndicator(eveningStateViewModel.progressVisible)
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
            Column(Modifier.selectableGroup()) {
                eveningStateViewModel.states.forEach { state ->
                    Row( Modifier.fillMaxWidth().height(56.dp), verticalAlignment = Alignment.CenterVertically)
                    {
                        RadioButton(
                            selected = (state == eveningStateViewModel.choosenState),
                            onClick = { eveningStateViewModel.choosenState = state }
                        )
                        Text( text = state.name, fontSize = 22.sp )
                    }
                }
            }
            Button(enabled = eveningStateViewModel.sendButtonEnabled(),onClick = {
                eveningStateViewModel.sendButtonClick(context)
            })
            {
                Text("Отправить", fontSize = 25.sp)
            }
        }
    }
}