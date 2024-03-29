using System.Linq;
using System.Text;
using UnityEngine;

public class VolumePosition : MonoBehaviour
{
    private NetworkManager networkManager;

    private Vector3 oldPosition = Vector3.zero;
    private Vector3 oldEulerAngles = Vector3.zero;

    private int MSG_LENGTH = 9;

    private Transform _transform;

    private void Awake()
    {
        networkManager = GameObject.Find("Network Manager").GetComponent<NetworkManager>();
    }

    private void Start()
    {
        _transform = transform;

        networkManager.websocket.OnMessage += (bytes) =>
        {
            if (!networkManager.isMaster)
            {
                if (bytes.Length > MSG_LENGTH)
                {
                    string code = Encoding.UTF8.GetString(bytes, 0, MSG_LENGTH);
                    int dataLength = bytes.Length - MSG_LENGTH;
                    byte[] data = new byte[dataLength];
                    data = bytes.Skip(MSG_LENGTH).Take(dataLength).ToArray();

                    if (code.Equals("objectRot"))
                    {
                        Rotation rotation = (Rotation)networkManager.ParseMessage(data);

                        _transform.eulerAngles = new Vector3(rotation.rX, rotation.rY, rotation.rZ);
                    }
                    else if (code.Equals("objectMov"))
                    {
                        Movement movement = (Movement)networkManager.ParseMessage(data);
                        _transform.position = new Vector3(movement.pX, movement.pY, movement.pZ);
                    }
                }
            }
        };
    }

    private async void FixedUpdate()
    {
        if (networkManager.isMaster)
        {
            if (oldPosition != _transform.position)
            {
                oldPosition = _transform.position;

                Movement movement = new Movement()
                {
                    pX = _transform.position.x,
                    pY = _transform.position.y,
                    pZ = _transform.position.z
                };

                await networkManager.Send("objectMov", movement);
            }

            if (oldEulerAngles != _transform.rotation.eulerAngles)
            {
                oldEulerAngles = _transform.rotation.eulerAngles;

                Rotation rotation = new Rotation()
                {
                    rX = _transform.rotation.eulerAngles.x,
                    rY = _transform.rotation.eulerAngles.y,
                    rZ = _transform.rotation.eulerAngles.z
                };

                await networkManager.Send("objectRot", rotation);
            }
        }
    }
}
