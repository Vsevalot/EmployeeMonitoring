package com.example.statohealth.view

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
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
import com.example.statohealth.viewmodel.RecommendationsViewModel

@Composable
fun Recommendations(
    recommendationsViewModel: RecommendationsViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    recommendationsViewModel.navController = navController

    LaunchedEffect(Unit) {
        recommendationsViewModel.getRecommendations(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Рекомендации")
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
                    ProgressIndicator(recommendationsViewModel.progressVisible)
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(top = padd.calculateTopPadding()),
                        horizontalAlignment = Alignment.CenterHorizontally
                    )
                    {
                        Text(
                            recommendationsViewModel.recommendationsText,
                            fontSize = 25.sp,
                            modifier = Modifier
                                .weight(0.9f)
                                .padding(32.dp)
                                .verticalScroll(rememberScrollState())
                        )
                    }
                }
            })
    }
}