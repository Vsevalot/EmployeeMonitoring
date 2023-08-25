package com.example.statohealth.view

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import com.example.statohealth.data.SubFactorType
import com.example.statohealth.viewmodel.FactorsViewModel

@Composable
fun Factors(
    factorsViewModel: FactorsViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    factorsViewModel.navController = navController

    LaunchedEffect(Unit) {
        factorsViewModel.getFactors(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        ProgressIndicator(factorsViewModel.progressVisible)
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
            if (factorsViewModel.choosenFactor.id == -1)
                Column(
                    verticalArrangement = Arrangement.spacedBy(
                        10.dp,
                        Alignment.CenterVertically
                    )
                ) {
                    factorsViewModel.factors.forEach { factor ->
                        Button(modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 25.dp)
                            .height(56.dp), onClick = {
                            factorsViewModel.choosenFactor = factor
                        })
                        {
                            Text(factor.name, fontSize = 25.sp)
                        }
                    }
                }
            else
                Column(Modifier.selectableGroup(), horizontalAlignment = Alignment.CenterHorizontally) {
                    factorsViewModel.choosenFactor.factors.forEach { subFactor ->
                        Row(
                            Modifier
                                .fillMaxWidth()
                                .height(56.dp),
                            verticalAlignment = Alignment.CenterVertically
                        )
                        {
                            RadioButton(
                                selected = (subFactor == factorsViewModel.choosenSubFactor),
                                onClick = { factorsViewModel.choosenSubFactor = subFactor }
                            )
                            Text(text = subFactor.value, fontSize = 22.sp)
                        }
                        if (subFactor.type == SubFactorType.TEXT) {
                            OutlinedTextField(
                                value = factorsViewModel.subFactorText,
                                enabled = factorsViewModel.choosenSubFactor.type == SubFactorType.TEXT,
                                onValueChange = { newText ->
                                    factorsViewModel.subFactorText = newText
                                },
                                singleLine = true,
                                label = {
                                    Text(text = "Введите текст")
                                },
                                placeholder = {
                                    Text(text = "Введите текст")
                                })
                        }
                    }
                }
            Button(enabled = factorsViewModel.sendButtonEnabled(), onClick = {
                factorsViewModel.sendButtonClick(context)
            })
            {
                Text("Отправить", fontSize = 25.sp)
            }
        }
    }
}