using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Move : MonoBehaviour
{
    Vector3 initialPosition;
    public Vector3 offsetPosition;
    public float speed = 0.1f;

    private void Start()
    {
        initialPosition = transform.position;
    }

    void Update()
    {
        //transform.position = initialPosition + offsetPosition;
        transform.Translate(speed * Time.deltaTime, 0, 0);// 1/60 = 16ms, 1/30 = 32ms
    }
}
