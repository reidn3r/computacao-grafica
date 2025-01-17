class Object3D {
    constructor() {
        this.vertices = [];
        this.faces = [];
    }

    async loadFromFile(file) {
        const text = await file.text();
        const lines = text.split('\n');

        for (const line of lines) {
            if (line.startsWith('v ')) {
                this.parseVertex(line);
            } else if (line.startsWith('f ')) {
                this.parseFace(line);
            }
        }
    }

    parseVertex(line) {
        const coords = line.split(' ').slice(1);
        this.vertices.push(coords.map(v => parseFloat(v)));
    }

    parseFace(line) {
        const elements = line.split(' ').slice(1);
        const vertexIndices = elements.map(element =>
            parseInt(element.split('/')[0]) - 1
        );
        this.faces.push(vertexIndices);
    }
}

function rotateVertex(vertex, angleX, angleY) {
    let [x, y, z] = vertex;

    // Rotate around X axis
    const cosX = Math.cos(angleX);
    const sinX = Math.sin(angleX);
    const yRot = y * cosX - z * sinX;
    const zRot = y * sinX + z * cosX;

    y = yRot;
    z = zRot;

    // Rotate around Y axis
    const cosY = Math.cos(angleY);
    const sinY = Math.sin(angleY);
    const xRot = x * cosY + z * sinY;
    z = -x * sinY + z * cosY;
    x = xRot;

    return [x, y, z];
}

class Viewer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.scale = 100;
        this.offset = [250, 250];
        this.isDragging = false;
        this.lastX = 0;
        this.lastY = 0;
        this.rotationX = 0;
        this.rotationY = 0;
        this.obj = null;
        this.setupControls();
    }

    setupControls() {
        // Mouse drag for rotation
        this.canvas.addEventListener('mousedown', (e) => {
            this.isDragging = true;
            this.lastX = e.clientX;
            this.lastY = e.clientY;
        });

        document.addEventListener('mousemove', (e) => {
            if (!this.isDragging || !this.obj) return;

            const deltaX = e.clientX - this.lastX;
            const deltaY = e.clientY - this.lastY;

            this.rotationY += deltaX * 0.01;
            this.rotationX += deltaY * 0.01;

            this.lastX = e.clientX;
            this.lastY = e.clientY;

            this.render();
        });

        document.addEventListener('mouseup', () => {
            this.isDragging = false;
        });

        // Keyboard zoom controls
        document.addEventListener('keydown', (e) => {
            if (e.key === '+') {
                this.scale *= 1.1; // Zoom in
                this.render();
            } else if (e.key === '-') {
                this.scale *= 0.9; // Zoom out
                this.render();
            }
        });
    }

    async loadObject(file) {
        this.obj = new Object3D();
        await this.obj.loadFromFile(file);
        this.render();
    }

    render() {
        if (!this.obj) return;

        const rotatedVertices = this.obj.vertices.map(vertex =>
            rotateVertex(vertex, this.rotationX, this.rotationY)
        );

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawProjection(rotatedVertices, this.obj.faces);
    }

    drawProjection(vertices, faces) {
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 1;

        for (const face of faces) {
            this.ctx.beginPath();
            for (let i = 0; i < face.length; i++) {
                const startIdx = face[i];
                const endIdx = face[(i + 1) % face.length];

                const startVertex = vertices[startIdx];
                const endVertex = vertices[endIdx];

                const startPoint = [
                    startVertex[0] * this.scale + this.offset[0],
                    startVertex[1] * this.scale + this.offset[1]
                ];

                const endPoint = [
                    endVertex[0] * this.scale + this.offset[0],
                    endVertex[1] * this.scale + this.offset[1]
                ];

                if (i === 0) {
                    this.ctx.moveTo(...startPoint);
                }
                this.ctx.lineTo(...endPoint);
            }
            this.ctx.closePath();
            this.ctx.stroke();
        }
    }
}

const canvas = document.getElementById('canvas');
const viewer = new Viewer(canvas);
const fileInput = document.getElementById('fileInput');

fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    await viewer.loadObject(file);
});