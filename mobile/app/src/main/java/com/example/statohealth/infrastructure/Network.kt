package com.example.statohealth.infrastructure

import android.content.Context
import android.util.Log
import com.android.volley.NetworkResponse
import com.android.volley.ParseError
import com.android.volley.Response
import com.android.volley.toolbox.HttpHeaderParser
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.google.gson.Gson
import org.json.JSONObject
import java.io.UnsupportedEncodingException


class Network(context: Context) {
    private val apiUrl: String = "http://159.223.224.135:8000"
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
        crossinline successResponseAction: (T?) -> Unit,
        useAuth: Boolean = true
    ) {
        updateProgress(true)

        val jsonObject = JSONObject(Gson().toJson(data))
        val request = object : JsonObjectRequest(
            Method.POST, getUrl(endpoint), jsonObject,
            { responseJson ->
                var response: T? = null
                if(responseJson != null)
                {
                updateProgress(false)
                    response =
                    Gson().fromJson(responseJson.toString(), T::class.java)
                }
                successResponseAction(response)
            }, {
                Log.d("MyLog", "VolleyError: $it")
                updateProgress(false)
            }) {

            override fun parseNetworkResponse(response: NetworkResponse): Response<JSONObject?>? {
                return try {
                    val json = String(
                        response.data
                    )
                    if (json.isEmpty()) {
                        Response.success(
                            null,
                            HttpHeaderParser.parseCacheHeaders(response)
                        )
                    } else {
                        Response.success(
                            JSONObject(json),
                            HttpHeaderParser.parseCacheHeaders(response))
                    }
                } catch (e: UnsupportedEncodingException) {
                    Response.error(ParseError(e))
                }
            }

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