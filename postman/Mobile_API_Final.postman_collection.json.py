{
  "info": { "name": "Mobile Backend - Complete", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "variable": [
    {"key": "BASE_URL", "value": "http://127.0.0.1:8000"},
    {"key": "ACCESS_TOKEN", "value": ""},
    {"key": "REFRESH_TOKEN", "value": ""}
  ],
  "item": [
    {
      "name": "Authentication",
      "item": [
        {"name": "Register", "request": {"method": "POST", "url": "{{BASE_URL}}/api/v1/auth/register/", "body": {"mode": "raw", "raw": "{\"username\":\"testuser\",\"email\":\"test@test.com\",\"password\":\"Test@123\"}", "options": {"raw": {"language": "json"}}}}},
        {"name": "Login", "request": {"method": "POST", "url": "{{BASE_URL}}/api/v1/auth/login/", "body": {"mode": "raw", "raw": "{\"username\":\"testuser\",\"password\":\"Test@123\"}"}}},
        {"name": "Refresh Token", "request": {"method": "POST", "url": "{{BASE_URL}}/api/v1/auth/refresh/", "body": {"mode": "raw", "raw": "{\"refresh\":\"{{REFRESH_TOKEN}}\"}"}}}
      ]
    },
    {
      "name": "Profile Image",
      "item": [
        {"name": "Upload Profile Image", "request": {"method": "POST", "header": [{"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}], "url": "{{BASE_URL}}/api/v1/profile/image/", "body": {"mode": "formdata", "formdata": [{"key": "image", "type": "file", "src": []}]}}}
      ]
    },
    {
      "name": "Service Images",
      "item": [
        {"name": "Upload Service Image", "request": {"method": "POST", "header": [{"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}], "url": "{{BASE_URL}}/api/v1/rides/services/1/images/", "body": {"mode": "formdata", "formdata": [{"key": "image", "type": "file", "src": []}]}}},
        {"name": "Get Service Images", "request": {"method": "GET", "header": [{"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}], "url": "{{BASE_URL}}/api/v1/rides/services/1/images/"}},
        {"name": "Delete Service Image", "request": {"method": "DELETE", "header": [{"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}], "url": "{{BASE_URL}}/api/v1/rides/services/1/images/1/"}}
      ]
    }
  ]
}