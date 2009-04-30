#! /usr/bin/env python
# encoding: utf-8

# defines not needed anymore

#  SUSE_10_2
#  USE_GTKHTML38_3_13 
#  USE_GTKHTML38 


import sys
if sys.version_info < (2,3):
    raise RuntimeError("Python 2.3 or newer is required")

import os, os.path
import intltool, gnome
from os.path import join, dirname, abspath


# waf imports
import Utils
import Options
import ccroot


# custom imports
from waffles.gecko import Gecko
from waffles.gtkhtml import Gtkhtml
from waffles.misc import *

# the following two variables are used by the target "waf dist"
VERSION='3.0.1'
APPNAME='xiphos'
PACKAGE='xiphos'

# these variables are mandatory ('/' are converted automatically)
srcdir = '.'
blddir = 'build'

_prefix = '/usr/local'

_headers = '''
dlfcn.h
inttypes.h
locale.h
memory.h
stdint.h
stdlib.h
strings.h
string.h
sys/stat.h
sys/types.h
unistd.h
sys/select.h
sys/socket.h
'''.split()

_unused_options = '''
sbindir
sysconfdir
libdir
libexecdir
sharedstatedir
localstatedir
includedir
oldincludedir
datadir
infodir
mandir
htmldir
dvidir
pdfdir
psdir
'''.split()


def set_options(opt):


    # options provided by the modules
    #opt.tool_options('g++ gcc gnome intltool glib2')
    opt.tool_options('g++ gcc gnu_dirs')

    # unused options
    for name in _unused_options:
        option_name = '--' + name
        opt.parser.remove_option(option_name)

    #opt.add_option('--enable-paratab', action='store_true', default=True,
            #dest='paratab', help='Use paratab [Default: True]')

    opt.add_option('--enable-autoclear', action='store_true', default=False,
            dest='autoclear', help='Use previewer autoclear [Default: False]')

    opt.add_option('--enable-old_navbar', action='store_true', default=False,
            dest='old_navbar', help='Use old_navbar [Default: False]')

    opt.add_option('--enable-gtkhtml', action='store_true', default=False,
            dest='gtkhtml',
            help='Use gtkhtml instead of gtkmozembed [Default: False]')

    #opt.add_option('--enable-maintainer-mode', action='store_true',
            #default=False, dest='maintainer_mode',
            #help='''Enable make rules and dependencies not useful (and sometimes confusing) to the casual installer''')

    # replaces '--enable-maintainer-mode', '--enable-debug'
    opt.add_option('-d', '--debug-level',
		action = 'store',
		default = ccroot.DEBUG_LEVELS.ULTRADEBUG,
		help = "Specify the debugging level ['ultradebug', 'debug', 'release', 'optimized']",
		choices = ['ultradebug', 'debug', 'release', 'optimized'],
		dest = 'debug_level')

    opt.add_option('--enable-delint', action='store_true', default=False,
            dest='delint',
            help='Use -Wall -Werror [Default: False]')

    group = opt.add_option_group ('Localization and documentation', '')
    group.add_option('--helpdir',
		action = 'store',
		default = '${DATAROOTDIR}/gnome/help/${PACKAGE}',
                help = "user documentation [Default: ${DATAROOTDIR}/gnome/help/${PACKAGE}]",
		dest = 'helpdir')


def configure(conf):

    env = conf.env
    import Utils
    platform = Utils.detect_platform()
    env['IS_LINUX'] = platform == 'linux'
    env['IS_WIN32'] = platform == 'win32'

    if env['IS_LINUX']:
        Utils.pprint('CYAN', "Linux detected")

    if env['IS_WIN32']:
        Utils.pprint('CYAN', "Windows detected")

    if not (env['IS_LINUX'] or env['IS_WIN32']):
        Utils.pprint('RED', "Unknown or unsupported platform")
        exit(1)


    ## temporary HACKS for win32
    if env['IS_WIN32']:
        env['PREFIX'] = _prefix
    ##

    conf.check_tool('g++ gcc gnu_dirs')

    if env['IS_WIN32']:
        # tool to link icon with executable
        conf.check_tool('winres')
    else:
        conf.check_tool('intltool') # check for locale.h included
        conf.check_tool('misc')


    # delint flags
    for name in ('CXXFLAGS_DELINT', 'CCFLAGS_DELINT'):
        env[name] = ['-Werror', '-Wall']

    # gcc compiler debug levels
    # msvc has levels predefined
    if env['CC_NAME'] == 'gcc':
        env['CCFLAGS']            = []
        env['CCFLAGS_OPTIMIZED']  = ['-O2']
        env['CCFLAGS_RELEASE']    = ['-O2']
        env['CCFLAGS_DEBUG']      = ['-g', '-DDEBUG']
        env['CCFLAGS_ULTRADEBUG'] = ['-g3', '-O0', '-DDEBUG']

    if env['CXX_NAME'] == 'gcc':
        env['CXXFLAGS']            = []
        env['CXXFLAGS_OPTIMIZED']  = ['-O2']
        env['CXXFLAGS_RELEASE']    = ['-O2']
        env['CXXFLAGS_DEBUG']      = ['-g', '-DDEBUG', '-ftemplate-depth-25']
        env['CXXFLAGS_ULTRADEBUG'] = ['-g3', '-O0', '-DDEBUG', '-ftemplate-depth-25']
    
    
    ## temporary HACKS for win32
    if env['IS_WIN32']:
        env['CCFLAGS'] = ['-mms-bitfields']
        env['CXXFLAGS'] = ['-mms-bitfields']
    ##

    
    ### cmd line options

    opt = Options.options
    dfn = conf.define
    env = conf.env


    # appropriate cflags
    env.append_value('CXXFLAGS', env['CXXFLAGS_%s' % opt.debug_level.upper()])
    env.append_value('CCFLAGS', env['CCFLAGS_%s' % opt.debug_level.upper()])

    if env['IS_WIN32']:
        dfn('WIN32', 1)

    if opt.delint:
        env.append_value('CXXFLAGS', env['CXXFLAGS_DELINT'])
        env.append_value('CCFLAGS', env['CCFLAGS_DELINT'])

    if opt.debug_level == 'ultradebug' or opt.debug_level == 'debug':
        dfn('MAINTAINER_MODE', 1)
    #if opt.paratab:
        #dfn('USE_PARALLEL_TAB', 1)
    if opt.autoclear:
        dfn('USE_PREVIEWER_AUTOCLEAR', 1)
    if opt.old_navbar:
        dfn('OLD_NAVBAR ', 1)

    # gtkhtml
    if opt.gtkhtml:
        env['ENABLE_GTKHTML'] = True
        dfn('GTKHTML', 1)



    ### App info, paths
    define = conf.define
    sub = Utils.subst_vars

    env['VERSION'] = VERSION
    env['APPNAME'] = APPNAME
    env['PACKAGE'] = PACKAGE
    env['HELPDIR'] = sub(opt.helpdir, env)

    define('VERSION', VERSION)
    define('PACKAGE_VERSION', VERSION)
    define('GETTEXT_PACKAGE', PACKAGE)
    define('PACKAGE', PACKAGE)
    define('PACKAGE_NAME', APPNAME)
    define('PACKAGE_STRING', '%s %s' % (APPNAME, VERSION))
    define('PACKAGE_TARNAME', PACKAGE)

    define('INSTALL_PREFIX', escpath(sub('${PREFIX}/', env)))
    #dfn('LT_OBJDIR', '.libs') - what's the purpose?
    define('PACKAGE_BUGREPORT','http://sourceforge.net/tracker/?group_id=5528&atid=105528' )
    define('PACKAGE_DATA_DIR', escpath(sub('${DATAROOTDIR}/${PACKAGE}', env)))
    define('PACKAGE_DOC_DIR', escpath(env['DOCDIR']))
    define('PACKAGE_HELP_DIR', escpath(sub('${DATAROOTDIR}/gnome/help/${PACKAGE}', env)))
    define('PACKAGE_LOCALE_DIR', escpath(env['LOCALEDIR']))
    define('PACKAGE_MENU_DIR', escpath(sub('${DATAROOTDIR}/applications', env)))
    define('PACKAGE_PIXMAPS_DIR', escpath(sub('${DATAROOTDIR}/pixmaps/${PACKAGE}', env)))
    define('PACKAGE_SOURCE_DIR', escpath(abspath(srcdir))) # foder where was wscript executed

    # some folders for final executable
    #define('PREFIX', escpath(env['PREFIX']))
    #define('SYSCONFDIR', escpath(env['SYSCONFDIR']))
    #define('DATADIR', escpath(env['DATAROOTDIR']))
    #env.append_value('CXXFLAGS', env['CXXDEFINES_ST'] % ('DATADIR='+escpath(env['DATAROOTDIR'])))
    #env.append_value('CCFLAGS', env['CCDEFINES_ST'] % ('DATADIR='+escpath(env['DATAROOTDIR'])))
    #define('LIBDIR', escpath(env['LIBDIR']))
    #define('SHARE_DIR', escpath(sub('${DATAROOTDIR}/${PACKAGE}', env)))


    ## CXX flags (compiler arguments)
    #conf.check_cxx(cxxflags='-ftemplate-depth-25')
    #conf.check_cxx(cxxflags='-Werror')
    #conf.check_cxx(cxxflags='-Wall')
    #conf.env.append_value('CCFLAGS', '-g -O2 -Werror -Wall'.split())
    #conf.env.append_value('CXXFLAGS', '-g -O2 -ftemplate-depth-128 -Werror -Wall'.split())

    # pkg-config
    conf.check_cfg(atleast_pkgconfig_version='0.9.0')


    # GTK+
    #check_pkg(conf, 'gtk+-x11-2.0', '2.0.0', var='LIBGTK_X11_2_0')
    #if not env['HAVE_LIBGTK_X11_2_0']:
    #    check_pkg(conf, 'gtk+-x11-2.0', '2.0.0', True, var='LIBGTK_WIN32_2_0')
    check_pkg(conf, 'gtk+-2.0', '2.0', True, var='GTK')

    # tooltip function needs gtk+ >= 2.12 HAVE_WIDGET_TOOLTIP_TEXT
    #check_pkg(conf, 'gtk+-2.0', '2.12', var='WIDGET_TOOLTIP_TEXT')
    #conf.check_cfg(conf, 'gtk+-2.0', '2.12', var='WIDGET_TOOLTIP_TEXT')
    #conf.check_cfg (package='gtk+-2.0', msg='Checking for widget_tooltip_text',
        #uselib_store='WIDGET_TOOLTIP_TEXT', atleast_version='2.12')
    check_pkgver_msg(conf, 'gtk+-2.0', '2.12', var='WIDGET_TOOLTIP_TEXT',
        msg='Checking for gtk+-2.0 widget_tooltip_text')

    # glade
    check_pkg(conf, 'libglade-2.0', '2.0.0', var='GLADE')
        

    # gtk popup menus - dynamic loadable libs
    #if env['IS_WIN32']:
        #check_pkg(conf, 'gmodule-no-export-2.0', '2.0.0', True, var='GMODULEEXP')
    #else: 
        #check_pkg(conf, 'gmodule-export-2.0', '2.0.0', True, var='GMODULEEXP')
    check_pkg(conf, 'gmodule-2.0', '2.0.0', True, var='GMODULEEXP')

    ## Gnome libs
    check_pkg(conf, 'glib-2.0', '2.0.0', True, 'GLIB')
    check_pkg(conf, 'libgnomeui-2.0', '2.0.0', True, var='GNOMEUI')

    #check_pkg(conf, 'libgnomeprintui-2.2', '2.2', True, var='GNOMEPRINTUI')
    #check_pkg(conf, 'libgnomeprint-2.2', '2.2', True, var='GNOMEPRINT')

    ## Other
    check_pkg(conf, 'libxml-2.0', '2.0.0', True, var='XML')
    check_pkg(conf, 'ImageMagick++', '6.0.0', True, var='MAGICK')

    check_pkg(conf, 'gtk+-unix-print-2.0', '2.0.0', var='UPRINT')
    if env['HAVE_UPRINT']:
        dfn('USE_GTKUPRINT', 1)

    ## Sword
    check_pkg(conf, 'sword', '1.5.11', True, var='SWORD')

    check_pkgver_msg(conf, 'sword', '1.5.11.99', var='MULTIVERSE',
            msg='Checking for sword multiverse')
    if env['HAVE_MULTIVERSE']:
        dfn('SWORD_MULTIVERSE', 1)


    ### gtkhtml - decide HAVE_GTKHTML3_23
    if not Gtkhtml(conf).detect():
        print 'Error: GTKHTML not found'
        exit(1)


    # bonobo editor variant, slib-editor otherwise
    if not env['HAVE_EDITOR_IDL']:

        ### editor.py
        check_pkg(conf, 'ORBit-2.0', mandatory=True)
        check_pkg(conf, 'libbonobo-2.0', mandatory=True)
        check_pkg(conf, 'bonobo-activation-2.0', mandatory=True)

        # ORBIT_IDL
        env['ORBIT_IDL'] = get_pkgvar(conf, 'ORBit-2.0', 'orbit_idl')

        # BONOBO_IDL_INCLUDES
        idl1 = get_pkgvar(conf, 'libbonobo-2.0', 'idldir')
        idl2 = get_pkgvar(conf, 'bonobo-activation-2.0', 'idldir')

        env['BONOBO_IDL_INCLUDES'] = '-I%s -I%s' % (idl1, idl2)
        ### END editor.py



    ######################
    ### gecko (xulrunner) for html rendering
    # gtkhtml only for editor
    if not env['ENABLE_GTKHTML']:
        Gecko(conf).detect()
        dfn('USE_GTKMOZEMBED', 1)
        env.append_value('CCFLAGS', env['GECKO_CCFLAGS'])
        env.append_value('CXXFLAGS', env['GECKO_CCFLAGS'])
    ######################


    # TODO: maybe the following checks should be in a more generic module.

    #always defined to indicate that i18n is enabled */
    dfn('ENABLE_NLS', 1)

    # TODO
    #Define to 1 if you have the `bind_textdomain_codeset' function.
    dfn('HAVE_BIND_TEXTDOMAIN_CODESET', 1)


    # TODO
    #Define if the GNU gettext() function is already present or preinstalled.
    dfn('HAVE_GETTEXT', 1)
    #Define to 1 if you have the `dcgettext' function.
    dfn('HAVE_DCGETTEXT', 1)


    # Check for header files
    for h in _headers:
        conf.check(header_name=h)


    # Define to 1 if you have the `strcasestr' function.
    # this function is part of some glibc, string.h
    # could be missing in win32
    conf.check_cc(msg='Checking for function strcasestr', define_name="HAVE_STRCASESTR",
            fragment='int main() {strcasestr("hello","he");}\n')


    # TODO: What's the purpose of STDC? Is xiphos able compile without that?
    # Define to 1 if you have the ANSI C header files. */
    # NOT necessary?
    dfn('STDC_HEADERS', 1)
    # Define to 1 if you can safely include both <sys/time.h> and <time.h>. */
    dfn('TIME_WITH_SYS_TIME', 1)


            # TODO: how to detect these values? is it possible to detect them?

    # TODO: not necessary SELECT* defines?
    # Define to the type of arg 1 for `select'. */
    #dfn('SELECT_TYPE_ARG1', 'int', quote=0) # dont add quotes around 'int'
    # Define to the type of args 2, 3 and 4 for `select'. */
    #dfn('SELECT_TYPE_ARG234', '(fd_set *)', quote=0)
    # Define to the type of arg 5 for `select'. */
    #dfn('SELECT_TYPE_ARG5', '(struct timeval *)', quote=0)


    #dfn('__cplusplus', 1)

    # let compiler know that we have 'config.h'
    
    # portable adding define, should work gcc and msvc
    env.append_value('CXXFLAGS', env['CXXDEFINES_ST'] % 'HAVE_CONFIG_H')
    env.append_value('CCFLAGS', env['CCDEFINES_ST'] % 'HAVE_CONFIG_H')

    conf.write_config_header('config.h')

    # process configure for subfolders
    conf.sub_config('src/editor') # generate Editor source from idl



def build(bld):

    # process subfolders
    bld.add_subdirs("""
        src/backend
        src/editor
        src/main
        src/gnome2
        ui
    """)
    # use GECKO
    if not bld.env['ENABLE_GTKHTML']:
        bld.add_subdirs('src/gecko')

    bld.install_files('${PACKAGE_DOC_DIR}', """
        README
	RELEASE-NOTES
	COPYING
	COPYING-DOCS
	AUTHORS
	ChangeLog
	INSTALL
	NEWS
	TODO
	Xiphos.ogg
        help/xiphos.pdf
    """)

    bld.install_files('${PACKAGE_PIXMAPS_DIR}','pixmaps/*')

    # handle .desktop creation and installation
    if not bld.env["IS_WIN32"]:
        bld.new_task_gen(
                features='subst',
                source='xiphos.desktop.in.in',
                target='xiphos.desktop.in',
                dict={'xiphos_exec':'xiphos',
                      'PACKAGE_PIXMAPS_DIR': bld.env['PACKAGE_PIXMAPS_DIR']})
        bld.new_task_gen(
                features='intltool_in',
                source='xiphos.desktop.in',
                target='xiphos.desktop',
                install_path='${PACKAGE_MENU_DIR}',
                podir='po',
                flags='-d')


    #mkenums marshal pixmaps')

    #env = bld.env
    #if env['XML2PO'] and env['XSLTPROC2PO']:
        #bld.add_subdirs('help')

    if bld.env['INTLTOOL']:
        bld.add_subdirs('po')

    #if env['HAVE_GTKSHARP'] and env['MCS']:
        #bld.add_subdirs('sharp')

    #if env['SGML2MAN']:
    #	bld.add_subdirs('man')


def shutdown():
    # Postinstall tasks:
    #gnome.postinstall_srrcrollkeeper('gnome-hello') # Installing the user docs
    #gnome.postinstall_schemas('gnome-test') # Installing GConf schemas
    #gnome.postinstall_icons() # Updating the icon cache
    pass

def distclean():

    ### editor.py
    lst = ('''
        src/editor/Editor-common.c
        src/editor/Editor.h
        src/editor/Editor-skels.c
        src/editor/Editor-stubs.c
    ''').split()

    print 'Removing files generated for editor:'
    for i in lst:
        if os.path.exists(i):
            print i
            os.remove(i)
    ### END editor.py

