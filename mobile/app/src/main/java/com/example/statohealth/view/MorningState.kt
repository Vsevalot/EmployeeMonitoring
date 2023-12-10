package com.example.statohealth.view

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.paint
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.animateLottieCompositionAsState
import com.airbnb.lottie.compose.rememberLottieComposition
import com.example.statohealth.R
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.viewmodel.MorningStateViewModel


@Composable
fun OkAnimation() {
    val composition by rememberLottieComposition(LottieCompositionSpec.RawRes(R.raw.ok_blue2))
    val progress by animateLottieCompositionAsState(composition)
    LottieAnimation(
        composition = composition,
        progress = { progress },
    )
}

@Composable
fun MorningState(
    morningStateViewModel: MorningStateViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    morningStateViewModel.navController = navController

    LaunchedEffect(Unit) {
        morningStateViewModel.getStates(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Выберите утреннее самочувствие")
                    }
                )
            }, content = { padd ->
                Box(
                    modifier = with(Modifier) {
                        fillMaxSize()
                            .paint(
                                painterResource(id = R.drawable.urfu),
                                contentScale = ContentScale.FillHeight
                            )
                    })
                {
                    ProgressIndicator(morningStateViewModel.progressVisible)
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(top = padd.calculateTopPadding()),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(
                            20.dp,
                            Alignment.CenterVertically
                        ),
                    )
                    {
                        Column(Modifier.selectableGroup()) {
                            morningStateViewModel.states.forEach { state ->
                                Row(
                                    Modifier
                                        .height(56.dp)
                                        .selectable(
                                            selected = (state == morningStateViewModel.choosenState),
                                            onClick = {
                                                morningStateViewModel.choosenState = state
                                            },
                                            role = Role.RadioButton
                                        ), verticalAlignment = Alignment.CenterVertically
                                )
                                {
                                    RadioButton(
                                        selected = (state == morningStateViewModel.choosenState),
                                        onClick = null
                                    )
                                    Text(text = state.name, fontSize = 22.sp)
                                }
                            }
                        }
                        Button(enabled = morningStateViewModel.sendButtonEnabled(), onClick = {
                            morningStateViewModel.sendButtonClick(context)
                        })
                        {
                            Text("Отправить", fontSize = 25.sp)
                        }
                    }
                    Box(
                        modifier = if (!morningStateViewModel.success) Modifier.fillMaxSize() else Modifier
                            .fillMaxSize()
                            .background(color = Color.Gray.copy(0.3f)), contentAlignment = Alignment.Center
                    )
                    {
                        if (morningStateViewModel.success)
                            OkAnimation()
                    }
                }
            })
    }
}