using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System;

public class rami_SocketSender : MonoBehaviour
{
    private Socket socket;
    private Socket socket_in;

    private void Start()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket.Connect("localhost", 8001); // replace with your IP address and port number

        socket_in = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        socket_in.Connect("localhost", 8000);
    }

    private void Update()
    {
        Vector3 position = transform.position;
        string message = position.ToString();
        Debug.Log(message);
        byte[] buffer = Encoding.ASCII.GetBytes(message);
        socket.Send(buffer);

        // create an array to receive data from python code
        byte[] data = new byte[1024];

        socket_in.Receive(data);
        int length = BitConverter.ToInt32(data, 0);

        // Receive the image bytes
        socket_in.Receive(data, length, SocketFlags.None);

        // Decode the image bytes into a PNG image
        Texture2D texture = new Texture2D(1, 1);
        texture.LoadImage(data);
    }

    private void OnDestroy()
    {
        socket.Close();
        socket_in.Close();
    }
}
