#version 120

varying vec3 l;
varying vec3 n;
varying vec4 color;

void main (void)
{
    const vec4  diffColor = vec4 ( 0.5, 0.5, 0.5, 1.0 );
    const vec4 amb = vec4 (0.3, 0.3, 0.3, 1.0);

    vec3 n2   = normalize ( n );
    vec3 l2   = normalize ( l );
    vec4 diff = color * diffColor * max ( dot ( n2, l2 ), 0.0 );

    gl_FragColor = 0.8 * diff + color * amb;
}
