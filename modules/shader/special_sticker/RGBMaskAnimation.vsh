
attribute vec4 a_position;
attribute vec2 a_texCoord;
attribute vec4 a_color;

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;
uniform mat4 CC_PMatrix;

void main()
{
    v_fragmentColor = a_color;
    v_texCoord = a_texCoord;

    gl_Position = CC_PMatrix * a_position;
}
