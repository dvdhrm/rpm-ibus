/* -*- mode: js2; js2-basic-offset: 4; indent-tabs-mode: nil -*- */
/* To enable IBus panel for gnome-shell, two modifications are needed.
 * 1. Copy this file to /usr/share/gnome-shell/js/ui/status/ibus.js
 * 2. Modify /usr/share/gnome-shell/js/ui/panel.js with the following patch.
 */
/*
--- usr/share/gnome-shell/js/ui/panel.js
+++ usr/share/gnome-shell/js/ui/panel.js
@@ -33,12 +33,13 @@ const ANIMATED_ICON_UPDATE_TIMEOUT = 100;
 const SPINNER_UPDATE_TIMEOUT = 130;
 const SPINNER_SPEED = 0.02;
 
-const STANDARD_TRAY_ICON_ORDER = ['a11y', 'display', 'keyboard', 'volume', 'bluetooth', 'network', 'battery'];
+const STANDARD_TRAY_ICON_ORDER = ['a11y', 'display', 'keyboard', 'volume', 'bluetooth', 'network', 'battery', 'ibus'];
 const STANDARD_TRAY_ICON_SHELL_IMPLEMENTATION = {
     'a11y': imports.ui.status.accessibility.ATIndicator,
     'volume': imports.ui.status.volume.Indicator,
     'battery': imports.ui.status.power.Indicator,
-    'keyboard': imports.ui.status.keyboard.XKBIndicator
+    'keyboard': imports.ui.status.keyboard.XKBIndicator,
+    'ibus': imports.ui.status.ibus.Indicator,
 };
 
 if (Config.HAVE_BLUETOOTH)
 */

const GLib = imports.gi.GLib;
//const IBUS_PKGDATADIR = imports.misc.config.IBUS_PKGDATADIR;
//const IBUS_GJSDIR = IBUS_PKGDATADIR + '/ui/gjs';
const IBUS_GJSDIR = '/usr/share/ibus' + '/ui/gjs';

const SystemStatusButton = imports.ui.panelMenu.SystemStatusButton;

if (GLib.file_test(IBUS_GJSDIR, GLib.FileTest.IS_DIR)) {
    imports.searchPath.push(IBUS_GJSDIR);
    const ibusindicator = imports.ibusindicator;
}

Indicator.prototype = {
    _init: function() {
        if (ibusindicator == undefined) {
            this._uiapplication = new SystemStatusButton('', '');
        } else {
            this._uiapplication = new ibusindicator.Indicator();
        }
        this.actor = this._uiapplication.actor;
        this.menu = this._uiapplication.menu;
    },
};

function Indicator() {
    this._init.apply(this, arguments);
}
