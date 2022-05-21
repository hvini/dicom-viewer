using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;
using UnityVolumeRendering;
using System.Linq;

public class PythonAPI : MonoBehaviour
{
    string dir = "/Users/vinicius/Downloads/test/";

    // Start is called before the first frame update
    public void Start()
    {
        //StartCoroutine(GetData());

        if (Directory.Exists(dir))
        {
            bool recursive = true;

            IEnumerable<string> fileCandidates = Directory.EnumerateFiles(dir, "*.*", recursive ? SearchOption.AllDirectories : SearchOption.TopDirectoryOnly)
                .Where(p => p.EndsWith(".dcm", StringComparison.InvariantCultureIgnoreCase));

            if (fileCandidates.Any())
            {
                StartCoroutine(Upload(fileCandidates));

                IImageSequenceImporter importer = ImporterFactory.CreateImageSequenceImporter(ImageSequenceFormat.DICOM);
                IEnumerable<IImageSequenceSeries> seriesList = importer.LoadSeries(fileCandidates);
                float numVolumesCreated = 0;

                foreach (IImageSequenceSeries series in seriesList)
                {
                    VolumeDataset dataset = importer.ImportSeries(series);
                    if (dataset != null)
                    {
                        VolumeRenderedObject obj = VolumeObjectFactory.CreateObject(dataset);
                        obj.transform.position = new Vector3(numVolumesCreated, 0, 0);
                        numVolumesCreated++;
                    }
                }
            } else
            {
                Debug.LogError("Could not find any DICOM files to import");
            }
        }
    }

    public IEnumerator Upload(IEnumerable<string> files)
    {
        List<IMultipartFormSection> formData = new List<IMultipartFormSection>();

        foreach (string file in files)
        {
            byte[] data = File.ReadAllBytes(file);
            formData.Add(new MultipartFormFileSection("files", data, Path.GetFileName(file), "multipart/form-data"));
        }

        UnityWebRequest www = UnityWebRequest.Post("http://localhost:3000/dicom/upload", formData);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Could not upload the files");
        }
        else
        {
            Debug.Log("Files successfully uploaded");
        }
    }
}
