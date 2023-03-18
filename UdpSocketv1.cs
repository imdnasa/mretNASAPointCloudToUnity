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

public class UdpSocketv1 : MonoBehaviour
{
    [HideInInspector] public bool isTxStarted = false;

    [SerializeField] string IP = "127.0.0.1"; // local host
    [SerializeField] int rxPort = 8000; // port to receive data from Python on
    [SerializeField] int txPort = 8001; // port to send data to Python on
    //public bool finished = true;

    //int i = 0; // DELETE THIS: Added to show sending data from Unity to Python via UDP

    // Create necessary UdpClient objects
    UdpClient client;
    IPEndPoint remoteEndPoint;
    Thread receiveThread; // Receiving Thread
    //byte[] imageData;
    //public Texture2D image;
   // private Texture2D texture;

    //private RenderTexture renderTexture;

    void Update() // DELETE THIS: Added to show sending data from Unity to Python via UDP
    {
        
        // Sending data from unity to python
        // SendData(gameObject.transform.rotation.eulerAngles.ToString());
        

        SendData(gameObject.transform.position.ToString());



        //Vestigal code for now
        //image = Resources.Load<Texture2D>("myTextureAsset");
        //image.name = "img1";

        //Texture2D tex = new Texture2D(512,512);
        //bool check = tex.LoadImage(imageData);
        //Debug.Log(check);



       /* string filePath = "Assets / PPTK Textures / img.png";

        byte[] fileData = System.IO.File.ReadAllBytes(filePath);
        texture = new Texture2D(512, 512);
        texture.LoadImage(fileData);




        Color[] pixels = texture.GetPixels();
        for (int i = 0; i < pixels.Length; i++)
        {
            Debug.Log("Pixel " + i + ": " + pixels[i]);
        }


        renderTexture = new RenderTexture(image.width, image.height, 0);
        Graphics.SetRenderTarget(renderTexture);
        Graphics.Blit(image, renderTexture);
        //Graphics.SetRenderTarget(null);

       
        
        //Vestigal Code
        //Debug.Log(imageData);
        //cube.GetComponent<Renderer>().material.mainTexture = tex;
       */

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
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);
                print(">> " + text);
                ProcessInput(text);
                //imageData = data;
               
             }
             catch (Exception err)
             {
                 print(err.ToString());
             }
         }
     }
    
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