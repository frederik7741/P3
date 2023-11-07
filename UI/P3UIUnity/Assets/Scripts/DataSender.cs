using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic; // For Dictionary
using TMPro; // Add this line for TextMeshPro

[System.Serializable]
public class PatientData
{
    public int patient_id;
    public string date;
    public int repetitions;
}

public class DataSender : MonoBehaviour
{


public void OnExerciseCompleted() // Call this method when an exercise is completed
{

    int patientId = 123; // Replace with actual patient ID
    string date = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm");; // Current date
    int repetitions = 10; // Replace with actual repetitions of the exercise completed
    
    // Optionally, send the data to the server to save it
    StartCoroutine(PostRequest(patientId, date, repetitions)); // Start the coroutine to send data

 DateUIUpdater dateUpdater = FindObjectOfType<DateUIUpdater>();
        if (dateUpdater != null)
        {
            dateUpdater.UpdateDateButtons();
        }
        else
        {
            Debug.LogError("DateUIUpdater component not found in the scene!");
        }
}


    string baseURL = "http://localhost:5000/save_data"; // Use the IP address of your server here if not running locally

    public void OnButtonClick() // This method will be visible in the inspector
    {
        int patientId = 123; // Replace with actual patient ID
        string date = System.DateTime.Now.ToString("yyyy-MM-dd");
        int repetitions = 10; // Replace with actual repetitions
        StartCoroutine(PostRequest(patientId, date, repetitions)); // Start the coroutine to send data
    }

   IEnumerator PostRequest(int patientId, string date, int repetitions)
{
    PatientData data = new PatientData
    {
        patient_id = patientId,
        date = date,
        repetitions = repetitions
    };

    // Convert the object to JSON
    string jsonData = JsonUtility.ToJson(data);

        // Create a new UnityWebRequest, setting the URL and method (POST)
        using (UnityWebRequest www = new UnityWebRequest(baseURL, "POST"))
        {
            // Convert the JSON string to a byte array
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

            // Set the content type header to 'application/json'
            www.SetRequestHeader("Content-Type", "application/json");

            // Send the request and wait for a response
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
            }
            else
            {
                Debug.Log("Response: " + www.downloadHandler.text);
            }
        }
    }
}
