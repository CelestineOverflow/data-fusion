
import * as THREE from "three";

export function createTextTexture(
    text: string,
    width: number = 800,
    height: number = 800,
): THREE.Texture {
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext("2d");

    if (!context) {
        throw new Error("Cannot create canvas context");
    }

    // Fill background if necessary
    context.fillStyle = "#FFFFFF"; // White background
    context.fillRect(0, 0, width, height);

    // Text style
    context.fillStyle = "#000000"; // Black text
    context.font = "Bold 40px Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";

    // Handle multiple lines
    const lines = text.split("\n");
    const lineHeight = 48; // Adjust line height as needed
    const initialY = height / 2 - (lineHeight * (lines.length - 1)) / 2;

    lines.forEach((line, index) => {
        context.fillText(line, width / 2, initialY + index * lineHeight);
    });

    // Create texture
    const texture = new THREE.Texture(canvas);
    texture.needsUpdate = true; // Important to update the texture with new canvas

    return texture;
}
