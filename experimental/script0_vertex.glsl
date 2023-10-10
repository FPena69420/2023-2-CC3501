#version 330


in vec3 position;
uniform mat4 view_transform;

in vec3 color;

out vec3 fragColor;

void main()
{
    fragColor = color;
    gl_Position = view_transform * vec4(position, 1.0f);
}