
#ifdef GL_ES
precision mediump float;
#endif

#define CARTESIAN_COORDINATE_TYPE 0
#define POLAR_COORDINATE_TYPE 1

#define ADD_BLEND_TYPE 0
#define SUB_BLEND_TYPE 1
#define MULTI_BLEND_TYPE 2
#define REPLACE_BLEND_TYPE 3
#define DISTORTION_BLEND_TYPE 4

const float PI = 3.141592653589793;
const float POLAR_CORRECTION = 0.159154943091895;

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform sampler2D u_maskTexture;
uniform sampler2D CC_Texture0;


// note: GLProgramState::getUniformValue 
uniform sampler2D u_red_blendTexture;
uniform vec2      u_red_tiling;
uniform vec2      u_red_offset;
uniform int       u_red_blendType;
uniform vec3      u_red_color;
uniform float     u_red_intensity;
uniform int       u_red_coordinateType;
uniform vec2      u_red_scrollVelocity;
uniform vec2      u_red_rotateCenter;
uniform float     u_red_rotateVelocity;

uniform sampler2D u_green_blendTexture;
uniform vec2      u_green_tiling;
uniform vec2      u_green_offset;
uniform int       u_green_blendType;
uniform vec3      u_green_color;
uniform float     u_green_intensity;
uniform int       u_green_coordinateType;
uniform vec2      u_green_scrollVelocity;
uniform vec2      u_green_rotateCenter;
uniform float     u_green_rotateVelocity;

uniform sampler2D u_blue_blendTexture;
uniform vec2      u_blue_tiling;
uniform vec2      u_blue_offset;
uniform int       u_blue_blendType;
uniform vec3      u_blue_color;
uniform float     u_blue_intensity;
uniform int       u_blue_coordinateType;
uniform vec2      u_blue_scrollVelocity;
uniform vec2      u_blue_rotateCenter;
uniform float     u_blue_rotateVelocity;

uniform float     u_animationTime;

float atan2(float y, float x)
{
    return x == 0.0 ? sign(y) * PI / 2.0 : atan(y, x);
}

vec2 convertPolarCoordinate(float x, float y)
{
    float r = sqrt((x * x) + (y * y));
    float theta = atan2(y, x);

    return vec2(r, theta);
}

vec4 blend(float cardAnimTime, vec4 baseColor, float maskColorRGB, sampler2D blendTexture,
           vec2 tiling, vec2 offset, int blendType, vec3 color, float intensity,
           int coordinateType, vec2 scrollVelocity, vec2 rotateCenter, float rotateVelocity)
{
#ifdef GL_ES
    highp vec2 textureCoord = vec2(v_texCoord.x * tiling.x + (offset.x * tiling.x),
                                   v_texCoord.y * tiling.y + (offset.y * tiling.y));
#else
    vec2 textureCoord = vec2(v_texCoord.x * tiling.x + (offset.x * tiling.x),
                             v_texCoord.y * tiling.y + (offset.y * tiling.y));
#endif
    float calculatedIntensity = maskColorRGB * intensity;

    if (coordinateType == POLAR_COORDINATE_TYPE) {  // Coordinate type 
        textureCoord = convertPolarCoordinate(textureCoord.x, textureCoord.y);
        textureCoord.y = (textureCoord.y * POLAR_CORRECTION) * 6.0;
    }

    // 
    textureCoord = vec2(textureCoord.x + cardAnimTime * scrollVelocity.x,
                        textureCoord.y + cardAnimTime * scrollVelocity.y);

    // 
    if (rotateVelocity != 0.0) {
        float angle = cardAnimTime * rotateVelocity;
        float sinX = sin(angle);
        float cosX = cos(angle);
        float sinY = sin(angle);
        float cosY = cos(angle);
        mat2 rotationMatrix = mat2(cosX, -sinX,
                                   sinY, cosX);
        textureCoord = (textureCoord - rotateCenter) * (rotationMatrix);
        textureCoord += rotateCenter;
    }

    // 
    textureCoord = fract(textureCoord);
    vec4 blendColor = v_fragmentColor * texture2D(blendTexture, textureCoord);
    vec4 resultTexture = blendColor * vec4(color, 1.0) * calculatedIntensity;
    if (blendType == ADD_BLEND_TYPE) {  // Blend type 
        return baseColor + vec4(resultTexture.xyz, 0.0);
    } else if (blendType == SUB_BLEND_TYPE) {  // Blend type 
        return baseColor - vec4(resultTexture.xyz, 0.0);
    } else if (blendType == MULTI_BLEND_TYPE) {  // Blend type 
        return baseColor * vec4(resultTexture.xyz, 1.0);
    } else if (blendType == REPLACE_BLEND_TYPE) {  // Blend type 
        return resultTexture;
    } else if (blendType == DISTORTION_BLEND_TYPE) {  // Blend type 
        vec2 distortedCoord = fract(v_texCoord + (v_fragmentColor * texture2D(blendTexture, textureCoord)).r * calculatedIntensity);
        return v_fragmentColor * texture2D(CC_Texture0, distortedCoord);
    }

    return baseColor;
}

void main()
{
    vec4 baseColor = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);
    vec4 maskColor = v_fragmentColor * texture2D(u_maskTexture, v_texCoord);

    if (maskColor.r > 0.0) {
        gl_FragColor = blend(u_animationTime, baseColor, maskColor.r, u_red_blendTexture,
                             u_red_tiling, u_red_offset, u_red_blendType, u_red_color, u_red_intensity,
                             u_red_coordinateType, u_red_scrollVelocity, u_red_rotateCenter, u_red_rotateVelocity);
        return;
    } else if (maskColor.g > 0.0) {
        gl_FragColor = blend(u_animationTime, baseColor, maskColor.g, u_green_blendTexture,
                             u_green_tiling, u_green_offset, u_green_blendType, u_green_color, u_green_intensity,
                             u_green_coordinateType, u_green_scrollVelocity, u_green_rotateCenter, u_green_rotateVelocity);
        return;
    } else if (maskColor.b > 0.0) {
        gl_FragColor = blend(u_animationTime, baseColor, maskColor.b, u_blue_blendTexture,
                             u_blue_tiling, u_blue_offset, u_blue_blendType, u_blue_color, u_blue_intensity,
                             u_blue_coordinateType, u_blue_scrollVelocity, u_blue_rotateCenter, u_blue_rotateVelocity);
        return;
    }

    gl_FragColor = baseColor;
}
