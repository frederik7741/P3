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
}

// This class manages the UI elements that display exercise data for patients.
public class DateUIUpdater : MonoBehaviour
{
    // UI elements to display and update exercise data.
    public Button[] dateButtons; // Array of buttons to display dates of exercises.
    public TextMeshProUGUI idPlaceholder; // Text field to show the patient ID.
    public TextMeshProUGUI repsPlaceholder; // Text field to show the number of repetitions.
    public TextMeshProUGUI datePlaceholder; // Text field to show the date of the exercise.

    // Queue to hold incoming exercise data before it's displayed.
    private Queue<ExerciseData> exerciseDataQueue = new Queue<ExerciseData>();

    // When the UI component is enabled, update the buttons with any queued data.
    void OnEnable()
    {
        ActivateAndUpdateButtons();
    }

    // Method to queue new exercise data and trigger UI update if active.
    public void QueueExerciseData(ExerciseData newData)
    {
        Debug.Log($"Queueing new exercise data: Date = {newData.date}, Reps = {newData.repetitions}");
        exerciseDataQueue.Enqueue(newData); // Add the new data to the queue.
    }

    // Method to update the date buttons with the queued exercise data.
    public void UpdateDateButtons()
    {
        int buttonIndex = 0; // Index to keep track of which button is being updated.
        // Reset text and listeners for all buttons first.
        foreach (var button in dateButtons)
        {
            button.GetComponentInChildren<TextMeshProUGUI>().text = "No data";
            button.onClick.RemoveAllListeners();
        }
        // Update buttons with data from the queue.
        while (exerciseDataQueue.Count > 0 && buttonIndex < dateButtons.Length)
        {
            ExerciseData data = exerciseDataQueue.Dequeue(); // Get the next item from the queue.
            Button button = dateButtons[buttonIndex]; // Get the current button to update.
            button.GetComponentInChildren<TextMeshProUGUI>().text = data.date; // Update button text with the date.
            button.onClick.AddListener(() => UpdatePlaceholders(data)); // Set the button to update placeholders when clicked.
            buttonIndex++; // Increment the button index.
        }
        Debug.Log($"Updated {buttonIndex} buttons with data.");
    }

    // Method to update the placeholders with the selected exercise data.
    public void UpdatePlaceholders(ExerciseData data)
    {
        // Set the text placeholders with the selected exercise data.
        idPlaceholder.text = $"ID: {data.patient_id}";
        repsPlaceholder.text = $"Reps: {data.repetitions}";
        datePlaceholder.text = $"Date: {data.date}";
    }

    // Check if the game object is active and update buttons if so.
    private void ActivateAndUpdateButtons()
    {
        // If the UI is active, call to update the date buttons with queued data.
        if (gameObject.activeInHierarchy)
        {
            UpdateDateButtons();
        }
    }
}
