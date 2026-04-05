#  ET-View RCSetup version 1.4
#  Remote Controller Setup (RCSetup)
# -*- coding: utf-8 -*-
# for localized messages
from . import _

from os import chmod, unlink
from os.path import exists

from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigSelection, getConfigListEntry

modelist = {"3": _("OdinM9"), "5": _("ET9000/ET9100"), "4": _("DMM/DMM ADV"), "6": _("DMM/DMM ADV"), "7": _("ET5000/ET6000"), "8": _("Vu"), "9": _("ET6500/ET9500"), "11": _("ET9200/ET9500"), "13": _("ET4000"), "14": _("XP1000"), "16": _("HD1100"), "17": _("XP3000"), "18": _("F1/F3"), "19": _("HD2400")}

PROC = "/proc/stb/ir/rc/type"
INIT_SCRIPT = "/etc/rc3.d/S30rcsetup"

config.plugins.RCSetup = ConfigSubsection()
file = open(PROC, "r")
text = file.read()
file.close()
temp = int(text)
if temp == 19:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="19")
elif temp == 18:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="18")
elif temp == 17:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="17")
elif temp == 16:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="16")
elif temp == 14:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="14")
elif temp == 13:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="13")
elif temp == 11:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="11")
elif temp == 9:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="9")
elif temp == 8:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="8")
elif temp == 7:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="7")
elif temp == 6:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="6")
elif temp == 5:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="5")
elif temp == 4:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="4")
elif temp == 3:
	config.plugins.RCSetup.mode = ConfigSelection(choices=modelist, default="3")


class RCSetupScreen(ConfigListScreen, Screen):
	skin = """
	<screen position="c-200,c-100" size="400,200" title="Remote setup">
		<widget name="config" position="c-175,c-75" size="350,150" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="c-145,e-45" zPosition="0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="c+5,e-45" zPosition="0" size="140,40" alphatest="on" />
		<widget name="ok" position="c-145,e-45" size="140,40" valign="center" halign="center" zPosition="1" font="Regular;20" transparent="1" backgroundColor="green" />
		<widget name="cancel" position="c+5,e-45" size="140,40" valign="center" halign="center" zPosition="1" font="Regular;20" transparent="1" backgroundColor="red" />
	</screen>"""

	def __init__(self, session):
		self.skin = RCSetupScreen.skin
		Screen.__init__(self, session)
		self.skinName = ['RCSetupScreen', 'Setup']

		self["key_green"] = self["ok"] = Button(_("OK"))
		self["key_red"] = self["cancel"] = Button(_("Cancel"))

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"ok": self.keyGo,
			"save": self.keyGo,
			"cancel": self.keyCancel,
			"green": self.keyGo,
			"red": self.keyCancel,
		}, -2)
		self.createSetup()
		self.grabLastGoodMode()

	def grabLastGoodMode(self):
		mode = config.plugins.RCSetup.mode.value
		self.last_good = (mode)

	def createSetup(self):
		self.list = []
		ConfigListScreen.__init__(self, self.list, session=self.session)
		mode = config.plugins.RCSetup.mode.value
		self.mode = ConfigSelection(choices=modelist, default=mode)
		self.list.append(getConfigListEntry(_("Remote"), self.mode))
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keyGo(self):
		config.plugins.RCSetup.mode.value = self.mode.value
		self.applySettings()

		RC = config.plugins.RCSetup.mode.value
		if (RC) != self.last_good:
			self.session.openWithCallback(self.confirm, MessageBox, _("Is this remote ok?"), MessageBox.TYPE_YESNO, timeout=10, default=False)
		else:
			config.plugins.RCSetup.save()
			self.close()

	def confirm(self, confirmed):
		if not confirmed:
			config.plugins.RCSetup.mode.value = self.last_good[0]
			self.applySettings()
		else:
			self.installHelper()
			self.applySettings()
			self.keySave()

	def installHelper(self):
		tmp = int(config.plugins.RCSetup.mode.value)
		if tmp == 3:
			self.removeFile()
		elif tmp == 5:
			self.removeFile()
		elif tmp == 4:
			self.createFile()
		elif tmp == 6:
			self.createFile()
		elif tmp == 7:
			self.createFile()
		elif tmp == 8:
			self.createFile()
		elif tmp == 9:
			self.createFile()
		elif tmp == 11:
			self.createFile()
		elif tmp == 13:
			self.createFile()
		elif tmp == 14:
			self.createFile()
		elif tmp == 16:
			self.createFile()
		elif tmp == 17:
			self.createFile()
		elif tmp == 18:
			self.createFile()
		elif tmp == 19:
			self.createFile()

	def createFile(self):
		file = open(INIT_SCRIPT, "w")
		m = 'echo ' + config.plugins.RCSetup.mode.value + ' > ' + PROC
		file.write(m)
		file.close()
		# Set permissions to rwxr-xr-x (0o755) - standard for init scripts
		# Owner: read, write, execute; Group: read, execute; Others: read, execute
		chmod(INIT_SCRIPT, 0o755)  # NOSONAR - octal literal is more clear for file permissions

	def removeFile(self):
		if exists(INIT_SCRIPT):
			unlink(INIT_SCRIPT)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)

	def keyRight(self):
		ConfigListScreen.keyRight(self)

	def keyCancel(self):
		self.applySettings()
		self.close()

	def applySettings(self):
		file = open(PROC, "r")
		lines = file.readlines()
		file.close()
		if int(lines[0]) != int(config.plugins.RCSetup.mode.value):
			try:
				file = open(PROC, "w")
				file.write('%d' % int(config.plugins.RCSetup.mode.value))
				file.close()
			except OSError:
				return


def main(session, **kwargs):
	session.open(RCSetupScreen)


def startup(reason, **kwargs):
	return


def RemoteControlSetup(menuid, **kwargs):
	if menuid == "system":
		return [(_("Remote Control Code"), main, "remotecontrolcode", 50)]
	else:
		return []


def Plugins(**kwargs):
	if exists(PROC):
		return [PluginDescriptor(name=_("Remote Control Code"), where=PluginDescriptor.WHERE_MENU, needsRestart=False, fnc=RemoteControlSetup),
					PluginDescriptor(name="Remote Setup", description="", where=PluginDescriptor.WHERE_SESSIONSTART, fnc=startup)]
	return []
