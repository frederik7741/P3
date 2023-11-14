using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System.Collections;
using TMPro;

[System.Serializable]
public class ExerciseData
{
    public string date;
    public int repetitions;
}

[System.Serializable]
public class PatientData
{
    public int patient_id;
    public string date;
    public int repetitions;
}


[System.Serializable]
public class ExerciseDataWrapper
{
    public ExerciseData[] exerciseData;
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
    public string getExerciseDataURL = "http://localhost:5000/get_exercise_data/";
	public string saveDataURL = "http://localhost:5000/save_data/";

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

        currentPatientId = patientId;
        ResetPatientUI(); // Reset the UI elements for the new patient
        StartCoroutine(GetPatientExerciseData(patientId)); // Fetch the new patient's exercise data
      
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
    
    if (currentPatientId <= 0) // Check if no patient is selected
    {
        Debug.LogError("No patient selected.");
        return;
    }

    string date = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm"); // Current date and time
    int repetitions = 10; // Replace with actual repetitions of the exercise completed
    DateUIUpdater dateUpdater = FindObjectOfType<DateUIUpdater>();
    
    
    if (dateUpdater != null)
    {
        Debug.Log($"currentPatientId: {currentPatientId}");
        Debug.Log($"date: {date}");
        Debug.Log($"repetitions: {repetitions}");

        dateUpdater.QueueDateUpdate(date);
        Debug.Log($"QueueDateUpdate called with date: {date}");
    }
    else
    {
        Debug.LogError("DateUIUpdater component not found in the scene!");
    }

    StartCoroutine(PostRequest(currentPatientId, date, repetitions)); // Send data to the server
}
 

 private IEnumerator PostRequest(int patientId, string date, int repetitions)
 {
     PatientData data = new PatientData
     {
         patient_id = patientId,
         date = date,
         repetitions = repetitions
     };

     string jsonData = JsonUtility.ToJson(data);
     Debug.Log($"Sending JSON to server: {jsonData}");

     using (UnityWebRequest www = UnityWebRequest.Post(saveDataURL, "POST"))
     {
         byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
         www.uploadHandler = new UploadHandlerRaw(jsonToSend);
         www.downloadHandler = new DownloadHandlerBuffer();
         www.SetRequestHeader("Content-Type", "application/json");

         Debug.Log($"Sending POST request to URL: {saveDataURL}");
         yield return www.SendWebRequest();

         if (www.result != UnityWebRequest.Result.Success)
         {
             Debug.LogError($"Error: {www.error}");
             Debug.LogError($"Status Code: {www.responseCode}");
         }
         else
         {
             Debug.Log($"Server response: {www.downloadHandler.text}");
         }
     }
 }


 private IEnumerator GetPatientExerciseData(int patientId)
 {
     using (UnityWebRequest www = UnityWebRequest.Get(getExerciseDataURL + patientId.ToString()))
     {
         yield return www.SendWebRequest();

         if (www.result != UnityWebRequest.Result.Success)
         {
             Debug.LogError("Error Getting Exercise Data: " + www.error);
         }
         else
         {
             string jsonResponse = www.downloadHandler.text;
             Debug.Log("Received JSON response: " + jsonResponse);

             // The JSON array should be wrapped in an object with a key "exerciseData" on the server side.
             // If that is not the case, you'll need to adjust the server response or adjust the JSON here as follows:
             string adjustedJson = "{\"exerciseData\":" + jsonResponse + "}";

             ExerciseDataWrapper wrapper = JsonUtility.FromJson<ExerciseDataWrapper>(adjustedJson);
             if (wrapper != null && wrapper.exerciseData != null)
             {
                 // Enqueue each date for processing.
                 foreach (var data in wrapper.exerciseData)
                 {
                     DateUIUpdater dateUpdater = FindObjectOfType<DateUIUpdater>();
                     if (dateUpdater != null)
                     {
                         dateUpdater.QueueDateUpdate(data.date);
                     }
                 }
             }
             else
             {
                 Debug.LogError("Failed to parse exercise data.");
             }
         }
     }
 }






public TMP_Text time;
    public void OnTimeSliderChanged(Slider slider)
    {
        time.text = slider.value.ToString();
    }
}
