"""Setuptools command sub-classes."""

from setuptools import Command
from setuptools.command import develop as _develop
from setuptools.command import install as _install
from setuptools.command import install as _install

import os
import inspect

from os.path import expanduser, abspath, dirname, join, exists, islink

from cheshire3.exceptions import ConfigFileException
from cheshire3.internal import cheshire3Home, cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.session import Session

from diggingintodata.setup.exceptions import * 


class unavailable_command(Command):
    """Sub-class commands that we don't want to make available."""

    description = "Command is not appropriate for this package"
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        raise NotImplementedError(self.description)


class DIDCommand(Command):
    """Base Class for custom commands."""
    
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class develop(_develop.develop, DIDCommand):
    
    description = "Install diggingintodata in development mode"
    
    user_options = _develop.develop.user_options + DIDCommand.user_options
    
    def install_for_development(self):
        global distropath, server, session
        # Carry out normal procedure
        _develop.develop.install_for_development(self)
        # Tell the server to register the config file
        try:
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'jstor',
                                                             'config.xml'))
        except ConfigFileException as e:
            if e.reason.startswith("Database with id 'db_jstor' is already "
                                   "registered."):
                # Existing install / development install
                raise DevelopException("Package is already installed. To "
                                       "install in 'develop' mode you must "
                                       "first run the 'uninstall' command.")
        
    def uninstall_link(self):
        global server, session
        # Carry out normal procedure
        _develop.develop.uninstall_link(self)
        # Unregister the database by deleting
        # Cheshire3 database config plugin
        serverDefaultPath = server.get_path(session,
                                            'defaultPath',
                                            cheshire3Root)
        userSpecificPath = join(expanduser('~'), '.cheshire3-server')
        pluginPath = os.path.join('configs', 'databases', 'db_jstor.xml')
        if exists(join(serverDefaultPath, pluginPath)):
            os.remove(join(serverDefaultPath, pluginPath))
        elif exists(os.path.join(userSpecificPath, pluginPath)):
            os.remove(os.path.join(userSpecificPath, pluginPath))
        else:
            server.log_error(session, "No database plugin file")


class install(_install.install):
    
    description = "Install diggingintodata"
    
    user_options = _install.install.user_options + DIDCommand.user_options
    
    def run(self):
        # Carry out normal procedure
        _install.install.run(self)
        # Install Cheshire3 database config plugin
        # Tell the server to register the config file
        try:
            server.register_databaseConfigFile(session, join(distropath,
                                                             'dbs',
                                                             'jstor',
                                                             'config.xml'))
        except ConfigFileException as e:
            if e.reason.startswith("Database with id 'db_jstor' is already "
                                   "registered."):
                # Existing install / development install
                raise InstallException("Package is already installed. To "
                                       "install you must first run the "
                                       "'uninstall' command.")


class uninstall(DIDCommand):

    description = "Uninstall diggingintodata"
    
    def run(self):
        # Unregister the database by deleting
        # Cheshire3 database config plugin
        serverDefaultPath = server.get_path(session,
                                            'defaultPath',
                                            cheshire3Root)
        userSpecificPath = join(expanduser('~'), '.cheshire3-server')
        pluginPath = os.path.join('configs', 'databases', 'db_jstor.xml')
        if exists(join(serverDefaultPath, pluginPath)):
            os.remove(join(serverDefaultPath, pluginPath))
        elif exists(os.path.join(userSpecificPath, pluginPath)):
            os.remove(os.path.join(userSpecificPath, pluginPath))
        else:
            server.log_error(session, "No database plugin file")


# Inspect to find current path
modpath = inspect.getfile(inspect.currentframe())
moddir = dirname(modpath)
distropath = abspath(join(moddir, '..', '..'))
serverConfig = os.path.join(cheshire3Root,
                            'configs',
                            'serverConfig.xml')
session = Session()
server = SimpleServer(session, serverConfig)
