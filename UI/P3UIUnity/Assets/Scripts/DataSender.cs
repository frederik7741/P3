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
    public TextMeshProUGUI exerciseDurationText;
    public GameObject overlayPanel; // Assign this in the inspector
    public TextMeshProUGUI countdownText;
    
    // Serializable classes to hold the response data structure from the server.
    [System.Serializable]
    public class ExerciseDataWrapper { public ExerciseData[] exerciseData; }
    
    [System.Serializable]
    public class PatientButtonPair { public Button button; public int patientId; }
    
    [System.Serializable]
    public class exerciseData
    {
        public int patient_id;
        public string date;
        public int repetitions;
        public int time; 
    }



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
        dateUIUpdater.ClearScrollView(); // Clear the scroll view before fetching new data
        StartCoroutine(GetPatientExerciseData(patientId));
    }



    public void StartExerciseRoutine()
    {
        if (currentPatientId <= 0)
        {
            Debug.LogError("No patient selected.");
            return;
        }

        if (int.TryParse(exerciseDurationText.text, out int exerciseTime))
        {
            exerciseData data = new exerciseData
            {
                patient_id = currentPatientId,
                date = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm"),
                time = exerciseTime
            };
        
            string jsonData = JsonUtility.ToJson(data);
            StartCoroutine(StartExerciseRoutine(jsonData));
        }
        else
        {
            Debug.LogError("Failed to parse exercise duration from text");
        }
        StartCoroutine(ExerciseCountdown(exerciseDurationText.text));
    }
    

    private IEnumerator StartExerciseRoutine(string jsonData)
    {
        using (UnityWebRequest www = UnityWebRequest.Post("http://localhost:5000/start_exercise", jsonData))
        {
            www.SetRequestHeader("Content-Type", "application/json");
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

            yield return www.SendWebRequest(); // Wait for the server response.

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Error starting exercise: {www.error}");
            }
            else
            {
                Debug.Log($"Exercise Completed: {www.downloadHandler.text}");
                // Here you can parse the response and update the UI with the reps count
                // after the exercise time has elapsed
            }
        }
    }
    
    private IEnumerator ExerciseCountdown(string durationText) {
        if (int.TryParse(durationText, out int duration)) {
            overlayPanel.SetActive(true); // Enable the overlay to block interactions

            // Start countdown
            for (int i = duration; i >= 0; i--) {
                countdownText.text = "Vent Venligst: " + i.ToString(); // Update countdown text
                yield return new WaitForSeconds(1);
            }

            countdownText.text = "Exercise Done!";
            yield return new WaitForSeconds(2); // Wait for 2 seconds after the countdown

            countdownText.text = ""; // Clear the countdown text
            overlayPanel.SetActive(false); // Disable the overlay to allow interactions
         
            
        } else {
            Debug.LogError("Invalid duration format.");
        }
    }

    
   
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
                    // Clear the current data to avoid duplicates
                    dateUIUpdater.ClearScrollView();

                    // Update the UI with the fetched data.
                    foreach (var exerciseData in wrapper.exerciseData)
                    {
                        dateUIUpdater.QueueExerciseData(exerciseData);
                    }
                
                    // Update the ScrollView after all data is queued.
                    dateUIUpdater.UpdateScrollView();
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
