using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using UnityVolumeRendering;

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

    private void Start()
    {
        StartCoroutine(GetData());
    }

    //public IEnumerator Upload(IEnumerable<string> files)
    //{
    //    List<IMultipartFormSection> formData = new List<IMultipartFormSection>();

    //    foreach (string file in files)
    //    {
    //        byte[] data = File.ReadAllBytes(file);
    //        formData.Add(new MultipartFormFileSection("files", data, Path.GetFileName(file), "multipart/form-data"));
    //    }

    //    UnityWebRequest www = UnityWebRequest.Post("http://localhost:3000/dicom/upload", formData);
    //    yield return www.SendWebRequest();

    //    if (www.result != UnityWebRequest.Result.Success)
    //    {
    //        Debug.LogError("Could not upload the files");
    //    }
    //    else
    //    {
    //        Debug.Log("Files successfully uploaded");
    //    }
    //}

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

    public IEnumerator GetData()
    {
        string path = "/Users/vinicius/Downloads/Angosto_Calvet_Antonio/AngioTc_Abdomen_I_Pelvis - 3494/ARTERIAL_IMR_402";
        string uri = "http://localhost:3000/dicom/3d?path=" + path;
        Debug.Log("START");
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

                VolumeRenderedObject obj = VolumeObjectFactory.CreateObject(dataset);
                obj.transform.position = new Vector3(1, 0, 0);
            }
        }
    }
}
