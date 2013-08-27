#!/usr/bin/env python

import argparse
import ConfigParser

class store_build(argparse.Action):
    #We have called to build the environemt, configurationg build options
    def __call__(self, parser, namespace, values, option_string=None):
        print ("%r %r %r" % (namespace, values, option_string))

class list_environments(argparse.Action):
    #We have called to list all current environments, getting info
    #Still trying to decide to do this on the fly or store envs in cache
    def __call__(self, parser, namespace, values, option_string=None):
        print ("%r %r %r" % (namespace, values, option_string))

class store_destroy(argparse.Action):
    #We are destroying the environment selected, if more than one, well need to list envs
    def __call__(self, parser, namespace, values, option_string=None):
        print ("%r %r %r" % (namespace, values, option_string))

class configuration():
    def __init__(self, config):
        config = ConfigParser.SafeConfigParser()
        config.readfp(open('build_dev.cfg'))
        # Read User Credentials
        try:
            self.username = config.get("credentials", "username")
        except ConfigParser.NoOptionError:
            print "Unable to find username defined in configuration file"
            print "Please correct username field under the \"credentials\" option"
            return False

        try:
            self.password = config.get("credentials", "password")
        except ConfigParser.NoOptionError:
            self.password = ""

        try:
            self.apikey = config.get("credentials", "apikey")
        except ConfigParser.NoOptionError:
            self.apikey = ""

        if self.apikey == "" and self.password == "":
            print "You need to provide either an account password"
            print "or an ApiKey for your user account"
            return False
        # Since usercredentials could be stored in the keyring, check for
        # USE_KEYRING in the variable
        if self.username == "USE_KEYRING" or self.password == "USE_KEYRING" or self.apikey == "USE_KEYRING":
            # Something needs a keyring variable, lets walk through them
            import keyring

            if self.username == "USE_KEYRING":
                self.username = keyring.get_password('build_dev', 'username')
                if self.username == 'None'
                    print "Username not set in keyring"
                    return 0


if __name__ == '__main__':
    # Lets Parse some Arguments to see what we are doing
    parser = argparse.ArgumentParser(description="This program will take your RackSpace usernane and api \
                                    key and username and build a dev server from an image or fresh")
    parser.add_argument('-v', '--version', help="Version of the OS for the Dev Env", type=int)
    parser.add_argument('-r', '--region', metavar='region', help="Enter the Region (DFW, ORD, IAD, SYD)",\
                        choices=['DFW','ORD','IAD','SYD'], type=str)
    parser.add_argument('-d', '--distribution', metavar='distribuion',  help="Enter Distribution Type (CentOS)")
    parser.add_argument('-c', '--config', metavar='configFile', help="Configuration File", default="~/.build_dev.cfg")
    buildGroup = parser.add_mutually_exclusive_group()
    buildGroup.add_argument('-b', '--build', action='store_true', help="Build the server Environment")
    buildGroup.add_argument('-l', '--list', action='store_true', help="List Currently Running Environmenrs")
    buildGroup.add_argument('--destroy', action='store_true', help="Destroy Environment" )
    args = parser.parse_args()

    # Now we have parsed the Arguments, we know what to do, let read the configuration file.
    config = configuration(args.config)
