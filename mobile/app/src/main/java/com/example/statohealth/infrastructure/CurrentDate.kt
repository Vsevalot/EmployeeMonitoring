package com.example.statohealth.infrastructure

import java.util.Calendar

class CurrentDate {
    val now = Calendar.getInstance()
    val year = now.get(Calendar.YEAR)

    val month = now.get(Calendar.MONTH)+1
    val day = now.get(Calendar.DAY_OF_MONTH)

    val hour = now.get(Calendar.HOUR_OF_DAY)
    val minute = now.get(Calendar.MINUTE)
    val second = now.get(Calendar.SECOND)

    fun isMorning(): Boolean = hour in 7..11
    fun isEvening(): Boolean = hour in 16..20

    fun toStringDate(): String {
        var formattedMonth = if(month<10)
            "0$month"
        else
            month.toString()

        var formattedDay = if(day<10)
            "0$day"
        else
            day.toString()
        return "${year}-${formattedMonth}-${formattedDay}"
    }

    fun toStringDateRu(): String {
        var formattedMonth = if(month<10)
            "0$month"
        else
            month.toString()

        var formattedDay = if(day<10)
            "0$day"
        else
            day.toString()
        return "${formattedDay}.${formattedMonth}.${year}"
    }
}