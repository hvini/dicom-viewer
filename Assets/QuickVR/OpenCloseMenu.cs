using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using WebXR;

public class OpenCloseMenu : MonoBehaviour
{
    private WebXRController controller = null;

    private GameObject canvas = null;
    private bool canvasVisibility = true;

    void Awake()
    {
        canvas = GameObject.Find("Canvas");
        controller = gameObject.GetComponent<WebXRController>();
    }

    // Update is called once per frame
    void Update()
    {
        if (controller.GetButtonDown(WebXRController.ButtonTypes.ButtonA))
        {
            canvasVisibility = !canvasVisibility;
            canvas.SetActive(canvasVisibility);
        }
    }
}
