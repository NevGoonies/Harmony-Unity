using System.IO;
using UnityEngine;
using UnityEngine.Rendering.HighDefinition;

public class ContinouseReader : MonoBehaviour
{

    public string filePath = "C:\\Users\\Administrator\\Documents\\NatHacks\\show.txt";
    public GameObject ocean;
    float damp1;
    float damp2;
    float speed;

    public float currentDamp = 0f;
    public float currentDamp2 = 0f;
    public float currentSpeed = 0f;

    public float lerpSpeed = 0.1f;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        StartCoroutine(ReadFileCoroutine());
    }

    // Update is called once per frame
    void Update()
    {
        currentDamp = Mathf.Lerp(currentDamp, damp1, lerpSpeed * Time.deltaTime);
        currentDamp2 = Mathf.Lerp(currentDamp2, damp2, lerpSpeed * Time.deltaTime);
        currentSpeed = Mathf.Lerp(currentSpeed, speed, lerpSpeed * Time.deltaTime);

        ocean.GetComponent<WaterSurface>().largeBand0Multiplier = currentDamp;
        ocean.GetComponent<WaterSurface>().largeBand1Multiplier = currentDamp2;
        ocean.GetComponent<WaterSurface>().largeCurrentSpeedValue = currentSpeed;
    }

    private System.Collections.IEnumerator ReadFileCoroutine()
    {
        while (true)
        {
            float wait_time = 0.5f;
            try
            {
                using (StreamReader sr = new StreamReader(filePath))
                {
                    string line;
                    {
                        // Read a new line if available
                        line = sr.ReadLine();

                        if (line != null)
                        {
                            Debug.Log($"Read: {line}");
                            float anxietyness = float.Parse(line);

                            
                            if (anxietyness < 1.5f)
                            {
                                damp1 = 0; damp2 = 0;
                                speed = 0.5f;
                            } else if(anxietyness < 2f)
                            {
                                damp1 = 0.3f; damp2 = 0.3f;
                                speed = 1f;
                            } else if (anxietyness < 2.7f)
                            {
                                damp1 = 0.6f; damp2 = 0.6f;
                                speed = 5f;
                            } else if (anxietyness < 3.5f)
                            {
                                damp1 = 0.85f; damp2 = 0.85f;
                                speed = 10f;
                            } else
                            {
                                damp1 = 1f; damp2 = 1f;
                                speed = 25f;
                            }


                            

                        }
                        else
                        {
                            // Wait briefly before checking for more data

                        }
                    }
                }
            }
            catch {
                wait_time = 0.1f;
                Debug.Log("Read file content error");
                
            }
            yield return new WaitForSeconds(wait_time);
        }
    }
}
