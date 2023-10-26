using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CanvasInteractivity : MonoBehaviour
{
    public GameObject buttonPrefab;
    public RectTransform buttonParent;  // Use RectTransform instead of Transform

    public string[] buttonNames;  // You can set your desired names in the Unity Inspector
    public Vector2 buttonSize = new Vector2(100, 50);

    private Button øvelserButton;
    private Button dataButton;

    private void Start()
    {
        // Setting up GridLayoutGroup
        GridLayoutGroup grid = buttonParent.gameObject.AddComponent<GridLayoutGroup>();
        grid.cellSize = buttonSize;
        grid.spacing = new Vector2(10, 10);

        // Dynamically create name buttons
        for (int i = 0; i < buttonNames.Length; i++)
        {
            Button btn = Instantiate(buttonPrefab, buttonParent).GetComponent<Button>();
            TextMeshProUGUI buttonText = btn.GetComponentInChildren<TextMeshProUGUI>();
            if (buttonText != null)
            {
                buttonText.text = buttonNames[i];
            }
            else
            {
                Debug.LogError("Button does not have a TextMeshProUGUI component!");
            }
            btn.onClick.AddListener(ShowOptions);
        }

        // Dynamically create Øvelser and Data buttons
        øvelserButton = Instantiate(buttonPrefab).GetComponent<Button>();
        øvelserButton.GetComponentInChildren<TextMeshProUGUI>().text = "Øvelser";
        øvelserButton.transform.SetParent(transform, false); // Set it to this script's gameobject or another empty one
        øvelserButton.gameObject.SetActive(false);

        dataButton = Instantiate(buttonPrefab).GetComponent<Button>();
        dataButton.GetComponentInChildren<TextMeshProUGUI>().text = "Data";
        dataButton.transform.SetParent(transform, false); // Set it to this script's gameobject or another empty one
        dataButton.gameObject.SetActive(false);
    }

    private void ShowOptions()
    {
        if (øvelserButton != null && dataButton != null)
        {
            øvelserButton.gameObject.SetActive(true);
            dataButton.gameObject.SetActive(true);

            // Place the buttons at the bottom middle of the canvas panel
            Vector2 parentSize = buttonParent.rect.size;
            øvelserButton.GetComponent<RectTransform>().anchoredPosition = buttonParent.anchoredPosition + new Vector2(-buttonSize.x / 1, -parentSize.y / 2 + buttonSize.y / 2);
            dataButton.GetComponent<RectTransform>().anchoredPosition = buttonParent.anchoredPosition + new Vector2(buttonSize.x / 1, -parentSize.y / 2 + buttonSize.y / 2);
        }
        else
        {
            Debug.LogError("Øvelser or Data button is not instantiated.");
        }
    }

}