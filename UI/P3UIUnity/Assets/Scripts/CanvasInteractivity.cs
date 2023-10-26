using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;

public class CanvasInteractivity : MonoBehaviour
{
    public GameObject backButtonPrefab; // Return Button prefab
    public GameObject headerPrefab; // Header prefab
    public RectTransform backgroundPanel; // The UI panel named "Background"
    public Vector2 returnButtonSize = new Vector2(100, 50);
    public GameObject buttonPrefab;
    public RectTransform buttonParent;  // The grid for buttons inside the "Background" panel
    public string[] buttonNames;  // Names set in the Unity Inspector
    public Vector2 buttonSize = new Vector2(100, 50);
    private Button øvelserButton;
    private Button dataButton;

    private void Awake()
    {
        // Subscribe to the sceneLoaded event
        SceneManager.sceneLoaded += OnSceneLoaded;
    }

    private void OnDestroy()
    {
        // Unsubscribe from the event
        SceneManager.sceneLoaded -= OnSceneLoaded;
    }

    private void Start()
    {
        // Setup GridLayoutGroup for the buttons
        GridLayoutGroup grid = buttonParent.gameObject.AddComponent<GridLayoutGroup>();
        grid.cellSize = buttonSize;
        grid.spacing = new Vector2(10, 10);
    
        // Adjust the top padding to move the buttons down
        grid.padding.top = 150;  // Adjust this value as needed

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
        // Get the root canvas
        Canvas rootCanvas = backgroundPanel.GetComponentInParent<Canvas>();

        // Instantiate the header under the canvas
        GameObject headerObj = Instantiate(headerPrefab, rootCanvas.transform);
    }




    private void ShowOptions()
    {
        // Implementation for the ShowOptions method (unchanged)
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
