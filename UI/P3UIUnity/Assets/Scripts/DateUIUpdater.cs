using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

// Serializable class to hold exercise data for each patient.
[System.Serializable]
public class ExerciseData
{
    public int patient_id;
    public string date;
    public int repetitions;
    public string exercise_name;
}

// This class manages the UI elements that display exercise data for patients.
public class DateUIUpdater : MonoBehaviour
{
    // UI elements to display and update exercise data.
    public TextMeshProUGUI idPlaceholder; // Text field to show the patient ID.
    public TextMeshProUGUI repsPlaceholder; // Text field to show the number of repetitions.
    public TextMeshProUGUI datePlaceholder; // Text field to show the date of the exercise.
    public TextMeshProUGUI exerciseNamePlaceholder;
	public GameObject buttonPrefab; // Assign this prefab in the Inspector
	public Transform scrollViewContent; // Assign the content panel of your ScrollRect here
	public GameObject InformationBox;
    
    // Queue to hold incoming exercise data before it's displayed.
    private Queue<ExerciseData> exerciseDataQueue = new Queue<ExerciseData>();


  public void QueueExerciseData(ExerciseData newData) {
    Debug.Log($"Queueing new exercise data: Date = {newData.date}, Reps = {newData.repetitions}");
    exerciseDataQueue.Enqueue(newData);
    
}


public void UpdateScrollView() {
    Debug.Log($"Creating buttons for {exerciseDataQueue.Count} entries.");

    while (exerciseDataQueue.Count > 0) {
        ExerciseData data = exerciseDataQueue.Dequeue(); // Get the next item from the queue.
        CreateButtonForData(data);
    }
}




private void CreateButtonForData(ExerciseData data)
{
    GameObject newButton = Instantiate(buttonPrefab, scrollViewContent);
    newButton.GetComponentInChildren<TextMeshProUGUI>().text = data.date;
    
    ExerciseData buttonData = data;
    newButton.GetComponent<Button>().onClick.AddListener(delegate {
        
        UpdatePlaceholders(buttonData);
        InformationBox.SetActive(true);
    });
}






public void ClearScrollView()
{
    foreach (Transform child in scrollViewContent)
    {
        Destroy(child.gameObject);
    }
}
    // Method to update the placeholders with the selected exercise data.
   public void UpdatePlaceholders(ExerciseData data)
{
    
    idPlaceholder.text = $"ID: {data.patient_id}";
    repsPlaceholder.text = $"Reps: {data.repetitions}";
    datePlaceholder.text = $"Date: {data.date}";
    exerciseNamePlaceholder.text = $"Exercise: {data.exercise_name}";
}


  
}
