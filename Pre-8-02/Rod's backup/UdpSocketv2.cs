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

public class UdpSocketv2 : MonoBehaviour
{
    //Data fields needed for the Socket
    [SerializeField] string IP = "127.0.0.1"; // local host
    [SerializeField] int rxPort = 8000; // port to receive data from Python on
    [SerializeField] int txPort = 8001; // port to send data to Python on
    public int dbgInc = 0; // debug incrementer
    public float accumulatedFPS = 0;

    // Create necessary UdpClient objects
    UdpClient client;
    IPEndPoint remoteEndPoint;

    void Start()
    {
        Application.targetFrameRate = 50;
    }

    void Awake()
    {

        //Sets up the UDP Sockets and Clients
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), txPort);
        client = new UdpClient(rxPort);

        Debug.Log("UDP Comms Initialised");

    }

    void Update() 
    {
        SendData(gameObject.transform.position.ToString()); //SENDS POSITIONAL DATA
        //string message = "UNITY---" + dbgInc.ToString();
        //SendData(message);
        dbgInc++;
        accumulatedFPS += 1 / Time.unscaledDeltaTime;
        Debug.Log(accumulatedFPS / dbgInc);
    }

    public void SendData(string message) // Use to send data to Python
    {
        try
        {
            //Debug.Log(message);
            byte[] data = Encoding.UTF8.GetBytes(message);//message is the string containing the data
            //client.Client.SendBufferSize = 0;
            client.Send(data, data.Length, remoteEndPoint);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }
     
    //Prevent crashes - close client properly!
    
    void OnDisable()
    {
        client.Close();
    } 
    
}