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
using System.IO;

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

    private void Start()
    {
        if (env.TryParseEnvironmentVariable("BASE_URL", out string url))
        {
            baseURL = url;
        }

        patientsBtn = GameObject.Find("Canvas")
            .transform.Find("PatientsBtn").GetComponent<Button>();

        studiesBtn = GameObject.Find("Canvas")
            .transform.Find("StudiesBtn").GetComponent<Button>();

        loadingTxt = GameObject.Find("Canvas")
            .transform.Find("LoadingTxt").GetComponent<Text>();
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

                if (type == "patients")
                {
                    patients = JsonConvert.DeserializeObject<List<Patients>>(json);
                }
                else if (type == "studies")
                {
                    studies = JsonConvert.DeserializeObject<List<Studies>>(json);
                }
                else
                {
                    series = JsonConvert.DeserializeObject<List<Series>>(json);
                }
                
                Debug.Log("Data successfully retrieved!");
            }
        }
    }

    public IEnumerator GetData(Series series)
    {
        seriesBtns = GameObject.Find("Canvas")
            .transform.Find("SeriesTable")
            .transform.Find("SeriesEntryContainer").GetComponentsInChildren<Button>();

        DisableBtns(seriesBtns);

        if (currentObj != null) Destroy(currentObj);

        string path = series.filepath;
        string bitspath = series.bitspath;

        string uri = baseURL + "dicom/3d?path=" + path + "&bitspath=" + bitspath;
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

                VolumeDataset dataset = JsonConvert.DeserializeObject<VolumeDataset>(json);

                dataset.FixDimensions();

                if (bitspath == null) bitspath = dataset.bitspath;

                UnityWebRequest www = UnityWebRequest.Get(baseURL + bitspath);
                var operation = www.SendWebRequest();

                while (!operation.isDone)
                {
                    loadingTxt.text = Mathf.Round(www.downloadProgress * 100).ToString() + "%";
                    yield return null;
                }

                loadingTxt.text = "";

                dataset.jdlskald = www.downloadHandler.data;

                VolumeRenderedObject obj = VolumeObjectFactory.CreateObject(dataset, series);
                obj.tag = "Interactable";

                obj.gameObject.AddComponent<Rigidbody>();
                obj.GetComponent<Rigidbody>().useGravity = false;

                obj.gameObject.AddComponent<BoxCollider>();
                obj.gameObject.AddComponent<MouseDrag>();

                obj.transform.position = new Vector3(0.0f, -1.0f, 1.3f);

                currentObj = obj.gameObject;

                EnableBtns(seriesBtns);
            }
        }
    }

    public IEnumerator Put(string url, string bodyJsonString)
    {
        byte[] data = Encoding.UTF8.GetBytes(bodyJsonString);
        using (UnityWebRequest request = UnityWebRequest.Put(url, data))
        {
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log("Error on get data: " + request.error);
            }
            else
            {
                string json = request.downloadHandler.text;
                Series result = JsonConvert.DeserializeObject<Series>(json);

                Series obj = series.FirstOrDefault(x => x.id == result.id);
                if (obj != null) obj = result;
            }
        };
    }

    private void DisableBtns(Button[] btns)
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


    private void EnableBtns(Button[] btns)
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
