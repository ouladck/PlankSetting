#!/bin/bash

sudo cp -v PlankSetting.desktop /usr/share/applications
sudo cp -v planksetting /usr/bin
sudo cp -v planksetting.dockitem /home/*/.config/plank/*/launchers
sudo cp -v pixmaps/*.png /usr/share/pixmaps
sudo cp -r -v locale /usr/share
sudo mv pixmaps /tmp
sudo mv locale /tmp
sudo mv PlankSetting.desktop /tmp
sudo mv planksetting /tmp
sudo mkdir /usr/share/planksetting
sudo cp -v -r * /usr/share/planksetting
sudo mv /tmp/pixmaps .
sudo mv /tmp/locale .
sudo mv /tmp/PlankSetting.desktop .
sudo mv /tmp/planksetting .
echo "PlankSetting is installed now!"