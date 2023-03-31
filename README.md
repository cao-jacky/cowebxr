# CoWebXR (Collaborative WebXR)
======

CoWebXR is forked from [Networked-Aframe](https://github.com/networked-aframe/networked-aframe) which in itself is built upon [A-Frame](https://aframe.io/).

### Main files

The two app pages can be loaded without the file extensions 
* The "backend" support user is `app/instructor.html`
* The "frontend" client AR user is `app/passthrough_ar.html`

In addition to the web app pages, there are supporting components that have to be run separately.
1. `supporting_components/database` contains the JavaScript server that the web app communicates with to store the data
2. `supporting_components/stream_capture` can watch and listen to the client streams in CoWebXR using `stream_capture.html`, these are then saved into small chunks which are then analysed in a Python script `detect.py`, and the recognised results returned to the user  


### Installation and running

Before the CoWebXR experience can be run, several dependencies need to be installed/already installed.

Clone this GitHub repo

 ```sh
git clone https://github.com/cao-jacky/cowebxr.git 
cd cowebxr
```

1. SSL for HTTPS connectivity
As we want to utilise the on-device sensors, a HTTPS connection is required. In this work, I have been using LetsEncrypt and Certbot, you will need to know the locations of your `privkey.pem`, `chain.pem`, and `fullchain.pem`. 

Then in the file, `server\easyrtc-server-ssl.js`, change the variable webServer to match the location of the files which correspond to the `key`, `ca`, and `cert`.

```javascript
const webServer = https.createServer({
    key:  fs.readFileSync("/etc/letsencrypt/live/cowebxr.com/privkey.pem"),
    ca:   fs.readFileSync("/etc/letsencrypt/live/cowebxr.com/chain.pem"),
    cert: fs.readFileSync("/etc/letsencrypt/live/cowebxr.com/fullchain.pem")
}, app);
```

2. Janus for collaborative connections
To get this runnimg, the easiest way is following [this](https://github.com/networked-aframe/naf-janus-adapter/blob/master/docs/janus-deployment.md) tutorial       

There are some additional steps that need to be taken, when editing the `janus.transport.websockets.jcfg` file, make these changes/additions:

```
general: {
    wss = true
    wss_port = 8989
}

certificates: {
    cert_pem = "/etc/letsencrypt/live/cowebxr.com/cert.pem"
    cert_key = "/etc/letsencrypt/live/cowebxr.com/privkey.pem"
}
```

3. Check the app files and whether the correct Janus URLs are being pointed to, e.g., 

```html
<a-scene
        mindar-image="imageTargetSrc: https://cdn.jsdelivr.net/gh/hiukim/mind-ar-js@1.1.4/examples/image-tracking/assets/card-example/card.mind; uiScanning: no"
        color-space="sRGB" renderer="colorManagement: true, physicallyCorrectLights" vr-mode-ui="enabled: false"
        device-orientation-permission-ui="enabled: false" 
        networked-scene="
          room: 1;
          debug: true;
          adapter: janus;
          connectOnLoad: true;
          serverURL: wss://cowebxr.com:8989/janus; " 
          >
```

4. (Optional) You can choose to use a local or cloud MongoDB database to store the data for the marker codes and their corresponding content

5. Install the dependencies for the Python analysis application 

6. Run npm install on the root of the `cowebxr` directory

 ```sh
npm install  # Install dependencies
```


### Running the CoWebXR system

The following need to be run to get the system working

1. The main WebXR server application

```sh
cd server
sudo node server.js
```

2. Janus if it is not already running
```sh
janus
```

3. Similarly, MongoDB if not already running

4. The MongoDB database connector web app

```sh
cd supporting_components/database
sudo node main.js
```