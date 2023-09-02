using System.Collections;
using System.Collections.Generic;
using CandyCoded.env;
using UnityEngine;
using UnityEngine.UI;

public class SeriesTable : MonoBehaviour
{
    private Transform seriesEntryContainer;
    private Transform seriesEntryTemplate;
    private PythonAPI pyAPI;
    private List<Transform> seriesEntryTransformList;
    private string baseURL;

    private NetworkManager networkManager;

    private void Awake()
    {
        if (env.TryParseEnvironmentVariable("BASE_URL", out string url))
        {
            baseURL = url;
        }

        networkManager = GameObject.Find("Network Manager").GetComponent<NetworkManager>();
        pyAPI = GameObject.Find("PyAPI").GetComponent<PythonAPI>();
    }

    public IEnumerator GetStudySeries(string id, GameObject studiesTable)
    {
        DestroyAll(seriesEntryTransformList);

        string type = "series";
        yield return StartCoroutine(pyAPI.Get(baseURL + "studies/" + id + "/series", type));

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

        Text buttonLabel = button.GetComponentInChildren<Text>();
        if (series.bitspath == null) buttonLabel.text = "Download model";
        else buttonLabel.text = "Load model";

        button.gameObject.SetActive(true);
        button.onClick.AddListener(delegate { ActionButtonEvent(series); });

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

    async public void ActionButtonEvent(Series series)
    {
        if (series.bitspath != null) {
            //await networkManager.Send("masterObj", series);
            StartCoroutine(pyAPI.LoadModel(series));
        }
    }
}
