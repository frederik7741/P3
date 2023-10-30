using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;

public class CanvasInteractivity : MonoBehaviour
{
    public GameObject buttonPrefab;
    public RectTransform buttonParent;
    public string[] buttonNames;
    public Vector2 buttonSize = new Vector2(100, 50);
    private Button øvelserButton;
    private Button dataButton;
    public Vector3 buttonScale = new Vector3(5f, 5f, 5f);
    private void Start()
    {
       
        // Create "Øvelser" and "Data" buttons
        øvelserButton = CreateButton("Øvelser", new Vector2(0, 0), OpenOvelserScene);
        dataButton = CreateButton("Data", new Vector2(60, -50), OpenDataScene);
       
    }

    public Button CreateButton(string text, Vector2 position, UnityEngine.Events.UnityAction onClickAction)
    {
        Canvas rootCanvas = buttonParent.GetComponentInParent<Canvas>();
        Button button = Instantiate(buttonPrefab, rootCanvas.transform).GetComponent<Button>();
        button.GetComponent<RectTransform>().anchoredPosition = position;
        button.GetComponentInChildren<TextMeshProUGUI>().text = text;
        button.onClick.AddListener(onClickAction);
        
        if (text != "Return")
            button.gameObject.SetActive(false);

        return button;
    }

    public void ShowOptions()
    {
        øvelserButton.gameObject.SetActive(true);
        øvelserButton.GetComponent<RectTransform>().anchoredPosition = new Vector2(-buttonSize.x / 1, -buttonSize.y / 0.2f);
      
        
        dataButton.gameObject.SetActive(true);
        dataButton.GetComponent<RectTransform>().anchoredPosition = new Vector2(buttonSize.x / 1, -buttonSize.y / 0.2f);
        
    }

    public void OpenOvelserScene()
    {
        LoadSceneByName("Øvelser");
    }

    public void OpenDataScene()
    {
        LoadSceneByName("Data");
    }

    public void LoadSceneByName(string sceneName)
    {
        if (!SceneManager.GetSceneByName(sceneName).isLoaded)
        {
            SceneManager.LoadScene(sceneName);
        }
    }

    public void ReturnToPreviousScene()
    {
        SceneManager.LoadScene("StartScreen");
    }
}
