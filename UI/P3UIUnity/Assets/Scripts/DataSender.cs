using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;
using System.Collections;

// This class handles sending and receiving data to/from a server for patient exercises.
public class DataSender : MonoBehaviour
{
    // References to button pairs for each patient, the API endpoints, and UI elements.
    public PatientButtonPair[] patientButtons;
    public string getExerciseDataURL = "http://localhost:5000/get_exercise_data/";
    public string saveDataURL = "http://localhost:5000/save_data/";
    public DateUIUpdater dateUIUpdater;
    public int currentPatientId = -1; // Keeps track of the currently selected patient ID.
    public TMP_Text time; // Text component to display time, linked from the UI.

    // Serializable classes to hold the response data structure from the server.
    [System.Serializable]
    public class ExerciseDataWrapper { public ExerciseData[] exerciseData; }
    
    [System.Serializable]
    public class PatientButtonPair { public Button button; public int patientId; }

    // On start, assign a listener for the patient buttons.
    void Start()
    {
        foreach (var pair in patientButtons)
        {
            pair.button.onClick.AddListener(() => OnPatientButtonClicked(pair.patientId));
        }
    }

    // When a patient button is clicked, fetch the exercise data for that patient.
    public void OnPatientButtonClicked(int patientId)
    {
        currentPatientId = patientId;
        StartCoroutine(GetPatientExerciseData(patientId));
    }

    // Method called when an exercise is completed to send the data to the server.
    public void OnExerciseCompleted()
    {
        if (currentPatientId <= 0)
        {
            Debug.LogError("No patient selected.");
            return;
        }

        ExerciseData data = new ExerciseData
        {
            patient_id = currentPatientId,
            date = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm"),
            repetitions = 25 // The number of repetitions completed, should come from the exercise logic.
        };

        StartCoroutine(PostRequest(data)); // Send the exercise data to the server.
    }

    // Coroutine to post exercise data to the server.
    private IEnumerator PostRequest(ExerciseData data)
    {
        string jsonData = JsonUtility.ToJson(data);
        using (UnityWebRequest www = UnityWebRequest.Post(saveDataURL, "POST"))
        {
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest(); // Wait for the server response.

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Error: {www.error}");
            }
            else
            {
                Debug.Log($"Server response: {www.downloadHandler.text}");
            }
        }
    }

    // Coroutine to fetch exercise data from the server for a specific patient.
    private IEnumerator GetPatientExerciseData(int patientId)
    {
        using (UnityWebRequest www = UnityWebRequest.Get(getExerciseDataURL + patientId))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error Getting Exercise Data: " + www.error);
            }
            else
            {
                string jsonResponse = www.downloadHandler.text;
                Debug.Log($"Received JSON response: {jsonResponse}");

                ExerciseDataWrapper wrapper = JsonUtility.FromJson<ExerciseDataWrapper>("{\"exerciseData\":" + jsonResponse + "}");
                if (wrapper != null && wrapper.exerciseData != null)
                {
                    // Update the UI with the fetched data.
                    foreach (var exerciseData in wrapper.exerciseData)
                    {
                        dateUIUpdater.QueueExerciseData(exerciseData);
                    }
                    dateUIUpdater.UpdateDateButtons();
                }
                else
                {
                    Debug.LogError("Failed to parse exercise data.");
                }
            }
        }
    }

    // Method to update the displayed time when a UI slider is changed.
    public void OnTimeSliderChanged(Slider slider)
    {
        time.text = slider.value.ToString();
    }
}
