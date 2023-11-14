using TMPro;
using UnityEngine;
using System.Collections.Generic;

public class DateUIUpdater : MonoBehaviour
{
    public TextMeshProUGUI[] dateButtons;
    private Queue<string> dateQueue = new Queue<string>();

    void OnEnable()
    {
        // Update the UI elements with the stored dates
        UpdateDateButtons();
    }

    public void QueueDateUpdate(string newDate)
    {
        // Store the new date
        dateQueue.Enqueue(newDate);

        // If the object is active, immediately update the buttons
        if (gameObject.activeInHierarchy)
        {
            UpdateDateButtons();
        }
    }

    public void UpdateDateButtons()
    {
        while (dateQueue.Count > 0 && dateButtons.Length > 0)
        {
            string dateToUpdate = dateQueue.Dequeue();
            // Shift the dates down and add the new date at the top
            for (int i = dateButtons.Length - 1; i > 0; i--)
            {
                dateButtons[i].text = dateButtons[i - 1].text; // Move the text down one button
            }
            dateButtons[0].text = dateToUpdate; // Set the latest date to the first button
        }
    }
}
