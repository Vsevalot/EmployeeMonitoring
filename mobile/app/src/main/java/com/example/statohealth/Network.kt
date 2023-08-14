package com.example.statohealth

import android.content.Context
import android.util.Log
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.google.gson.Gson
import org.json.JSONObject

class Network(context: Context) {
    private val apiUrl: String = "https://51397027-267d-4734-a017-e4e00774c2bd.mock.pstmn.io"
    private val apiVersion: String = "/api/v1/"

    companion object {
        var authorizationToken: String? = null
    }

    val queue = Volley.newRequestQueue(context)

    inline fun <reified T : Any> sendGetRequest(
        endpoint: String,
        crossinline updateProgress: (Boolean) -> Unit,
        crossinline successResponseAction: (T) -> Unit,
        useAuth: Boolean = true
    ) {
        updateProgress(true)

        val request = object : JsonObjectRequest(
            Method.GET, getUrl(endpoint), null,
            { responseJson ->
                updateProgress(false)
                val response =
                    Gson().fromJson(responseJson.toString(), T::class.java)
                successResponseAction(response)
            }, {
                Log.d("MyLog", "VolleyError: $it")
                updateProgress(false)
            }) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                if (useAuth)
                    headers["authorization"] = "$authorizationToken"
                return headers
            }
        }
        queue.add(request)
    }

    inline fun <reified T : Any> sendPostRequest(
        endpoint: String,
        data: Any,
        crossinline updateProgress: (Boolean) -> Unit,
        crossinline successResponseAction: (T) -> Unit,
        useAuth: Boolean = true
    ) {
        updateProgress(true)

        val jsonObject = JSONObject(Gson().toJson(data))
        val request = object : JsonObjectRequest(
            Method.POST, getUrl(endpoint), jsonObject,
            { responseJson ->
                updateProgress(false)
                val response =
                    Gson().fromJson(responseJson.toString(), T::class.java)
                successResponseAction(response)
            }, {
                Log.d("MyLog", "VolleyError: $it")
                updateProgress(false)
            }) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                if (useAuth)
                    headers["authorization"] = "$authorizationToken"
                return headers
            }
        }
        queue.add(request)
    }

    fun getUrl(endpoint: String): String = apiUrl + apiVersion + endpoint
}