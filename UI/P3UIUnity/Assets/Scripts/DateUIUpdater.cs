using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

[System.Serializable]
public class ExerciseData
{
    public int patient_id;
    public string date;
    public int repetitions;
}

public class DateUIUpdater : MonoBehaviour
{
    public Button[] dateButtons; // Buttons to display the exercise data
    public TextMeshProUGUI idPlaceholder; // Placeholder to display the patient ID
    public TextMeshProUGUI repsPlaceholder; // Placeholder to display the repetitions
    public TextMeshProUGUI datePlaceholder; // Placeholder to display the date

    private Queue<ExerciseData> exerciseDataQueue = new Queue<ExerciseData>();

    void OnEnable()
    {
        ActivateAndUpdateButtons();
    }

    public void QueueExerciseData(ExerciseData newData)
    {
        Debug.Log($"Queueing new exercise data: Date = {newData.date}, Reps = {newData.repetitions}");
        exerciseDataQueue.Enqueue(newData);
    }

    public void UpdateDateButtons()
    {
        int buttonIndex = 0;
        foreach (var button in dateButtons)
        {
            button.GetComponentInChildren<TextMeshProUGUI>().text = "No data"; // Reset the button text
            button.onClick.RemoveAllListeners(); // Clear previous listeners
        }

        while (exerciseDataQueue.Count > 0 && buttonIndex < dateButtons.Length)
        {
            ExerciseData data = exerciseDataQueue.Dequeue();
            Button button = dateButtons[buttonIndex];
            button.GetComponentInChildren<TextMeshProUGUI>().text = data.date; // Set the button text to the date
            button.onClick.AddListener(() => UpdatePlaceholders(data)); // Set the button to update placeholders when clicked
            buttonIndex++;
        }

        Debug.Log($"Updated {buttonIndex} buttons with data.");
    }

    public void UpdatePlaceholders(ExerciseData data)
    {
        idPlaceholder.text = $"ID: {data.patient_id}";
        repsPlaceholder.text = $"Reps: {data.repetitions}";
        datePlaceholder.text = $"Date: {data.date}";
    }

    private void ActivateAndUpdateButtons()
    {
        if (gameObject.activeInHierarchy)
        {
            UpdateDateButtons();
        }
    }
}
