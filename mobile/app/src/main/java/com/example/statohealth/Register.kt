package com.example.statohealth

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import com.example.statohealth.view.model.RegisterViewModel

@Composable
fun Register(
    registerViewModel: RegisterViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    registerViewModel.navController = navController
    LaunchedEffect(Unit) {
        registerViewModel.getManagers(context)
    }
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        ProgressIndicator(registerViewModel.progressVisible)
        Column(
            verticalArrangement = Arrangement.spacedBy(
                10.dp,
                Alignment.CenterVertically
            ),
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .padding(bottom = 40.dp)
                .fillMaxHeight()
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
        ) {
            UserCredentials(
                registerViewModel.firstName,
                registerViewModel::setFirstNameProperty,
                "Имя"
            )
            UserCredentials(
                registerViewModel.lastName,
                registerViewModel::setLastNameProperty,
                "Фамилия"
            )
            UserCredentials(
                registerViewModel.surname,
                registerViewModel::setSurnameProperty,
                "Отчество"
            )
            UserCredentials(
                registerViewModel.birthdate,
                registerViewModel::setBirthdateProperty,
                "Дата рождения"
            )
            //manager
            ExposedDropdownMenuBox(
                expanded = registerViewModel.expanded,
                onExpandedChange = { registerViewModel.expanded = !registerViewModel.expanded }
            ) {
                OutlinedTextField(
                    value = registerViewModel.choosenManager.firstName,
                    onValueChange = {},
                    singleLine = true,
                    readOnly = true,
                    label = {Text(text = "Руководитель")},
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = registerViewModel.expanded) },
                    modifier = Modifier.menuAnchor()
                )

                ExposedDropdownMenu(
                    expanded = registerViewModel.expanded,
                    onDismissRequest = { registerViewModel.expanded = false }
                ) {
                    registerViewModel.managers.forEach { manager ->
                        DropdownMenuItem(
                            text = {
                                Text(text = manager.firstName)
                            },
                            onClick = {
                                registerViewModel.choosenManager = manager
                                registerViewModel.expanded = false
                            }
                        )
                    }
                }
            }

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
            Button(
                enabled = registerViewModel.isCorrectInput(),
                onClick = { registerViewModel.register(context) }) {
                Text("Зарегистрироваться", fontSize = 25.sp)
            }
        }
    }
}