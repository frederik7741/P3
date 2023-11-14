using TMPro;
using UnityEngine;
using System.Collections.Generic;

public class DateUIUpdater : MonoBehaviour
{
    public TextMeshProUGUI[] dateButtons;
    private Queue<string> dateQueue = new Queue<string>();

    void OnEnable()
    {
        ActivateAndUpdateButtons();
    }

    public void QueueDateUpdate(string newDate)
    {
        Debug.Log($"Enqueuing new date: {newDate}");
        dateQueue.Enqueue(newDate);

        // It's not necessary to check if the gameObject is active in the hierarchy here
        // because this script's gameObject should always be active for the component to work.
        ActivateAndUpdateButtons();
    }

    public void UpdateDateButtons()
    {
        Debug.Log($"Updating Date Buttons. Queue Count: {dateQueue.Count}");
        while (dateQueue.Count > 0 && dateButtons.Length > 0)
        {
            string dateToUpdate = dateQueue.Dequeue();
            Debug.Log($"Dequeuing date: {dateToUpdate}");

            for (int i = dateButtons.Length - 1; i > 0; i--)
            {
                dateButtons[i].text = dateButtons[i - 1].text;
            }
            dateButtons[0].text = dateToUpdate;
        }
    }

    // Call this method after date buttons are activated to ensure they're updated with any queued data
    public void ActivateAndUpdateButtons()
    {
        // Check if date buttons are active and update them
        foreach (var button in dateButtons)
        {
            if (button.gameObject.activeInHierarchy)
            {
                UpdateDateButtons();
                break; // Only need to update once if at least one button is active
            }
        }
    }

    // This method can be linked to the OnClick event of the date button if needed.
    public void OnDateButtonClick()
    {
        // Ensure any queued data is processed and the UI is updated.
        UpdateDateButtons();
    }
}
