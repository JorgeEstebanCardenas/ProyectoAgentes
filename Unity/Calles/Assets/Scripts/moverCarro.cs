using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UIElements;



public class moverCarro : MonoBehaviour
{
    public float speed = 1;


    private Ciudad ciudad = new Ciudad();

    private Vector2 start;

    private Vector2 end;

    private Vector2 direction;

    void Start()
    {
        start = ciudad.calle1.start;
        end = ciudad.calle1.end;

        transform.position = start;

        

        direction = end - start;

        //transform.Rotate()

        direction.Normalize();

        Debug.Log(ciudad);
    }

    // Update is called once per frame
    void Update()
    {
        Quaternion rotation = Quaternion.LookRotation(direction);
        transform.rotation = Quaternion.Lerp(transform.rotation, rotation, speed * Time.time);
        transform.Rotate(0, -90, 0);

        transform.position = Vector2.MoveTowards(transform.position, end, speed * Time.deltaTime);

        //Debug.Log(transform.position);
    }
}
