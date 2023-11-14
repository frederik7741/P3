using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
public class TestConnection : MonoBehaviour
{
    public string serverURL = "http://localhost:5000/test_connection";

    void Start()
    {
        StartCoroutine(TestServerConnection());
    }

    IEnumerator TestServerConnection()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(serverURL))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
            }
            else
            {
                Debug.Log("Server response: " + www.downloadHandler.text);
            }
        }
    }
}