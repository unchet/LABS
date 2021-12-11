#version 120

varying vec3 l;
varying vec3 n;
varying vec4 color;
attribute vec3 abc;

void main(void)
{
    vec3 p = vec3 (gl_ModelViewMatrix * gl_Vertex);// transformed point to world space

    l = normalize ( vec3 ( 1.0, 1.0, 1.0 ) - p );
    n = normalize (gl_NormalMatrix * gl_Normal);// transformed n
    color = vec4(abc, 1.0);

    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
