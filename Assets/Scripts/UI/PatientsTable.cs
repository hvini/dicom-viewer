using System.Collections;
using System.Collections.Generic;
using CandyCoded.env;
using UnityEngine;
using UnityEngine.UI;

public class PatientsTable : MonoBehaviour
{
    private Transform patientsEntryContainer;
    private Transform patientsEntryTemplate;
    private PythonAPI pyAPI;
    private List<Transform> patientsEntryTransformList;
    private string baseURL;

    private void Awake()
    {
        if (env.TryParseEnvironmentVariable("BASE_URL", out string url))
        {
            baseURL = url;
        }
    }

    public IEnumerator Start()
    {
        pyAPI = GameObject.Find("PyAPI").GetComponent<PythonAPI>();
        string type = "patients";
        yield return StartCoroutine(pyAPI.Get(baseURL + "patients/", type));

        patientsEntryContainer = transform.Find("PatientsEntryContainer");
        patientsEntryTemplate = patientsEntryContainer.Find("PatientsEntryTemplate");

        patientsEntryTemplate.gameObject.SetActive(false);

        patientsEntryTransformList = new List<Transform>();
        foreach (Patients patient in pyAPI.patients)
        {
            CreatePatientEntryTransform(patient, patientsEntryContainer, patientsEntryTransformList);
        }
    }

    private void CreatePatientEntryTransform(Patients patient, Transform container, List<Transform> transformList)
    {
        float templateHeight = 30f;

        Transform entryTransform = Instantiate(patientsEntryTemplate, container);
        RectTransform entryRectTransform = entryTransform.GetComponent<RectTransform>();
        entryRectTransform.anchoredPosition = new Vector2(0, -templateHeight * transformList.Count);
        entryTransform.gameObject.SetActive(true);

        entryTransform.Find("NameTxt").GetComponent<Text>().text = patient.name;
        entryTransform.Find("BirthDateTxt").GetComponent<Text>().text = patient.birthDate;

        Button button = entryTransform.Find("ActionBtn").GetComponent<Button>();
        button.gameObject.SetActive(true);
        button.onClick.AddListener(delegate { ActionButtonEvent(patient.id); });

        transformList.Add(entryTransform);
    }

    public void ActionButtonEvent(int id)
    {
        StudiesTable studiesTable = GameObject.Find("Canvas").transform.Find("StudiesTable").GetComponent<StudiesTable>();

        transform.gameObject.SetActive(true);
        studiesTable.transform.gameObject.SetActive(true);
        StartCoroutine(studiesTable.GetPatientStudies(id, transform.gameObject));
    }
}
