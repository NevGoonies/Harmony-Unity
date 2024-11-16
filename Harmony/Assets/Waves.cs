using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class Waves : MonoBehaviour
{
    public int Dimensions = 10;
    protected MeshFilter meshFilter;
    protected Mesh mesh;
    
    // Start is called before the first frame update
    void Start()
    {
        // Mesh Setup
        Mesh = new Mesh();
        Mesh.name = gameObject.name;

        Mesh.vertices = GenerateVerts();
        Mesh.triangles = GenerateTries();
        Mesh.RecalculateBounds();

        MeshFilter = gameObject.AddComponent<MeshFilter>();
        MeshFilter.mesh = Mesh;
    }

    private Vector3[] GenerateVerts()
    {
        var verts = new Vector3[(Dimensions + 1) * (Dimensions + 1)];
        
        //equally distributed verts
        for (int x = 0; x <= Dimensions; x++)
            for (int z = 0; z <= Dimensions; z++)
                verts[index(x, z)] = new Vector3(x, 0, z);

        return verts;
    }

    private int index(int x, int z)
    {
        return x * (Dimensions + 1) + z;
    }

    private int[] GenerateTries()
    {
        var tries = new int[Mesh.vertices.Length * 6];
        
        //two triangles are one tile
        for (int x = 0; x < Dimensions; x++)
        {
            for ()
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
