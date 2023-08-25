package com.example.statohealth.infrastructure

import java.util.Calendar

class CurrentDate {
    val now = Calendar.getInstance()
    val year = now.get(Calendar.YEAR)

    val month = now.get(Calendar.MONTH)
    val day = now.get(Calendar.DAY_OF_MONTH)

    val hour = now.get(Calendar.HOUR_OF_DAY)
    val minute = now.get(Calendar.MINUTE)
    val second = now.get(Calendar.SECOND)

    fun isMorning(): Boolean = hour in 6..11
    fun isEvening(): Boolean = hour in 18..24

}