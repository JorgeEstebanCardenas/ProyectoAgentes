using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationManual : MonoBehaviour
{
    public float duration = 3;
    float durationDt = 0;
    public float speed = 1;
    public Vector3 direction = Vector3.up;
    public Vector3 rotation;

    void Update()
    {
        durationDt += Time.deltaTime;
        if(durationDt >= duration)
        {
            enabled = false;
        }

        transform.Translate(speed * Time.deltaTime * direction);
        transform.Rotate(rotation);
    }
}
