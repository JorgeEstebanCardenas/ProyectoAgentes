using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarAgent : AgentComponent
{
    public Transform target;
    public float speed = 1;
    public float rotationSpeed = 1;
    Vector3 lastPosition;

    public override void Update()
    {
        float delta = speed * Time.deltaTime;
        transform.position = Vector3.MoveTowards(transform.position, target.position, delta);

        var movementDirection = lastPosition - transform.position;
        // Validates last position and current position are not the same.
        if (movementDirection != Vector3.zero)
        {
            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                Quaternion.LookRotation(-movementDirection),
                Time.deltaTime * rotationSpeed);
        }
        
        lastPosition = transform.position;
    }
}
