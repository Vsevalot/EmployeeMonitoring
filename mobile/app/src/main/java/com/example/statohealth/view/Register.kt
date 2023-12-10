package com.example.statohealth.view

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.statohealth.Manager
import com.example.statohealth.R
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.infrastructure.MaskFormatter
import com.example.statohealth.viewmodel.RegisterViewModel

@Composable
fun Register(
    registerViewModel: RegisterViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    registerViewModel.navController = navController
    LaunchedEffect(Unit) {
        registerViewModel.manager = Manager.choosenManager
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(text = "Регистрация")
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
                    ProgressIndicator(registerViewModel.progressVisible)
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

                        Text("Руководитель:")
                        Text(
                            "${registerViewModel.manager.firstName + " " + registerViewModel.manager.lastName + " " + registerViewModel.manager.surname}",
                            maxLines = 2
                        )
                        UserCredentials(
                            registerViewModel.lastName,
                            registerViewModel::setLastNameProperty,
                            "Фамилия"
                        )
                        UserCredentials(
                            registerViewModel.firstName,
                            registerViewModel::setFirstNameProperty,
                            "Имя"
                        )
                        UserCredentials(
                            registerViewModel.surname,
                            registerViewModel::setSurnameProperty,
                            "Отчество"
                        )
                        OutlinedTextField(
                            value = registerViewModel.birthdate,
                            onValueChange = { newText ->
                                registerViewModel.setBirthdateProperty(newText.take("00.00.0000".count { it == '0' }))
                            },
                            singleLine = true,
                            placeholder = { Text(text = "01.01.2000") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            label = { Text(text = "Дата рождения") },
                            visualTransformation = MaskFormatter("00.00.0000", '0'),
                        )

                        UserCredentials(
                            registerViewModel.position,
                            registerViewModel::setPositionProperty,
                            "Должность"
                        )
                        UserPhoneCredentials(
                            registerViewModel.phone,
                            registerViewModel::setPhoneProperty,
                            "Номер телефона"
                        )
                        UserEmailCredentials(
                            registerViewModel.email,
                            registerViewModel::setEmailProperty,
                            "Email"
                        )
                        UserPasswordCredentials(
                            registerViewModel.password,
                            registerViewModel.passwordVisible,
                            registerViewModel::invertPasswordVisible,
                            registerViewModel::setPasswordProperty,
                            "Пароль"
                        )
                        UserPasswordCredentials(
                            registerViewModel.passwordRepeat,
                            registerViewModel.passwordRepeatVisible,
                            registerViewModel::invertPasswordRepeatVisible,
                            registerViewModel::setPasswordRepeatProperty,
                            "Введите пароль еще раз"
                        )
                        Row(
                            modifier = Modifier
                                .padding(horizontal = 30.dp)
                        ) {
                            Checkbox(
                                checked = registerViewModel.personalDataAgreement,
                                onCheckedChange = { newState ->
                                    registerViewModel.updatePersonalDataAgreement(
                                        newState
                                    )
                                }
                            )
                            Text("Согласен с правилами обработки персональных данных", maxLines = 2)
                        }
                        Button(
                            enabled = registerViewModel.isCorrectInput(),
                            onClick = { registerViewModel.register(context) }) {
                            Text("Зарегистрироваться", fontSize = 25.sp)
                        }
                    }
                    Box(
                        modifier = if (!registerViewModel.success) Modifier.fillMaxSize() else Modifier
                            .fillMaxSize()
                            .background(color = Color.Gray.copy(0.3f)), contentAlignment = Alignment.Center
                    )
                    {
                        if (registerViewModel.success)
                            OkAnimation()
                    }
                }
            })
    }
}