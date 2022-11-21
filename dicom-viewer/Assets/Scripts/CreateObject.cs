using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityVolumeRendering;

public class CreateObject : MonoBehaviour
{
    public static void CreateVolObject(string filepath)
    {
        if (Directory.Exists(filepath))
        {
            bool recursive = true;

            IEnumerable<string> fileCandidates = Directory.EnumerateFiles(filepath, "*.*", recursive ? SearchOption.AllDirectories : SearchOption.TopDirectoryOnly)
                .Where(p => p.EndsWith(".dcm", StringComparison.InvariantCultureIgnoreCase));

            if (fileCandidates.Any())
            {
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
                        obj.gameObject.AddComponent<LookControls>();

                        Camera.main.transform.position = new Vector3(obj.transform.position.x, obj.transform.position.y, -0.7f);
                        numVolumesCreated++;
                    }
                }

                GameObject canvas = GameObject.Find("Canvas");
                canvas.SetActive(false);
            }
            else
            {
                Debug.LogError("Could not find any DICOM files to import");
            }
        }
    }
}
