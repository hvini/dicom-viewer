using System.Collections;
using System.Collections.Generic;
using CandyCoded.env;
using UnityEngine;
using UnityEngine.UI;

public class StudiesTable : MonoBehaviour
{
    private Transform studiesEntryContainer;
    private Transform studiesEntryTemplate;
    private PythonAPI pyAPI;
    private List<Transform> studiesEntryTransformList;
    private string baseURL;

    private void Awake()
    {
        if (env.TryParseEnvironmentVariable("BASE_URL", out string url))
        {
            baseURL = url;
        }
    }

    public IEnumerator GetPatientStudies(string id, GameObject patientsTable)
    {

        DestroyAll(studiesEntryTransformList);

        pyAPI = GameObject.Find("PyAPI").GetComponent<PythonAPI>();
        string type = "studies";
        yield return StartCoroutine(pyAPI.Get(baseURL + "patients/" + id + "/studies", type));

        patientsTable.SetActive(false);

        studiesEntryContainer = transform.Find("StudiesEntryContainer");
        studiesEntryTemplate = studiesEntryContainer.Find("StudiesEntryTemplate");

        studiesEntryTemplate.gameObject.SetActive(false);

        studiesEntryTransformList = new List<Transform>();
        foreach (Studies study in pyAPI.studies)
        {
            CreateStudiesEntryTransform(study, studiesEntryContainer, studiesEntryTransformList);
        }
    }

    private void CreateStudiesEntryTransform(Studies study, Transform container, List<Transform> transformList)
    {
        float templateHeight = 30f;

        Transform entryTransform = Instantiate(studiesEntryTemplate, container);
        RectTransform entryRectTransform = entryTransform.GetComponent<RectTransform>();
        entryRectTransform.anchoredPosition = new Vector2(0, -templateHeight * transformList.Count);
        entryTransform.gameObject.SetActive(true);

        entryTransform.Find("InstanceUIDTxt").GetComponent<Text>().text = study.instanceUID;
        entryTransform.Find("DescriptionTxt").GetComponent<Text>().text = study.description;
        entryTransform.Find("TimeTxt").GetComponent<Text>().text = study.time;

        Button button = entryTransform.Find("ActionBtn").GetComponent<Button>();
        button.gameObject.SetActive(true);
        button.onClick.AddListener(delegate { ActionButtonEvent(study.instanceUID); });

        transformList.Add(entryTransform);
    }

    private void DestroyAll(List<Transform> patientEntryTransformList)
    {
        if (patientEntryTransformList != null && patientEntryTransformList.Count > 0)
        {
            foreach (Transform transform in patientEntryTransformList)
            {
                Destroy(transform.gameObject);
            }
        }
    }

    public void ActionButtonEvent(string id)
    {
        SeriesTable seriesTable = GameObject.Find("Canvas").transform.Find("SeriesTable").GetComponent<SeriesTable>();

        transform.gameObject.SetActive(true);
        seriesTable.transform.gameObject.SetActive(true);
        StartCoroutine(seriesTable.GetStudySeries(id, transform.gameObject));
    }
}