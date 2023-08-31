package com.example.statohealth.infrastructure

import android.util.Log

class Logger {
    companion object {
        fun log(msg: String)
        {
            Log.d("MyLog", msg)
        }
        fun log(msg: String, tr: Throwable?)
        {
            Log.d("MyLog", msg, tr)
        }
    }
}