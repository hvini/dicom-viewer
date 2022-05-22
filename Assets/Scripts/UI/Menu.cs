using UnityEngine;
using UnityEngine.UI;

public class Menu : MonoBehaviour
{
    public GameObject patientsBtn;
    public GameObject studiesBtn;
    public GameObject seriesBtn;

    public GameObject patientsTable;
    public GameObject studiesTable;
    public GameObject seriesTable;

    public void HideAllTabs()
    {
        patientsTable.SetActive(false);
        studiesTable.SetActive(false);
        seriesTable.SetActive(false);

        patientsBtn.GetComponent<Button>().image.color = new Color32(200, 200, 200, 128);
        studiesBtn.GetComponent<Button>().image.color = new Color32(200, 200, 200, 128);
        seriesBtn.GetComponent<Button>().image.color = new Color32(200, 200, 200, 128);
    }

    public void ShowPatientsTab()
    {
        HideAllTabs();
        patientsTable.SetActive(true);
        patientsBtn.GetComponent<Button>().image.color = new Color32(255, 255, 255, 255);
    }

    public void ShowStudiesTab()
    {
        HideAllTabs();
        studiesTable.SetActive(true);
        studiesBtn.GetComponent<Button>().image.color = new Color32(255, 255, 255, 255);
    }

    public void ShowSeriessTab()
    {
        HideAllTabs();
        seriesTable.SetActive(true);
        seriesBtn.GetComponent<Button>().image.color = new Color32(255, 255, 255, 255);
    }
}
