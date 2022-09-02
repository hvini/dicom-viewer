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
    private string baseURL, basePath;

    private void Start()
    {
        if (env.TryParseEnvironmentVariable("BASE_URL", out string url))
        {
            baseURL = url;
        }

        if (env.TryParseEnvironmentVariable("BASE_PATH", out string path))
        {
            basePath = path;
        }
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
        string path = basePath + series.filepath;
        string bitspath = basePath + series.bitspath;

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

                VolumeRenderedObject obj = VolumeObjectFactory.CreateObject(dataset, series);
                obj.transform.position = new Vector3(1, 0, 0);

                GameObject canvas = GameObject.Find("Canvas");
                canvas.SetActive(false);

                if (series.bitspath == null) {
                    series.bitspath = "bits/" + series.instanceUID + ".bits";
                    StartCoroutine(Put(baseURL + "series/" + series.id + "/update", JsonConvert.SerializeObject(series)));
                }
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
}
