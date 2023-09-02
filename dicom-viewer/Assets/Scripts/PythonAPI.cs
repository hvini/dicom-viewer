using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using UnityVolumeRendering;
using System.Text;
using System.Linq;
using CandyCoded.env;
using UnityEngine.UI;
using Newtonsoft.Json.Linq;

[Serializable]
public class Patients
{
    public int id { get; set; }
    public string patientID { get; set; }
    public string name { get; set; }
    public string birthDate { get; set; }
}

[Serializable]
public class Studies
{
    public int id { get; set; }
    public int patientID { get; set; }
    public string instanceUID { get; set; }
    public string description { get; set; }
    public string time { get; set; }
}

[Serializable]
public class Series
{
    public int id { get; set; }
    public int studyID { get; set; }
    public string instanceUID { get; set; }
    public string filepath { get; set; }
    public string bitspath { get; set; }
    public string description { get; set; }
    public int dimX { get; set; }
    public int dimY { get; set; }
    public int dimZ { get; set; }
    public string pixelSpacing { get; set; }
    public float scaleX { get; set; }
    public float scaleY { get; set; }
    public float scaleZ { get; set; }
}

[Serializable]
public class Instances
{
    public int id { get; set; }
    public int seriesID { get; set; }
    public string filename { get; set; }
}

public class PythonAPI : MonoBehaviour
{
    public List<Patients> patients;
    public List<Studies> studies;
    public List<Series> series;

    private string baseURL;

    private GameObject currentObj = null;

    private Button[] seriesBtns = null;
    private Button patientsBtn = null;
    private Button studiesBtn = null;

    private Text loadingTxt = null;

    private NetworkManager networkManager;

    private int MSG_LENGTH = 9;

    private void Awake()
    {
        if (env.TryParseEnvironmentVariable("BASE_URL", out string url))
        {
            baseURL = url;
        }

        networkManager = GameObject.Find("Network Manager").GetComponent<NetworkManager>();
    }

    private void Start()
    {
        //patientsBtn = GameObject.Find("Canvas")
        //    .transform.Find("PatientsBtn").GetComponent<Button>();

        //studiesBtn = GameObject.Find("Canvas")
        //    .transform.Find("StudiesBtn").GetComponent<Button>();

        //loadingTxt = GameObject.Find("Canvas")
        //    .transform.Find("LoadingTxt").GetComponent<Text>();

        networkManager.websocket.OnMessage += (bytes) =>
        {
            if (!networkManager.isMaster)
            {
                if (bytes.Length > MSG_LENGTH)
                {
                    string code = Encoding.UTF8.GetString(bytes, 0, MSG_LENGTH);
                    int dataLength = bytes.Length - MSG_LENGTH;
                    byte[] data = new byte[dataLength];
                    data = bytes.Skip(MSG_LENGTH).Take(dataLength).ToArray();

                    if (code.Equals("masterObj"))
                    {
                        Series series = (Series)networkManager.ParseMessage(data);
                        StartCoroutine(LoadModel(series));
                    }
                }
            }
        };
    }

    public IEnumerator Get(string uri, string type)
    {
        using (UnityWebRequest request = UnityWebRequest.Get(uri))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log("Error on get data: " + request.error);
            }
            else
            {
                string json = request.downloadHandler.text;
                var jsonObj = JObject.Parse(json);

                if (type == "patients")
                {
                    patients = JsonConvert.DeserializeObject<List<Patients>>(jsonObj["data"].ToString());
                }
                else if (type == "studies")
                {
                    studies = JsonConvert.DeserializeObject<List<Studies>>(jsonObj["data"].ToString());
                }
                else
                {
                    series = JsonConvert.DeserializeObject<List<Series>>(jsonObj["data"].ToString());
                }
                
                Debug.Log("Data successfully retrieved!");
            }
        }
    }

    public IEnumerator LoadModel(Series series)
    {
        seriesBtns = GameObject.Find("Canvas")
            .transform.Find("SeriesTable")
            .transform.Find("SeriesEntryContainer").GetComponentsInChildren<Button>();

        DisableBtns(seriesBtns);

        if (currentObj != null) Destroy(currentObj);

        VolumeDataset dataset = JsonConvert.DeserializeObject<VolumeDataset>(JsonConvert.SerializeObject(series));
        dataset.FixDimensions();

        using (UnityWebRequest request = UnityWebRequest.Get(series.bitspath))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.ConnectionError)
            {
                throw new Exception($"Failed to retrieve data from URL. Error: {request.error}");
            }
            else
            {
                dataset.jdlskald = request.downloadHandler.data;
            }
        }

        VolumeRenderedObject obj = VolumeObjectFactory.CreateObject(dataset, series);
        obj.transform.position = new Vector3(0.0f, -1.0f, 1.3f);

        if (!networkManager.isMaster)
        {
            obj.transform.localScale = new Vector3(10.0f, 10.0f, 10.0f);
        }
        else
        {
            obj.tag = "Interactable";

            obj.gameObject.AddComponent<Rigidbody>();
            obj.GetComponent<Rigidbody>().useGravity = false;
            obj.GetComponent<Rigidbody>().velocity = Vector3.zero;

            obj.gameObject.AddComponent<BoxCollider>();
            obj.gameObject.AddComponent<MouseDrag>();
        }

        obj.gameObject.AddComponent<VolumePosition>();
        currentObj = obj.gameObject;

        EnableBtns(seriesBtns);

        yield return null;
    }

    private void DisableBtns(Button[] btns)
    {
        if (networkManager.isMaster)
        {
            // disable header buttons
            patientsBtn.interactable = false;
            studiesBtn.interactable = false;

            // disable action buttons
            foreach (Button btn in btns)
            {
                btn.interactable = false;
            }
        }
    }


    private void EnableBtns(Button[] btns)
    {
        if (networkManager.isMaster)
        {
            // enable header buttons
            patientsBtn.interactable = true;
            studiesBtn.interactable = true;

            // enable action buttons
            foreach (Button btn in btns)
            {
                btn.interactable = true;
            }
        }
    }
}
