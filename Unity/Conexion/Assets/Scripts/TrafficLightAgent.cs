using System.Collections;
using UnityEngine;

public class TrafficLightAgent : AgentComponent
{
    public Step[] steps;
    float dt;
    int index = 0;
    public Renderer[] renderers;
    Material[] lights;
    [ColorUsage(true, true)]
    public Color[] lightsOn;
    [ColorUsage(true, true)]
    public Color[] lightsOff;

    public override void Start()
    {
        lights = new Material[] { renderers[0].material, renderers[1].material, renderers[2].material };
    }

    public override void Update()
    {
        if(steps == null) { return; }
        dt += Time.deltaTime;
        Step currentStep = steps[index];
        if (currentStep.StepInfo.time < dt)
        {
            index++;
            if (index > steps.Length - 1)
            {
                index = steps.Length - 1;
                enabled = false;
            }
            ChangeLight(currentStep.StepInfo.state);
        }
    }

    void ChangeLight(int index)
    {
        for (int i = 0; i < lights.Length; i++)
        {
            lights[i].SetColor("_EmissionColor", lightsOff[i]);
        }
        lights[index].SetColor("_EmissionColor", lightsOn[index]);
    }
}