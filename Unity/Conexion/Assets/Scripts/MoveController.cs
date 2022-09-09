using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveController : MonoBehaviour
{
    public Step[] steps;
    float dt;
    int index = 0;

    void Update()
    {
        dt += Time.deltaTime;
        Step currentStep = steps[index];
        if(currentStep.Stepinfo.time < dt)
        {
            index++;
            //Debug.Log(index);
            if(index > steps.Length - 1)
            {
                index = steps.Length - 1;
                enabled = false;
            }
            return;
        }

        Vector3 postion = new Vector3(currentStep.Stepinfo.positionX, 0, currentStep.Stepinfo.positionY);
        transform.localPosition = postion;// Tiene que ser local position para que sea afectado por el GameObject Pivot.
    }
}
