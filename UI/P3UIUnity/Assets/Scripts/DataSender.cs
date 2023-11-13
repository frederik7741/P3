using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System.Collections;
using TMPro;

[System.Serializable]
public class PatientData
{
    public int patient_id;
    public string date;
    public int repetitions;
}

[System.Serializable]
public class PatientButtonPair
{
    public Button button; // Assign the actual button from the inspector
    public int patientId; // Assign the patient ID manually in the inspector
}

public class DataSender : MonoBehaviour
{
    public TextMeshProUGUI[] dateButtons;
    public PatientButtonPair[] patientButtons;
    private int currentPatientId = -1; // Variable to store the current patient ID
    public string baseURL = "http://localhost:5000/save_data";

    void Start()
    {
        // Initialize buttons in the start method
        foreach (var pair in patientButtons)
        {
            pair.button.onClick.AddListener(delegate { OnPatientButtonClicked(pair.patientId); });
        }
    }

    public void OnPatientButtonClicked(int patientId)
    {
        if (currentPatientId != patientId)
        {
            currentPatientId = patientId; // Set the current patient ID
            ResetPatientUI(); // Clear the previous patient's data from the UI
            Debug.Log($"Patient button clicked. Patient ID: {currentPatientId}");
        }
        else
        {
            Debug.Log($"Patient ID {currentPatientId} is already selected.");
        }
    }

    private void ResetPatientUI()
    {
        // Clear or update the UI elements associated with patient data
        foreach (var dateButton in dateButtons)
        {
            dateButton.text = "No data"; // Reset the text of date buttons
        }
        // Additional UI reset logic can go here
    }

   public void OnExerciseCompleted()
{
    Debug.Log("clicked");
    if (currentPatientId > 0) // Note: This condition should be <= 0 based on your log message.
    {
        Debug.LogError("No patient selected.");
        return;
    }

    string date = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm"); // Current date and time
    int repetitions = 10; // Replace with actual repetitions of the exercise completed

    // Find the DateUIUpdater in the scene and queue the new date update.
    DateUIUpdater dateUpdater = FindObjectOfType<DateUIUpdater>();
    if (dateUpdater != null)
    {
        dateUpdater.QueueDateUpdate(date);
    }
    else
    {
        Debug.LogError("DateUIUpdater component not found in the scene!");
    }

    StartCoroutine(PostRequest(currentPatientId, date, repetitions)); // Send data to server
}


    IEnumerator PostRequest(int patientId, string date, int repetitions)
    {
        PatientData data = new PatientData
        {
            patient_id = patientId,
            date = date,
            repetitions = repetitions
        };

        string jsonData = JsonUtility.ToJson(data);
        using (UnityWebRequest www = new UnityWebRequest(baseURL, "POST"))
        {
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            www.uploadHandler = new UploadHandlerRaw(jsonToSend);
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
            }
            else
            {
                Debug.Log("Response: " + www.downloadHandler.text);
                // Update the UI to show the new date
                dateButtons[0].text = date; // Assuming the first button is the most recent
            }
        }
    }
}
