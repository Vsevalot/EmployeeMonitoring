package com.example.statohealth.view

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.viewmodel.ManagerKeyViewModel

@Composable
fun ManagerKey(
    managerKeyViewModel: ManagerKeyViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    managerKeyViewModel.navController = navController
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Введите ключ")
                    }
                )
            }, content = { padd ->
                ProgressIndicator(managerKeyViewModel.progressVisible)
                Column(
                    verticalArrangement = Arrangement.spacedBy(
                        10.dp,
                        Alignment.CenterVertically
                    ),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .padding(bottom = 10.dp, top = padd.calculateTopPadding())
                        .fillMaxHeight()
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState())
                ) {
                    CapitalizedUserCredentials(
                        managerKeyViewModel.managerKey,
                        managerKeyViewModel::setManagerKeyProperty,
                        "Ключ"
                    )

                    Button(
                        enabled = managerKeyViewModel.isCorrectInput(),
                        onClick = { managerKeyViewModel.getManager(context) }) {
                        Text("Продолжить", fontSize = 25.sp)
                    }
                }
            })
    }
}