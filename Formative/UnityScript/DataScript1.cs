/*
 * This script is for Task1
 */

using System.Collections.Generic;
using System.IO;
using Unity.VisualScripting;
using UnityEngine;

public class DataScript1 : MonoBehaviour
{
    public string InputFolder = @"Result Raw";
    public string OutputFolder = @"Result Processed";

    private List<string> PostureList = new List<string>{"Standing", "Lying"};
    private Dictionary<string, string> DirectionDict = new Dictionary<string, string>{
        {"0", "Right"}, {"45", "UpRight"}, {"90", "Up"}, {"135", "UpLeft"}, {"180", "Left"}, {"225", "DownLeft"}, {"270", "Down"}, {"315", "DownRight"}
    };

    // Start is called before the first frame update
    async void Start()
    {
        for (int participant = 1; participant <= 16; participant++)
        {
            foreach (string posture in PostureList)
            {
                // Create output file
                string OutputFile = Path.Combine(OutputFolder, "Formative_T1_P" + participant.ToString() + "_" + posture.ToString() + "_ReCalculate.csv");
                FileStream fs = new FileStream(OutputFile, FileMode.OpenOrCreate);
                StreamWriter writer = new StreamWriter(fs);

                string Header = "Direction,tCount,MaxViewingRange,StartVector,EndVector";
                await writer.WriteLineAsync(Header);

                // Read data from input file
                string InputFile = Path.Combine(InputFolder, "Formative_T1_P" + participant.ToString() + "_" + posture.ToString() + ".csv");

                if (File.Exists(InputFile)) {
                    using (StreamReader reader = new StreamReader(InputFile)) {
                        Debug.Log("Processing... " + InputFile);

                        reader.ReadLine(); // skip header

                        // Get UpVector
                        Vector3 UpStartVector = new Vector3(0, 0, 0);
                        Vector3 UpEndVector = new Vector3(0, 0, 0);
                        Vector3 UpVector = new Vector3(0, 0, 0);
                        while (!reader.EndOfStream) {
                            string line = await reader.ReadLineAsync();
                            string[] readValues = line.Split(',');

                            int tCount = int.Parse(readValues[2]);
                            string DirectionStr = DirectionDict[readValues[3]];
                            string StartVectorStr = readValues[5];
                            string EndVectorStr = readValues[6];

                            if (DirectionStr == "Up") {
                                Vector3 StartVector = ParseVectorString(StartVectorStr);
                                Vector3 EndVector = ParseVectorString(EndVectorStr);

                                UpStartVector += StartVector;
                                UpEndVector += EndVector;

                                if (tCount == 3) {
                                    UpVector = GetUpVector(UpStartVector.normalized, UpEndVector.normalized);
                                    break;
                                }
                            }
                        }

                        Debug.Log("UpVector: " + UpVector.ToString());
                        if (UpVector == new Vector3(0, 0, 0)) {
                            Debug.Log("UpVector not set!");
                            continue;
                        }

                        // Reset reader to start of file
                        reader.DiscardBufferedData();
                        reader.BaseStream.Seek(0, SeekOrigin.Begin);
                        reader.ReadLine(); // skip header

                        while (!reader.EndOfStream) {
                            string line = await reader.ReadLineAsync();
                            string[] readValues = line.Split(',');

                            string DirectionStr = DirectionDict[readValues[3]];
                            string StartVectorStr = readValues[5];
                            string EndVectorStr = readValues[6];

                            Vector3 StartVector = ParseVectorString(StartVectorStr);
                            Vector3 EndVector = ParseVectorString(EndVectorStr);
                            float MaxViewingRange = Vector3.SignedAngle(StartVector, EndVector, UpVector);

                            string NewLine = DirectionStr + ',' + readValues[2] + ','
                                + MaxViewingRange.ToString() + ',' + readValues[5] + ',' + readValues[6];

                            await writer.WriteLineAsync(NewLine);
                        }

                        Debug.Log("Processed Successed: " + OutputFile);
                    }

                    writer.Close();
                    fs.Close();
                }
            }
        }

        Debug.Log("Processing Done!");
    }

    Vector3 ParseVectorString(string VectorStr)
    {
        VectorStr = VectorStr.Trim('(', ')');
        VectorStr = VectorStr.Replace("*", "");
        string[] VectorValues = VectorStr.Split(' ');

        return new Vector3(float.Parse(VectorValues[0]), float.Parse(VectorValues[1]), float.Parse(VectorValues[2]));
    }

    Vector3 GetUpVector(Vector3 UpStartVector, Vector3 UpEndVector)
    {
        Vector3 LeftVector = Vector3.Cross(UpStartVector, UpEndVector);
        return Vector3.Cross(LeftVector, UpStartVector);
    }

    float GetMaxViewingRange(Vector3 StartVector, Vector3 EndVector)
    {
        return Vector3.SignedAngle(StartVector, EndVector, Vector3.up);
    }

    // Update is called once per frame
    void Update()
    {
    }
}
