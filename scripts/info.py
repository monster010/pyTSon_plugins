from ts3plugin import ts3plugin, PluginHost
import ts3, ts3defines, datetime, configparser, os.path
from PythonQt.QtGui import QDialog, QInputDialog, QMessageBox, QWidget
from pytsonui import getValues, ValueType
from collections import OrderedDict
from inspect import getmembers

class info(ts3plugin):
    name = "Extended Info"
    apiVersion = 21
    requestAutoload = True
    version = "1.0"
    author = "Bluscream"
    description = "Shows you more informations.\nBest to use together with a Extended Info Theme.\nClick on \"Settings\" to select what items you want to see :)\n\nHomepage: https://github.com/Bluscream/Extended-Info-Plugin\n\n\nCheck out https://r4p3.net/forums/plugins.68/ for more plugins."
    offersConfigure = True
    commandKeyword = "info"
    infoTitle = "[b]"+name+":[/b]"
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Set Meta Data", "")]
    hotkeys = []
    ini = os.path.join(ts3.getConfigPath(), "extended_info.ini")
    cfg = configparser.ConfigParser()
    cfg.optionxform = str
    runs = 0

    def __init__(self):
        if os.path.isfile(self.ini):
            self.cfg.read(self.ini)
        else:
            self.cfg['general'] = { "Debug": "False", "Colored": "False", "Autorequest Server Variables": "False", "Autorequest Client Variables": "False" }
            self.cfg.add_section('VirtualServerProperties');self.cfg.add_section('VirtualServerPropertiesRare');
            self.cfg.add_section('ChannelProperties');self.cfg.add_section('ChannelPropertiesRare');
            self.cfg.add_section('ClientProperties');self.cfg.add_section('ClientPropertiesRare');
            self.cfg.add_section('ConnectionProperties');self.cfg.add_section('ConnectionPropertiesRare')
            self.cfg.set("VirtualServerProperties", "LAST_REQUESTED", "TRUE");self.cfg.set("VirtualServerProperties", "TYPE", "TRUE")
            for name, value in getmembers(ts3defines.VirtualServerProperties):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER'):
                    self.cfg.set("VirtualServerProperties", name, "False")
            for name, value in getmembers(ts3defines.VirtualServerPropertiesRare):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER_RARE'):
                    self.cfg.set("VirtualServerPropertiesRare", name, "False")
            self.cfg.set("ChannelProperties", "LAST_REQUESTED", "TRUE");self.cfg.set("ChannelProperties", "TYPE", "TRUE")
            for name, value in getmembers(ts3defines.ChannelProperties):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER'):
                    self.cfg.set("ChannelProperties", name, "False")
            for name, value in getmembers(ts3defines.ChannelPropertiesRare):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER_RARE'):
                    self.cfg.set("ChannelPropertiesRare", name, "False")
            self.cfg.set("ClientProperties", "LAST_REQUESTED", "TRUE");self.cfg.set("ClientProperties", "TYPE", "TRUE")
            for name, value in getmembers(ts3defines.ClientProperties):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER'):
                    self.cfg.set("ClientProperties", name, "False")
            for name, value in getmembers(ts3defines.ClientPropertiesRare):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER_RARE'):
                    self.cfg.set("ClientPropertiesRare", name, "False")
            for name, value in getmembers(ts3defines.ConnectionProperties):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER'):
                    self.cfg.set("ConnectionProperties", name, "False")
            for name, value in getmembers(ts3defines.ConnectionPropertiesRare):
                if not name.startswith('__') and not '_DUMMY_' in name and not name.endswith('_ENDMARKER_RARE'):
                    self.cfg.set('ConnectionPropertiesRare', name, 'False')
            with open(self.ini, 'w') as configfile:
                self.cfg.write(configfile)
        ts3.logMessage(self.name+" script for pyTSon by "+self.author+" loaded from \""+__file__+"\".", ts3defines.LogLevel.LogLevel_INFO, "Python Script", 0)
        if self.cfg.getboolean('general', 'Debug'):
            ts3.printMessageToCurrentTab('[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())+" [color=orange]"+self.name+"[/color] Plugin for pyTSon by [url=https://github.com/"+self.author+"]"+self.author+"[/url] loaded.")

    def configDialogClosed(self, r, vals):
        try:
            ts3.printMessageToCurrentTab("vals: "+str(vals))
            if r == QDialog.Accepted:
                for name, val in vals.items():
                    try:
                        if not val == self.cfg.getboolean('general', name):
                            self.cfg.set('general', str(name), str(val))
                    except:
                        from traceback import format_exc
                        ts3.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon", 0)
                with open(self.ini, 'w') as configfile:
                    self.cfg.write(configfile)
        except:
            from traceback import format_exc
            ts3.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon", 0)

    def configure(self, qParentWidget):
        try:
            d = dict()
            d['Debug'] = (ValueType.boolean, "Debug", self.cfg.getboolean('general', 'Debug'), None, None)
            # d['Colored'] = (ValueType.boolean, "Colored", self.cfg.getboolean('general', 'Colored'), None, None)
            d['Autorequest Server Variables'] = (ValueType.boolean, "Autorequest Server Variables", self.cfg.getboolean('general', 'Autorequest Server Variables'), None, None)
            d['Autorequest Client Variables'] = (ValueType.boolean, "Autorequest Client Variables", self.cfg.getboolean('general', 'Autorequest Client Variables'), None, None)
            d['VirtualServerProperties'] = (ValueType.listitem, "Server", ([key for key in self.cfg['VirtualServerProperties']], [i for i, key in enumerate(self.cfg['VirtualServerProperties']) if self.cfg.getboolean('VirtualServerProperties', key)]), 0, 0)
            d['ChannelProperties'] = (ValueType.listitem, "Channel", ([key for key in self.cfg['ChannelProperties']], [i for i, key in enumerate(self.cfg['ChannelProperties']) if self.cfg.getboolean('ChannelProperties', key)]), 0, 0)
            d['ClientProperties'] = (ValueType.listitem, "Client", ([key for key in self.cfg['ClientProperties']], [i for i, key in enumerate(self.cfg['ClientProperties']) if self.cfg.getboolean('ClientProperties', key)]), 0, 0)
            d['ConnectionProperties'] = (ValueType.listitem, "Connection", ([key for key in self.cfg['ConnectionProperties']], [i for i, key in enumerate(self.cfg['ConnectionProperties']) if self.cfg.getboolean('ConnectionProperties', key)]), 0, 0)
            widgets = getValues(None, "Extended Info Configuration", d, self.configDialogClosed)
        except:
            from traceback import format_exc
            ts3.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon", 0)

    def processCommand(self, schid, command):
        tokens = command.split(' ')
        if tokens[0] == "pcmd":
            ts3.sendPluginCommand(schid, tokens[1], ts3defines.PluginTargetMode.PluginCommandTarget_SERVER, []);return True
        elif tokens[0] == "meta":
            if tokens[1] == "get":
                schid = ts3.getCurrentServerConnectionHandlerID()
                error, ownid = ts3.getClientID(schid)
                if error == ts3defines.ERROR_ok:
                    # requestClientVariables(schid, ownid)
                    error, meta = ts3.getClientVariableAsString(schid, ownid, ts3defines.ClientProperties.CLIENT_META_DATA)
                    if error == ts3defines.ERROR_ok:
                        ts3.printMessageToCurrentTab(meta);return True
                    else:
                        ts3.printMessageToCurrentTab("Error: Can't get own meta data.");return True
                else:
                    ts3.printMessageToCurrentTab("Error: Can't get own clientID.");return True
            elif tokens[1] == "set":
                schid = ts3.getCurrentServerConnectionHandlerID()
                error = ts3.setClientSelfVariableAsString(schid, ts3defines.ClientProperties.CLIENT_META_DATA, tokens[2])
                if not error == ts3defines.ERROR_ok:
                    ts3.printMessageToCurrentTab("Error: Unable to set own meta data.");return True
                else: return True
        else:
            ts3.printMessageToCurrentTab("ERROR: Command \""+tokens[0]+"\" not found!");return True
        return False

    def onPluginCommandEvent(self, serverConnectionHandlerID, pluginName, pluginCommand):
            _f = "Plugin message by \""+pluginName+"\": "+pluginCommand
            ts3.logMessage('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())+" "+_f, ts3defines.LogLevel.LogLevel_INFO, self.name, 0)
            if self.cfg.getboolean('general', 'Debug'):
                ts3.printMessageToCurrentTab(_f)
                print(_f)

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if atype == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL:
            if menuItemID == 0:
                schid = ts3.getCurrentServerConnectionHandlerID()
                error, ownid = ts3.getClientID(schid)
                if error == ts3defines.ERROR_ok:
                    error, meta = ts3.getClientVariableAsString(schid, ownid, ts3defines.ClientProperties.CLIENT_META_DATA)
                    if error == ts3defines.ERROR_ok:
                        x = QWidget()
                        meta = QInputDialog.getMultiLineText(x, "Change own Meta Data", "Meta Data:", meta)
                        error = ts3.setClientSelfVariableAsString(schid, ts3defines.ClientProperties.CLIENT_META_DATA, meta)
                        if not error == ts3defines.ERROR_ok:
                            _t = QMessageBox(QMessageBox.Critical, "Error", "Unable to set own meta data!");t.show()

    def infoData(self, schid, id, atype):
        i = []
        schid = ts3.getCurrentServerConnectionHandlerID()
        if atype == 0:
            if self.cfg.getboolean('GENERAL', 'Autorequest Server Variables'):
                ts3.requestServerVariables(schid)
            for name in self.cfg['VirtualServerProperties']:
                if name == 'LAST_REQUESTED':
                    if self.cfg.getboolean('VirtualServerProperties', 'LAST_REQUESTED'):
                        i.append('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                elif name == 'TYPE':
                    if self.cfg.getboolean('VirtualServerProperties', 'TYPE'):
                        i.append('Type: [b]Server[/b]')
                else:
                    try:
                        if self.cfg.getboolean('VirtualServerProperties', name):
                            _tmp = eval('ts3defines.VirtualServerProperties.'+name)
                            (error, _var) = ts3.getServerVariableAsString(schid, _tmp)
                            if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "" and not str(_var) == "0.0000":
                                i.append(name.replace('VIRTUALSERVER_', '').replace('_', ' ').title()+": "+_var)
                    except:
                        continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            for name in self.cfg['VirtualServerPropertiesRare']:
                try:
                    if self.cfg.getboolean('VirtualServerPropertiesRare', name):
                        _tmp = eval('ts3defines.VirtualServerPropertiesRare.'+name)
                        (error, _var) = ts3.getServerVariableAsString(schid, _tmp)
                        if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "" and not str(_var) == "0.0000":
                            i.append(name.replace('VIRTUALSERVER_', '').replace('_', ' ').title()+": "+_var)
                except:
                    continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            return i
        elif atype == 1:
            for name in self.cfg['ChannelProperties']:
                if name == 'LAST_REQUESTED':
                    if self.cfg.getboolean('ChannelProperties', 'LAST_REQUESTED'):
                        i.append('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                elif name == 'TYPE':
                    if self.cfg.getboolean('ChannelProperties', 'TYPE'):
                        i.append('Type: [b]Channel[/b]')
                else:
                    try:
                        if self.cfg.getboolean('ChannelProperties', name):
                            _tmp = eval('ts3defines.ChannelProperties.'+name)
                            (error, _var) = ts3.getChannelVariableAsString(schid, id, _tmp)
                            if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "":
                                i.append(name.replace('CHANNEL_', '').replace('_', ' ').title()+": "+_var)
                    except:
                        continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            for name in self.cfg['ChannelPropertiesRare']:
                try:
                    if self.cfg.getboolean('ChannelPropertiesRare', name):
                        _tmp = eval('ts3defines.ChannelPropertiesRare.'+name)
                        (error, _var) = ts3.getChannelVariableAsString(schid, id, _tmp)
                        if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "":
                            i.append(name.replace('CHANNEL_', '').replace('_', ' ').title()+": "+_var)
                except:
                    continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            return i
        elif atype == 2:
            if self.cfg.getboolean('GENERAL', 'Autorequest Client Variables'):
                ts3.requestClientVariables(schid, id)
            for name in self.cfg['ClientProperties']:
                if name == 'LAST_REQUESTED':
                    if self.cfg.getboolean('ClientProperties', 'LAST_REQUESTED'):
                        i.append('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                elif name == 'TYPE':
                    if self.cfg.getboolean('ClientProperties', 'TYPE'):
                        (error, type) = ts3.getClientVariableAsInt(schid, id, ts3defines.ClientPropertiesRare.CLIENT_TYPE)
                        if error == ts3defines.ERROR_ok:
                            if type == ts3defines.ClientType.ClientType_NORMAL:
                                i.append('Type: [b]Client[/b]')
                            elif type == ts3defines.ClientType.ClientType_SERVERQUERY:
                                i.append('Type: [b]ServerQuery[/b]')
                            else:
                                i.append('Type: [b]Unknown ('+str(type)+')[/b]')
                else:
                    try:
                        if self.cfg.getboolean('ClientProperties', name):
                            _tmp = eval('ts3defines.ClientProperties.'+name)
                            (error, _var) = ts3.getClientVariableAsString(schid, id, _tmp)
                            if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "":
                                i.append(name.replace('CLIENT_', '').replace('_', ' ').title()+": "+_var)
                    except:
                        continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            for name in self.cfg['ClientPropertiesRare']:
                try:
                    if self.cfg.getboolean('ClientPropertiesRare', name):
                        _tmp = eval('ts3defines.ClientPropertiesRare.'+name)
                        (error, _var) = ts3.getClientVariableAsString(schid, id, _tmp)
                        if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "":
                            i.append(name.replace('CLIENT_', '').replace('_', ' ').title()+": "+_var)
                except:
                    continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            for name in self.cfg['ConnectionProperties']:
                try:
                    if self.cfg.getboolean('ConnectionProperties', name):
                        _tmp = eval('ts3defines.ConnectionProperties.'+name)
                        (error, _var) = ts3.getConnectionVariableAsString(schid, id, _tmp)
                        if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "":
                            i.append(name.replace('CONNECTION_', '').replace('_', ' ').title()+": "+_var)
                except:
                    continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            for name in self.cfg['ConnectionPropertiesRare']:
                try:
                    if self.cfg.getboolean('ConnectionPropertiesRare', name):
                        _tmp = eval('ts3defines.ConnectionPropertiesRare.'+name)
                        (error, _var) = ts3.getConnectionVariableAsString(schid, id, _tmp)
                        if error == ts3defines.ERROR_ok and _var and not str(_var) == "0" and not str(_var) == "":
                            i.append(name.replace('CONNECTION_', '').replace('_', ' ').title()+": "+_var)
                except:
                    continue#ts3.logMessage('Could not look up '+name, ts3defines.LogLevel.LogLevel_ERROR, self.name, schid)
            return i
        else:
            return ["ItemType \""+str(atype)+"\" unknown."]
