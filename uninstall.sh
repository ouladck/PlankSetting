#!/bin/bash

sudo rm /usr/share/applications/PlankSetting.desktop
sudo rm /usr/bin/planksetting
sudo rm /usr/share/pixmaps/planksettin*.png
sudo rm -r /usr/share/PlankSetting
sudo rm /usr/share/locale/*/LC_MESSAGES/planksetting.mo
echo -e "Uninstallation is done\nThanks for using PlankSetting(^_^)"
exit 0