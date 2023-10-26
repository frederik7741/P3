using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using UnityEngine.Events; // Add this line to use UnityAction

public class CanvasInteractivity : MonoBehaviour
{
    public GameObject headerPrefab;
    public RectTransform backgroundPanel;
    public Vector2 returnButtonSize = new Vector2(100, 50);
    public GameObject buttonPrefab;
    public RectTransform buttonParent;
    public string[] buttonNames;
    public Vector2 buttonSize = new Vector2(100, 50);
    private Button øvelserButton;
    private Button dataButton;

    private void Awake()
    {
        SceneManager.sceneLoaded += OnSceneLoaded;
    }

    private void OnDestroy()
    {
        SceneManager.sceneLoaded -= OnSceneLoaded;
    }

    private void Start()
    {
        // Setup GridLayoutGroup for the buttons
        GridLayoutGroup grid = buttonParent.gameObject.AddComponent<GridLayoutGroup>();
        grid.cellSize = buttonSize;
        grid.spacing = new Vector2(10, 10);

        // Adjust the top padding to move the buttons down
        grid.padding.top = 150;

        // Dynamically create name buttons
        for (int i = 0; i < buttonNames.Length; i++)
        {
            Button btn = Instantiate(buttonPrefab, buttonParent).GetComponent<Button>();
            TextMeshProUGUI buttonText = btn.GetComponentInChildren<TextMeshProUGUI>();

            if (buttonText != null)
            {
                buttonText.text = buttonNames[i];
            }

            btn.onClick.AddListener(ShowOptions);
        }

        // Instantiate "Øvelser" and "Data" buttons outside the loop, directly under the rootCanvas
        Canvas rootCanvas = backgroundPanel.GetComponentInParent<Canvas>();
        øvelserButton = Instantiate(buttonPrefab, rootCanvas.transform).GetComponent<Button>();
        øvelserButton.GetComponentInChildren<TextMeshProUGUI>().text = "Øvelser";
        øvelserButton.gameObject.SetActive(false); // Initially hide the button
        øvelserButton.onClick.AddListener(OpenOvelserScene); // Add listener here

        dataButton = Instantiate(buttonPrefab, rootCanvas.transform).GetComponent<Button>();
        dataButton.GetComponentInChildren<TextMeshProUGUI>().text = "Data";
        dataButton.gameObject.SetActive(false); // Initially hide the button
        dataButton.onClick.AddListener(OpenDataScene); // Add listener here
    }

    private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        if (scene.name != "StartScreen")
        {
            InstantiateHeader();
        }
    }

    private void InstantiateHeader()
    {
        Canvas rootCanvas = backgroundPanel.GetComponentInParent<Canvas>();
        GameObject headerObj = Instantiate(headerPrefab, rootCanvas.transform);
    }

    private void ShowOptions()
    {
        Debug.Log("Button Clicked!"); // Add this line to check if the method is called.
        
        if (øvelserButton != null && dataButton != null)
        {
            øvelserButton.gameObject.SetActive(true);
            dataButton.gameObject.SetActive(true);

            // Position the "Øvelser" button at the bottom-left
            øvelserButton.GetComponent<RectTransform>().anchoredPosition = new Vector2(-buttonSize.x / 1, -buttonSize.y / 0.2f);

            // Position the "Data" button at the bottom-right
            dataButton.GetComponent<RectTransform>().anchoredPosition = new Vector2(buttonSize.x / 1, -buttonSize.y / 0.2f);
        }
    }

    private void OpenOvelserScene()
    {
        LoadSceneByName("Øvelser");
    }

    private void OpenDataScene()
    {
        LoadSceneByName("Data");
    }

    private void LoadSceneByName(string sceneName)
    {
        if (!SceneManager.GetSceneByName(sceneName).isLoaded)
        {
            SceneManager.LoadScene(sceneName);
        }
    }

    private void ReturnToPreviousScene()
    {
        SceneManager.LoadScene("StartScreen");
    }
}
