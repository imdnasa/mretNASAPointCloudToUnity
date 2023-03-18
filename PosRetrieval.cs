using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class PosRetrieval : MonoBehaviour
{
    // Start is called before the first frame update

    void Start()
    {

        writeString(gameObject.transform.rotation.eulerAngles.ToString());
    }
    static void writeString(string rot) {
        string path = "Assets/Resources/test.txt";
        StreamWriter writer = new StreamWriter(path, true);
        writer.WriteLine(rot);
        writer.Close();
    }
    // Update is called once per frame
    void Update()
    {
        //Debug.Log(gameObject.transform.position);
        writeString(gameObject.transform.position.ToString());
        writeString(gameObject.transform.rotation.eulerAngles.ToString());
    }
}
