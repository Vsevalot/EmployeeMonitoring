package com.example.statohealth.view

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.example.statohealth.R
import com.example.statohealth.activities.MainActivity
import com.example.statohealth.viewmodel.LoginViewModel

@Composable
fun Login(
    loginViewModel: LoginViewModel,
    navController: NavHostController,
    context: MainActivity
) {
    loginViewModel.navController = navController
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Scaffold(
            content = { padd ->
                ProgressIndicator(loginViewModel.progressVisible)
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(top = padd.calculateTopPadding() + 20.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                )
                {
                    Image(painter = painterResource(R.drawable.urfulogo_full_russian), contentDescription = "urfu_logo")
                    UserInputLayer(loginViewModel)
                    ButtonsLayer(loginViewModel, context)
                }
            })
    }
}

@Composable
fun ButtonsLayer(
    loginViewModel: LoginViewModel,
    context: MainActivity
) {
    Column(
        verticalArrangement = Arrangement.spacedBy(
            10.dp,
            Alignment.CenterVertically
        ),
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .fillMaxHeight()
            .fillMaxWidth()
    ) {
        Button(onClick = {
            loginViewModel.login(context)
        })
        {
            Text("Войти", fontSize = 25.sp)
        }
        Button(onClick = {
            loginViewModel.register()
        })
        {
            Text("Регистрация", fontSize = 25.sp)
        }
    }
}

@Composable
fun UserInputLayer(loginViewModel: LoginViewModel) {
    Column(
        verticalArrangement = Arrangement.spacedBy(
            10.dp,
            Alignment.CenterVertically
        ),
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .fillMaxHeight(0.5f)
            .fillMaxWidth()
    ) {
        UserEmailCredentials(loginViewModel.email, loginViewModel::setLoginProperty, "Email")
        UserPasswordCredentials(
            loginViewModel.password,
            loginViewModel.passwordVisible,
            loginViewModel::invertPasswordVisible,
            loginViewModel::setPasswordProperty,
            "Пароль"
        )
    }
}

@Composable
fun ProgressIndicator(visible: Boolean) {
    Box(
        modifier = if (!visible) Modifier.fillMaxSize() else Modifier
            .fillMaxSize()
        //.background(color = Color.Gray.copy(0.3f)),
        , contentAlignment = Alignment.Center
    ) {
        if (visible)
            CircularProgressIndicator()
    }
}

@Composable
fun CapitalizedUserCredentials(
    name: String,
    setPropertyAction: (String) -> Unit,
    placeholder: String
) {
    OutlinedTextField(
        keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Characters),
        value = name,
        onValueChange = { newText -> setPropertyAction(newText) },
        singleLine = true,
        label = {
            Text(text = placeholder)
        },
        placeholder = {
            Text(text = placeholder)
        })
}

@Composable
fun UserCredentials(
    name: String,
    setPropertyAction: (String) -> Unit,
    placeholder: String
) {
    OutlinedTextField(
        value = name,
        onValueChange = { newText -> setPropertyAction(newText) },
        singleLine = true,
        label = {
            Text(text = placeholder)
        },
        placeholder = {
            Text(text = placeholder)
        })
}

@Composable
fun UserPhoneCredentials(
    name: String,
    setPropertyAction: (String) -> Unit,
    placeholder: String
) {
    OutlinedTextField(
        value = name,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
        onValueChange = { newText -> setPropertyAction(newText) },
        singleLine = true,
        label = {
            Text(text = placeholder)
        },
        placeholder = {
            Text(text = placeholder)
        })
}

@Composable
fun UserEmailCredentials(
    name: String,
    setPropertyAction: (String) -> Unit,
    placeholder: String
) {
    OutlinedTextField(
        value = name,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
        onValueChange = { newText -> setPropertyAction(newText) },
        singleLine = true,
        label = {
            Text(text = placeholder)
        },
        placeholder = {
            Text(text = placeholder)
        })
}

@Composable
fun UserPasswordCredentials(
    name: String,
    passwordVisible: Boolean,
    invertPasswordVisibility: () -> Unit,
    setPropertyAction: (String) -> Unit,
    placeholder: String
) {
    OutlinedTextField(
        value = name,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
        visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
        onValueChange = { newText -> setPropertyAction(newText) },
        singleLine = true,
        label = {
            Text(text = placeholder)
        },
        placeholder = {
            Text(text = placeholder)
        },
        trailingIcon = {
            val image = if (passwordVisible)
                Icons.Filled.Visibility
            else Icons.Filled.VisibilityOff
            val description = if (passwordVisible) "Hide password" else "Show password"

            IconButton(onClick = invertPasswordVisibility) {
                Icon(imageVector = image, description)
            }
        }
    )
}