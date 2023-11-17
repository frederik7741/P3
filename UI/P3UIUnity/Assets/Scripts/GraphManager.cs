using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;
using TMPro;

// Ensure this class is defined in the same namespace as it's used in DataSender
[System.Serializable]
public class ExerciseDataWrapper
{
    public ExerciseData[] exerciseData;
}

public class GraphManager : MonoBehaviour
{
    public GameObject barPrefab; // Set this to your bar prefab
    public RectTransform graphContainer; // Set this to the RectTransform of the parent object in the canvas where bars should be placed
    public GameObject numberIndicatorPrefab; // Assign this prefab in the Inspector
    public Button comparisonButton;
    private bool graphGenerated = false; // Missing variable declaration added
    private DataSender dataSender; // Reference to the DataSender script
  
    private void Start()
    {
        dataSender = FindObjectOfType<DataSender>(); // Find the DataSender in the scene
        comparisonButton.onClick.AddListener(FillGraph);
        
    }

    private IEnumerator FetchExerciseDataFromDatabase(int patientId)
    {
        // Use the URL from the dataSender
        string getExerciseDataURL = dataSender.getExerciseDataURL;

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
                    ClearGraph();
                    GenerateGraph(new List<ExerciseData>(wrapper.exerciseData));
                }
                else
                {
                    Debug.LogError("Failed to parse exercise data.");
                }
            }
        }
    }
    private void FillGraph()
    {
        if (!graphGenerated && dataSender != null)
        {
            StartCoroutine(FetchExerciseDataFromDatabase(dataSender.currentPatientId)); // Use the currentPatientId from DataSender
        }
    }
    
    private void ClearGraph()
    {
        foreach (Transform child in graphContainer)
        {
            Destroy(child.gameObject); // Destroy all child objects (bars) of the graph container
        }
    }

    
    public void GenerateGraph(List<ExerciseData> exerciseDataList)
    {
        GenerateNumberIndicators(); // Call to generate number indicators on the left side of the graph

        float containerWidth = graphContainer.rect.width;
        float spacing = 10f; // Adjust spacing between bars
        float indicatorOffset = 50f; // Adjust this value based on the width of your number indicators
        float barWidth = (containerWidth - indicatorOffset - (spacing * (exerciseDataList.Count + 1))) / exerciseDataList.Count;
        float leftOffset = spacing + indicatorOffset; // Offset from the left side to account for number indicators
        float labelOffset = 20f; // Vertical offset for the label above the bar
        
        for (int i = 0; i < exerciseDataList.Count; i++)
        {
            GameObject bar = Instantiate(barPrefab, graphContainer);
            RectTransform rt = bar.GetComponent<RectTransform>();

            rt.pivot = new Vector2(0, 0); // Sets pivot to the bottom left
            rt.anchorMin = new Vector2(0, 0); // Sets the anchor to the bottom left
            rt.anchorMax = new Vector2(0, 0); // Sets the anchor to the bottom left

            float barPositionX = leftOffset + i * (barWidth + spacing);
            rt.anchoredPosition = new Vector2(barPositionX, 0);

            float heightFactor = Mathf.Clamp01((float)exerciseDataList[i].repetitions / 50f); // Assuming 50 is max reps
            rt.sizeDelta = new Vector2(barWidth, heightFactor * graphContainer.rect.height);
                
            // Instantiate a new TextMeshProUGUI or similar for the label
            GameObject label = new GameObject("ExerciseLabel", typeof(TextMeshProUGUI));
            label.transform.SetParent(graphContainer);
            // Set the label's RectTransform properties
            RectTransform labelRt = label.GetComponent<RectTransform>();
            labelRt.sizeDelta = new Vector2(barWidth, 20); // Adjust height as needed
            labelRt.anchorMin = new Vector2(0, 0);
            labelRt.anchorMax = new Vector2(0, 0);
            labelRt.pivot = new Vector2(0.5f, 0);
            labelRt.anchoredPosition = new Vector2(
                rt.anchoredPosition.x + rt.sizeDelta.x / 2, // This centers the label above the bar
                rt.sizeDelta.y + labelOffset
            );

            // Set the exercise name
            TextMeshProUGUI textMesh = label.GetComponent<TextMeshProUGUI>();
            textMesh.alignment = TextAlignmentOptions.Center;
            textMesh.text = "ØV" + (1); // Assuming you just want to number them

            // Set other text properties
            textMesh.fontSize = 10; // Adjust as needed
            textMesh.color = Color.black; // Adjust as needed
        }
        
    }

    

    private void GenerateNumberIndicators()
    {
        float maxReps = 50f; // Maximum number of repetitions
        float increment = 5f; // Increment value for each indicator
        int numberOfIndicators = (int)(maxReps / increment);

        for (int i = 0; i <= numberOfIndicators; i++)
        {
            GameObject indicator = Instantiate(numberIndicatorPrefab, graphContainer);
            RectTransform rt = indicator.GetComponent<RectTransform>();

            rt.anchorMin = new Vector2(0, 0); // Anchored to the bottom left
            rt.anchorMax = new Vector2(0, 0); // Anchored to the bottom left
            rt.pivot = new Vector2(0, 0); // Pivot at the bottom left

            // Position each indicator at the correct height
            float normalizedHeight = (increment * i) / maxReps;
            float yPos = normalizedHeight * graphContainer.rect.height;

            // Apply additional offset for the first and last indicators
            if (i == 0) {
                yPos += 25; // Adjust this value as needed
            } else if (i == numberOfIndicators) {
                yPos -= 15; // Adjust this value as needed
            }

            rt.anchoredPosition = new Vector2(+1, yPos); // Adjust the x offset as needed

            // Set the text to the current increment value
            TextMeshProUGUI textMesh = indicator.GetComponent<TextMeshProUGUI>();
            textMesh.text = (increment * i).ToString();
        }
    }



}
