using UnityEngine;
using WebXR;

public class FollowHead : MonoBehaviour
{
    [SerializeField]
    private WebXRCamera webXRCamera = null;

    private Transform _transform;

    private NetworkManager networkManager;

    private Vector3 oldEulerAngles = Vector3.zero;
    private Vector3 oldPosition = Vector3.zero;

    void Start()
    {
        _transform = transform;
        networkManager = GameObject.Find("Network Manager").GetComponent<NetworkManager>();
    }

    void Update()
    {
        _transform.localPosition = webXRCamera.GetLocalPosition();
        _transform.rotation = webXRCamera.GetLocalRotation();
    }

    async private void FixedUpdate()
    {
        if (networkManager.isMaster)
        {
            if (oldEulerAngles != webXRCamera.GetLocalRotation().eulerAngles)
            {
                oldEulerAngles = webXRCamera.GetLocalRotation().eulerAngles;

                Rotation rotation = new Rotation()
                {
                    rX = webXRCamera.GetLocalRotation().eulerAngles.x,
                    rY = webXRCamera.GetLocalRotation().eulerAngles.y,
                    rZ = webXRCamera.GetLocalRotation().eulerAngles.z
                };

                await networkManager.Send("headRotat", rotation);
            }
            else if (oldPosition != webXRCamera.GetLocalPosition())
            {
                oldPosition = webXRCamera.GetLocalPosition();

                Movement movement = new Movement()
                {
                    pX = webXRCamera.GetLocalPosition().x,
                    pY = webXRCamera.GetLocalPosition().y,
                    pZ = webXRCamera.GetLocalPosition().z
                };

                await networkManager.Send("headMovem", movement);
            }
        }
    }
}
