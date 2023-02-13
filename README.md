# CoWebXR (Collaborative WebXR)
======

CoWebXR is forked from [Networked-Aframe](https://github.com/networked-aframe/networked-aframe) which in itself is built upon [A-Frame](https://aframe.io/).

### Main files

The two app pages can be loaded without the file extensions 
* The "backend" support user is `app/instructor.html`
* The "frontend" client AR user is `app/passthrough_ar.html`

In addition to the web app pages, there are supporting components that have to be run separately.9


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

### Running the CoWebXR system

 ```sh
npm install  # Install dependencies
```