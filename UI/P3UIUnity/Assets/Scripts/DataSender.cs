using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic; // Add this line
using TMPro;

[System.Serializable]
public class PatientData
{
    public int patient_id;
    public string date;
    public int repetitions;
}

public class DataSender : MonoBehaviour
{

// Assuming you have a reference to your TextMeshPro buttons
public TextMeshProUGUI[] dateButtons;

public void OnExerciseCompleted() // Call this method when an exercise is completed
{
    int patientId = 123; // Replace with actual patient ID
    int repetitions = 10; // Replace with actual repetitions of the exercise completed
    
    DateUIUpdater dateUpdater = FindObjectOfType<DateUIUpdater>();
    if (dateUpdater != null)
    {
        string date = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm"); // Current date and time
        dateUpdater.QueueDateUpdate(date); // Queue the new date for updating
    }
    else
    {
        Debug.LogError("DateUIUpdater component not found in the scene!");
    }
}

private void UpdateDateButtons(string newDate)
{
    if (dateButtons.Length == 1)
    {
        // If there's only one button, just set its text to the new date
        dateButtons[0].text = newDate;
        return;
    }

    // If there's more than one button, shift the dates down and add the new date at the top
    for (int i = dateButtons.Length - 1; i > 0; i--)
    {
        dateButtons[i].text = dateButtons[i - 1].text; // Move the text down one button
    }
    dateButtons[0].text = newDate; // Set the latest date to the first button
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
