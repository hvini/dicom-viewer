using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SeriesTable : MonoBehaviour
{
    private Transform seriesEntryContainer;
    private Transform seriesEntryTemplate;
    private PythonAPI pyAPI;
    private List<Transform> seriesEntryTransformList;

    public IEnumerator GetStudySeries(int id, GameObject studiesTable)
    {

        DestroyAll(seriesEntryTransformList);

        pyAPI = GameObject.Find("PyAPI").GetComponent<PythonAPI>();
        string type = "series";
        yield return StartCoroutine(pyAPI.Get(Constants.API_BASE_URL + "studies/" + id + "/series", type));

        studiesTable.SetActive(false);

        seriesEntryContainer = transform.Find("SeriesEntryContainer");
        seriesEntryTemplate = seriesEntryContainer.Find("SeriesEntryTemplate");

        seriesEntryTemplate.gameObject.SetActive(false);

        seriesEntryTransformList = new List<Transform>();
        foreach (Series series in pyAPI.series)
        {
            CreateSeriesEntryTransform(series, seriesEntryContainer, seriesEntryTransformList);
        }
    }

    private void CreateSeriesEntryTransform(Series series, Transform container, List<Transform> transformList)
    {
        float templateHeight = 30f;

        Transform entryTransform = Instantiate(seriesEntryTemplate, container);
        RectTransform entryRectTransform = entryTransform.GetComponent<RectTransform>();
        entryRectTransform.anchoredPosition = new Vector2(0, -templateHeight * transformList.Count);
        entryTransform.gameObject.SetActive(true);

        entryTransform.Find("InstanceUIDTxt").GetComponent<Text>().text = series.instanceUID;
        entryTransform.Find("DescriptionTxt").GetComponent<Text>().text = series.description;

        Button button = entryTransform.Find("ActionBtn").GetComponent<Button>();
        button.gameObject.SetActive(true);

        string path = "./dicom-api/" + series.filepath;
        button.onClick.AddListener(delegate { ActionButtonEvent(path); });

        transformList.Add(entryTransform);
    }

    private void DestroyAll(List<Transform> seriesEntryTransformList)
    {
        if (seriesEntryTransformList != null && seriesEntryTransformList.Count > 0)
        {
            foreach (Transform transform in seriesEntryTransformList)
            {
                Destroy(transform.gameObject);
            }
        }
    }

    public void ActionButtonEvent(string filepath)
    {
        CreateObject.CreateVolObject(filepath);
    }
}
