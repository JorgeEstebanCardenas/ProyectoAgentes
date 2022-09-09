using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationCoroutine : MonoBehaviour
{
    public float duration = 3;
    float durationDt = 0;
    public Color initialColor;
    public Color finalColor;
    Material m_material;
    public Renderer m_renderer;
    public float intensity = 1;

    private void Start()
    {
        m_material = m_renderer.material;

        m_material.SetColor("_BaseColor", initialColor);
        Invoke("StartCoroutineDelay", 1);
    }

    void StartCoroutineDelay()
    {
        StartCoroutine(StartAnimation());
    }

    IEnumerator StartAnimation()
    {

        while (true)
        {
            durationDt += Time.deltaTime;
            if (durationDt >= duration)
            {
                break;
            }

            float t = durationDt / duration;
            Color currentColor = Color.Lerp(initialColor, finalColor, t);
            m_material.SetColor("_BaseColor", currentColor * intensity);

            yield return null;
        }
    }
}
