using UnityEngine;

public class FollowBody : MonoBehaviour
{
    private NetworkManager networkManager;

    private Vector3 oldPosition = Vector3.zero;

    [SerializeField]
    private Transform bodyTransform;

    private void Start()
    {
        networkManager = GameObject.Find("Network Manager").GetComponent<NetworkManager>();
    }

    async private void FixedUpdate()
    {
        if (networkManager.isMaster)
        {
            if (oldPosition != bodyTransform.position)
            {
                oldPosition = bodyTransform.position;

                Movement movement = new Movement()
                {
                    pX = bodyTransform.position.x,
                    pY = bodyTransform.position.y,
                    pZ = bodyTransform.position.z
                };

                await networkManager.Send("bodyPosit", movement);
            }
        }
    }
}
