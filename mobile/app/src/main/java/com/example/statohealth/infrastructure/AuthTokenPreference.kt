package com.example.statohealth.infrastructure

import android.content.Context
import androidx.activity.ComponentActivity

class AuthTokenPreference {
    private val authTokenSharedPreferenceName: String = "AuthenticateToken"
    private val authTokenPreferenceName = "AuthenticateToken"

    fun getToken(context: Context): String? {
        val sharedPreference = context.getSharedPreferences(
            authTokenSharedPreferenceName,
            ComponentActivity.MODE_PRIVATE
        )
        return sharedPreference.getString(authTokenPreferenceName, null)
    }

    fun setToken(context: Context,token: String?) {
        val sharedPreference = context.getSharedPreferences(
            authTokenSharedPreferenceName,
            ComponentActivity.MODE_PRIVATE
        )
        sharedPreference.edit().putString(authTokenPreferenceName,token).apply()
    }

    fun removeToken(context: Context) {
        val sharedPreference = context.getSharedPreferences(
            authTokenSharedPreferenceName,
            ComponentActivity.MODE_PRIVATE
        )
        sharedPreference.edit().remove(authTokenPreferenceName).apply()
    }
}