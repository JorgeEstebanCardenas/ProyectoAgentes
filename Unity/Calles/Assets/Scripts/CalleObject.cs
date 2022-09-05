using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class CalleObject
{
    public CalleObject(Vector2 start1, Vector2 end1)
    {
        start = start1;
        end = end1;

    }
    
    public Vector2 start;

    public Vector2 end;

    /*
    public double peso;
  
    public double longitud; */
}

public class Puntos
{
    
}

public class Ciudad
{    
    public CalleObject calle1 = new CalleObject(new Vector2(-8,6),new Vector2(8,6));

    public CalleObject calle2 = new CalleObject(new Vector2(8, 6), new Vector2(8, -6));

    public CalleObject calle3 = new CalleObject(new Vector2(8, -6), new Vector2(-8, -6));






}