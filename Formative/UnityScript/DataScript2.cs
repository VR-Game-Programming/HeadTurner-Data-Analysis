/*
 * This script is for Task2
 */

using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class DataScript2 : MonoBehaviour
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
                string OutputFile = Path.Combine(OutputFolder, "Formative_O3_P" + participant.ToString() + "_" + posture.ToString() + "_ReCalculate.csv");
                FileStream fs = new FileStream(OutputFile, FileMode.OpenOrCreate);
                StreamWriter writer = new StreamWriter(fs);

                string Header = "Direction,tCount,Time,StartRotation,HeadRotation,HeadYaw,HeadPitch,TrunkRotation,TrunkYaw,TrunkPitch";
                await writer.WriteLineAsync(Header);

                // Read data from input file
                string InputFile = Path.Combine(InputFolder, "Formative_O3_P" + participant.ToString() + "_" + posture.ToString() + ".csv");

                if (File.Exists(InputFile)) {
                    using (StreamReader reader = new StreamReader(InputFile)) {
                        Debug.Log("Processing... " + InputFile);

                        reader.ReadLine(); // skip header

                        int lastcount = 0;
                        Quaternion HeadBaseRotation = Quaternion.identity;
                        Quaternion TrunkBaseRotation = Quaternion.identity;

                        while (!reader.EndOfStream) {
                            string line = await reader.ReadLineAsync();
                            string[] readValues = line.Split(',');

                            int count = int.Parse(readValues[1]);
                            string DirectionStr = DirectionDict[readValues[0]];
                            string HeadRotationStr = readValues[3];
                            string TrunkRotationStr = readValues[6];
                            string StartRotationStr = readValues[9];

                            Quaternion StartRotation = ParseRotationString(StartRotationStr);
                            Quaternion HeadRotation = ParseRotationString(HeadRotationStr);
                            Quaternion TrunkRotation = ParseRotationString(TrunkRotationStr);

                            Quaternion HeadDiffRotation = HeadRotation * Quaternion.Inverse(StartRotation);
                            Quaternion TrunkDiffRotation = TrunkRotation * Quaternion.Inverse(StartRotation);

                            if (count != lastcount) {
                                lastcount = count;
                                HeadBaseRotation = HeadDiffRotation;
                                TrunkBaseRotation = TrunkDiffRotation;
                            }

                            /*
                             *  Pitch: Up positive, Down negative
                             *  Yaw: Right positive, Left negative
                             */

                            float HeadYaw, HeadPitch, TrunkYaw, TrunkPitch;
                            if (posture == "Standing") {
                                HeadYaw = CorrectionAngle(HeadDiffRotation.eulerAngles.y - HeadBaseRotation.eulerAngles.y);
                                HeadPitch = CorrectionAngle(HeadDiffRotation.eulerAngles.x - HeadBaseRotation.eulerAngles.x);
                                TrunkYaw = CorrectionAngle(TrunkDiffRotation.eulerAngles.y - TrunkBaseRotation.eulerAngles.y);
                                TrunkPitch = CorrectionAngle(TrunkDiffRotation.eulerAngles.z - TrunkBaseRotation.eulerAngles.z);
                            }
                            else {
                                HeadYaw = CorrectionAngle(HeadDiffRotation.eulerAngles.z - HeadBaseRotation.eulerAngles.z);
                                HeadPitch = CorrectionAngle(HeadDiffRotation.eulerAngles.x - HeadBaseRotation.eulerAngles.x);
                                TrunkYaw = CorrectionAngle(TrunkDiffRotation.eulerAngles.z - TrunkBaseRotation.eulerAngles.z);
                                TrunkPitch = CorrectionAngle(TrunkDiffRotation.eulerAngles.x - TrunkBaseRotation.eulerAngles.x);
                            }

                            string NewLine = DirectionStr + "," + readValues[1] + "," + readValues[2] + "," + StartRotation.ToString().Replace(",", "*") + ","
                                + HeadRotation.ToString().Replace(",", "*") + "," + HeadYaw.ToString() + "," + HeadPitch.ToString() + ","
                                + TrunkRotation.ToString().Replace(",", "*") + "," + TrunkYaw.ToString() + "," + TrunkPitch.ToString();


                            await writer.WriteLineAsync(NewLine);
                        }
                    }

                    writer.Close();
                    fs.Close();
                }
            }
        }

        Debug.Log("Processing Done!");
    }

    Quaternion ParseRotationString(string RotationStr)
    {
        RotationStr = RotationStr.Trim('(', ')');
        RotationStr = RotationStr.Replace("*", "");
        string[] RotationValues = RotationStr.Split(' ');

        return Quaternion.Euler(float.Parse(RotationValues[0]), float.Parse(RotationValues[1]), float.Parse(RotationValues[2]));
    }

    float CorrectionAngle(float angle)
    {
        if (angle > 180) {
            angle -= 360;
        }
        else if (angle < -180) {
            angle += 360;
        }

        return angle;
    }

    // Update is called once per frame
    void Update()
    {
    }
}
