/*
Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

Use at your own risk
Use under the Apache License 2.0

Modified by: 
Youssef Elashry 12/2020 (replaced obsolete functions and improved further - works with Python as well)
Based on older work by Sandra Fang 2016 - Unity3D to MATLAB UDP communication - [url]http://msdn.microsoft.com/de-de/library/bb979228.aspx#ID0E3BAC[/url]
*/

using UnityEngine;
using System.Collections;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UdpSocket : MonoBehaviour
{
    [HideInInspector] public bool isTxStarted = false;

    [SerializeField] string IP = "127.0.0.1"; // local host
    [SerializeField] int rxPort = 8000; // port to receive data from Python on
    [SerializeField] int txPort = 8001; // port to send data to Python on

    //int i = 0; // DELETE THIS: Added to show sending data from Unity to Python via UDP

    // Create necessary UdpClient objects
    UdpClient client;
    IPEndPoint remoteEndPoint;
    Thread receiveThread; // Receiving Thread

   /* void Start() {
        IEnumerator coro = ReceiveData();
        client = new UdpClient(rxPort);
        StartCoroutine(coro);
    
    }
   */

    //public void ReceiveDataStart() {
        //StartCoroutine(ReceiveData());
    //}

    void Update() // DELETE THIS: Added to show sending data from Unity to Python via UDP
    {
            
        SendData(gameObject.transform.position.ToString());
        Debug.Log(gameObject.transform.position.ToString());
        //SendData(gameObject.transform.rotation.eulerAngles.ToString());
        //ReceiveData();
        //i++;
        //yield return new WaitForSeconds(1f);
        //Debug.Log("Hellooo");
 
    }

    public void SendData(string message) // Use to send data to Python
    {
        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            client.Send(data, data.Length, remoteEndPoint);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }

    void Awake()
    {
        // Create remote endpoint (to Matlab) 
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), txPort);

        // Create local client
        client = new UdpClient(rxPort);

        // local endpoint define (where messages are received)
        // Create a new thread for reception of incoming messages
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        
        //ThreadPool.QueueUserWorkItem(o => ReceiveData());
        // Initialize (seen in comments window)
        Debug.Log("UDP Comms Initialised");

        //StartCoroutine(SendDataCoroutine()); // DELETE THIS: Added to show sending data from Unity to Python via UDP
    }

    // Receive data, update packets received
     private void ReceiveData()
     {
         while (true)
         {
             try
             {
                 IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse(IP), rxPort);
                /* byte[] data = client.Receive(ref anyIP);
                 string text = Encoding.UTF8.GetString(data);
                 print(">> " + text);
                 ProcessInput(text); */

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
             catch (Exception err)
             {
                 print(err.ToString());
             }
         }
     }
    

    /*IEnumerator ReceiveData()
    {
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, rxPort);
                byte[] data = client.Receive(ref anyIP); //changed to BeginReceive
                string text = Encoding.UTF8.GetString(data);
                Debug.Log(text);
            }
            catch (System.Exception e)
            {
                Debug.LogError(e);
                break;
            }
            yield return null;
        }
    }
 */
    private void ProcessInput(string input)
    {
        // PROCESS INPUT RECEIVED STRING HERE

        if (!isTxStarted) // First data arrived so tx started
        {
            isTxStarted = true;
        }
    }

    //Prevent crashes - close clients and threads properly!
    void OnDisable()
    {
        if (receiveThread != null)
            receiveThread.Abort();

        client.Close();
    }

}