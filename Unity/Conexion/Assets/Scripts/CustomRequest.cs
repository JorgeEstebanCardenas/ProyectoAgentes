using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System;

public class CustomRequest : MonoBehaviour
{
    public string uri = "";
    public TextAsset jsonFile;
    public SpawnManager spawnManager;

    void Start()
    {
        StartCoroutine(GetRequest(uri));
    }

    IEnumerator GetRequest(string uri)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
        {
            // Request and wait for the desired page.
            yield return webRequest.SendWebRequest();

            string[] pages = uri.Split('/');
            int page = pages.Length - 1;

            switch (webRequest.result)
            {
                case UnityWebRequest.Result.ConnectionError:
                case UnityWebRequest.Result.DataProcessingError:
                    Debug.LogError(pages[page] + ": Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.ProtocolError:
                    Debug.LogError(pages[page] + ": HTTP Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.Success:
                    string jsonString = webRequest.downloadHandler.text;
                    SimulationInfo simulationInfo = JsonUtility.FromJson<SimulationInfo>(jsonString);
                    spawnManager.SpawnAgents(simulationInfo);
                    break;
            }
        }
    }
}

public class PostInfo
{
    public int XPosition;
    public int YPosition;
    public int ZPosition;
}

[Serializable]
public class SimulationInfo
{
    public Agent[] agents;
    public Step[] steps;
}

[Serializable]
public class Agent
{
    public int id;
    public int type;
}

[Serializable]
public class Step
{
    public StepInfo Stepinfo;
}

[Serializable]
public class StepInfo
{
    public int agentId;
    public int stepIndex;
    public float time;
    public string state;
    public float positionX;
    public float positionY;
    //public float positionZ;
}