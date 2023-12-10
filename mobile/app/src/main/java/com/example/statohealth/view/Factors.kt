package com.example.statohealth.view

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
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
import com.example.statohealth.R
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.viewmodel.FactorsViewModel

@Composable
fun Factors(
    factorsViewModel: FactorsViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    factorsViewModel.navController = navController

    LaunchedEffect(Unit) {
        factorsViewModel.getCategories(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Выберите фактор повлиявший на самочувствие")
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
                    ProgressIndicator(factorsViewModel.progressVisible)
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
                        if (factorsViewModel.choosenCategory.id == -1)
                            Column(
                                verticalArrangement = Arrangement.spacedBy(
                                    10.dp,
                                    Alignment.CenterVertically
                                )
                            ) {
                                factorsViewModel.categories.forEach { category ->
                                    Button(modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(horizontal = 25.dp), onClick = {
                                        factorsViewModel.choosenCategory = category
                                    })
                                    {
                                        Text(category.name, fontSize = 25.sp)
                                    }
                                }
                            }
                        else
                            Column(Modifier.selectableGroup()) {
                                factorsViewModel.choosenCategory.factors.forEach { subFactor ->
                                    Row(
                                        Modifier
                                            //.height(56.dp)
                                            .selectable(
                                                selected = (subFactor == factorsViewModel.choosenFactor),
                                                onClick = {
                                                    factorsViewModel.choosenFactor = subFactor
                                                },
                                                role = Role.RadioButton
                                            ),
                                        verticalAlignment = Alignment.CenterVertically
                                    )
                                    {
                                        RadioButton(
                                            selected = (subFactor == factorsViewModel.choosenFactor),
                                            onClick = null
                                        )
                                        Text(text = subFactor.name, fontSize = 22.sp)
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
                    Box(
                        modifier = if (!factorsViewModel.success) Modifier.fillMaxSize() else Modifier
                            .fillMaxSize()
                            .background(color = Color.Gray.copy(0.3f)), contentAlignment = Alignment.Center
                    )
                    {
                        if (factorsViewModel.success)
                            OkAnimation()
                    }
                }
            })
    }
}