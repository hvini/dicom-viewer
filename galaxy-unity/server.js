global.__basedir = __dirname;
const app = require('./src/app');
const fs = require('fs');
const privateKey = fs.readFileSync('key.pem', 'utf8');
const certificate = fs.readFileSync('cert.pem', 'utf8');
const credentials = { key: privateKey, cert: certificate };
const https = require('https');
const server = https.createServer(credentials, app)
const { WebSocket, WebSocketServer } = require('ws');
const wss = new WebSocketServer({ server });
const { FindMaxFrames } = require('./src/utils/findMaxFrames');
const { ByteArray } = require('./src/utils/byteArray');

const port = 3230;

wss.on('connection', async (ws, req) => {
    console.log("a user connected");

    const ping = function() { ws.ping(noop); }
    setInterval(ping, 30000);

    const maxFrames = await FindMaxFrames();
    const maxFramesWithOffset = parseInt(maxFrames) + 10;
    const encodedMaxFrames = ByteArray(maxFramesWithOffset.toString());
    ws.send(encodedMaxFrames);

    ws.on('close', () => {
        console.log("client left");
    });

    ws.on('message', (message) => {
        wss.clients.forEach(client => {
            if (client !== ws && client.readyState == WebSocket.OPEN) {
                client.send(message);
            }
        });
    });
});

function noop() { }

server.listen(port, () => {
    console.log("Server is running on port: " + port);
});
