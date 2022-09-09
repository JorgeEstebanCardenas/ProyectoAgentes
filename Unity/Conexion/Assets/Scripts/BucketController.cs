using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BucketController : MonoBehaviour
{
    public Animator m_animator;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            m_animator.SetTrigger("TriggerParam");
        }
    }
}
