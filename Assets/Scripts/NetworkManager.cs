using UnityEngine;
using NativeWebSocket;
using System.Threading.Tasks;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System;

public class NetworkManager : MonoBehaviour
{
    public WebSocket websocket;
    public bool isMaster { get; set; }

    private void Awake()
    {
        isMaster = false;
        websocket = new WebSocket("wss://172.17.56.238:3230");
    }

    // Start is called before the first frame update
    async void Start()
    {
        websocket.OnOpen += () =>
        {
            Debug.Log("Connection Open");
        };

        websocket.OnError += (e) =>
        {
            Debug.Log("Error! " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Connection closed!");
        };

        await websocket.Connect();
    }

    public async Task Send(string type, object obj)
    {
        if (websocket.State == WebSocketState.Open)
        {
            byte[] encodedMessage;

            byte[] encodedType = Encoding.UTF8.GetBytes(type);

            BinaryFormatter bf = new BinaryFormatter();

            using (var ms = new MemoryStream())
            {
                bf.Serialize(ms, obj);
                encodedMessage = ms.ToArray();
            }

            byte[] bytes = new byte[encodedType.Length + encodedMessage.Length];
            Buffer.BlockCopy(encodedType, 0, bytes, 0, encodedType.Length);
            Buffer.BlockCopy(encodedMessage, 0, bytes, encodedType.Length, encodedMessage.Length);

            await websocket.Send(bytes);
        }
    }

    public object ParseMessage(byte[] bytes)
    {
        if(bytes.Length > 0)
        {
            MemoryStream ms = new MemoryStream();
            BinaryFormatter bf = new BinaryFormatter();

            ms.Write(bytes, 0, bytes.Length);
            ms.Seek(0, SeekOrigin.Begin);

            object data = bf.Deserialize(ms);

            return data;
        }

        return null;
    }

    void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
            websocket.DispatchMessageQueue();
        #endif
    }

    private async void OnApplicationQuit()
    {
        await websocket.Close();
    }
}
