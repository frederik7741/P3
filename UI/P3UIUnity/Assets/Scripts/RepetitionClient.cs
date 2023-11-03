using System;
using System.Collections;
using System.Net.Sockets;
using System.IO;
using System.Text;
using UnityEngine;
using TMPro; // Import the TextMeshPro namespace

public class RepetitionReader : MonoBehaviour
{
   

    private TcpClient client;
    private StreamReader reader;
    private StreamWriter writer;
    private string host = "127.0.0.1";
    private int port = 6789;
    public TextMeshProUGUI repetitionsText; // Public field to assign TextMeshPro UI element
    void Start()
    {
        // Start connecting to the server
        StartCoroutine(ConnectToServer());
    }

    IEnumerator ConnectToServer()
    {
        client = new TcpClient();
        bool tryConnect = true;

        while (!client.Connected && tryConnect)
        {
            try
            {
                client.Connect(host, port);
                writer = new StreamWriter(client.GetStream(), Encoding.UTF8);
                reader = new StreamReader(client.GetStream(), Encoding.UTF8);
                StartCoroutine(ReadData()); // Start reading once connected
            }
            catch (Exception e)
            {
                Debug.LogError("Connection attempt failed: " + e.Message);
                tryConnect = false; // Set the flag to false indicating connection attempt failed
            }

            if (!tryConnect)
            {
                yield return new WaitForSeconds(1); // Wait for a second before trying to reconnect
                tryConnect = true; // Reset the flag for the next attempt
            }
        }
    }


    IEnumerator ReadData()
    {
        while (client != null && client.Connected)
        {
            if (client.Available > 0)
            {
                try
                {
                    string message = reader.ReadLine();
                    if (message != null)
                    {
                        UpdateTextUI(message);
                    }
                }
                catch (Exception e)
                {
                    Debug.LogError("Error reading from server: " + e.Message);
                    client.Close(); // Close the client and exit the loop
                    break;
                }
            }
            yield return null;
        }
        StartCoroutine(ConnectToServer()); // Attempt to reconnect
    }


    void UpdateTextUI(string message)
    {
        if (repetitionsText != null)
        {
            repetitionsText.text = "Repetitions: " + message;
        }
        else
        {
            Debug.LogWarning("TextMeshProUGUI component not set in the inspector");
        }
    }
}
