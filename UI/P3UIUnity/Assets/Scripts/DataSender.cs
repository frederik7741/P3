using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;
using System.Collections;

public class DataSender : MonoBehaviour
{
    public PatientButtonPair[] patientButtons;
    public string getExerciseDataURL = "http://localhost:5000/get_exercise_data/";
    public string saveDataURL = "http://localhost:5000/save_data/";
    public DateUIUpdater dateUIUpdater;
    private int currentPatientId = -1;
    public TMP_Text time; // Ensure this is linked in the Unity Inspector

    [System.Serializable]
    public class ExerciseDataWrapper
    {
        public ExerciseData[] exerciseData;
    }

    [System.Serializable]
    public class PatientButtonPair
    {
        public Button button;
        public int patientId;
    }



    void Start()
    {
        foreach (var pair in patientButtons)
        {
            pair.button.onClick.AddListener(() => OnPatientButtonClicked(pair.patientId));
        }
    }

    public void OnPatientButtonClicked(int patientId)
    {
        currentPatientId = patientId;
        StartCoroutine(GetPatientExerciseData(patientId));
    }

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
            repetitions = 15 // Replace with the actual value from your exercise logic
        };

        StartCoroutine(PostRequest(data));
    }

    private IEnumerator PostRequest(ExerciseData data)
    {
        string jsonData = JsonUtility.ToJson(data);
        using (UnityWebRequest www = UnityWebRequest.Post(saveDataURL, "POST"))
        {
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();

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

                    foreach (var exerciseData in wrapper.exerciseData)
                    {
                        dateUIUpdater.QueueExerciseData(exerciseData);
                    }

                    // It's important to call UpdateDateButtons after all the data has been enqueued.
                    dateUIUpdater.UpdateDateButtons();
                }
                else
                {
                    Debug.LogError("Failed to parse exercise data.");
                }
            }
        }
    }



    public void OnTimeSliderChanged(Slider slider)
    {
        time.text = slider.value.ToString();
    }
}
