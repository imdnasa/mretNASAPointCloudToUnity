using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System;

public class rami_SocketSender : MonoBehaviour
{
    private Socket socket;

    private void Start()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Udp);
        socket.Connect("localhost", 8001); // replace with your IP address and port number

    }

    private void Update()
    {
        string message = transform.position.ToString();
        Debug.Log(message);
        byte[] buffer = Encoding.ASCII.GetBytes(message);
        socket.Send(buffer); 

    }

    private void OnDestroy()
    {
        socket.Close(); 
    }
}
