using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class SocketSender : MonoBehaviour
{
    private Socket socket;

    private void Start()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.Connect("localhost", 8001); // replace with your IP address and port number
    }

    private void Update()
    {
        Vector3 position = transform.position;
        string message = $"{position.x},{position.y},{position.z},";
        Debug.Log(message);
        byte[] buffer = Encoding.ASCII.GetBytes(message);
        socket.Send(buffer);
    }

    private void OnDestroy()
    {
        socket.Close();
    }
}
