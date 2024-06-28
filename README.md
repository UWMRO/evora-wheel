# evora-wheel

Controller and server for the Evora filter wheel, using asyncio.

## Installing and running

To run `evora-wheel` first clone the repository

```bash
git clone git@github.com/uwmro/evora-wheel
```

and then pip-install it

```bash
cd evora-wheel
pip install .
```

To run `evora-wheel` do

```bash
evora-wheel server start
```

which will start the server as a daemon and detach. To stop the running daemon do `evora-wheel sever stop`. To run in attached more

```bash
evora-wheel server start --debug
```

Finally, you can run the dummy server for testing as

```bash
evora-wheel server --dummy start --debug
```

## Using the Docker image

A Docker image for the arm64 architecture (mainly intended to run on a Raspberry Pi) is built every time a commit is pushed to the repository. You can pull the image as

```bash
docker pull ghcr.io/uwmro/evora-wheel:latest
```

and then run it as

```bash
docker run -it --privileged -p 9999:9999 --name evora-wheel -v /dev/bus/usb:/dev/bus/usb  ghcr.io/uwmro/evora-wheel:latest
```

Note that the container needs to run in privileged mode and the USB buses need to be mounted in the container. We also need to expose port 9999 on which the server runs.

### Deploying at MRO

To deploy `evora-wheel` in a Raspberry Pi at MRO we first need to add `udev` rules for the Phidget motor device. Add the following test to `/etc/udev/rules.d/80-phidget.rules`

```plaintext
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="06c2", ATTRS{idProduct}=="00[3-a][0-f]", MODE="666"
```

Then start the container with

```bash
docker run -it --privileged -p 9999:9999 --name evora-wheel -v /dev/bus/usb:/dev/bus/usb --restart always -d ghcr.io/uwmro/evora-wheel:latest
```

which will ensure the container is restarted if if crashes or if the Raspberry Pi is restarted.

If the server stops responding the first thing to try is rebooting the Raspberry Pi either physically or ssh'ing to `mro@72.233.250.84` and running `sudo reboot` (no password should be needed for `sudo`).

If necessary, you can kill the current container with `docker kill evora-wheel`.
