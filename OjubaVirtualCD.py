# -*- coding: UTF-8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
"""
Ojuba Virtual CD
Copyright © 2011, Ojuba Team <core@ojuba.org>

PyGtk+ front-end for fuseiso

        Released under terms of Waqf Public License.
        This program is free software; you can redistribute it and/or modify
        it under the terms of the latest version Waqf Public License as
        published by Ojuba.org.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

        The Latest version of the license can be found on
        "http://www.ojuba.org/wiki/doku.php/رخصة_وقف_العامة"

"""

import sys,os,os.path
import time
from gi.repository import Gtk, GObject
from subprocess import Popen,PIPE
import gettext
import re
from glob import glob

label_re=re.compile(r"""'([^']+)'""")

mount_prefix=os.path.expanduser('~/.virtuals')
_ps=[]
gettext.install('ojuba-virtual-cd', "/usr/share/locale", unicode=0)

def run_in_bg(cmd):
    global _ps
    setsid = getattr(os, 'setsid', None)
    if not setsid: setsid = getattr(os, 'setpgrp', None)
    _ps=filter(lambda x: x.poll()!=None,_ps) # remove terminated processes from _ps list
    _ps.append(Popen(cmd,0,'/bin/sh',shell=True, preexec_fn=setsid))

def get_pids(l):
    pids=[]
    for i in l:
        p=Popen(['/sbin/pidof',i], 0, stdout=PIPE)
        l=p.communicate()[0].strip().split()
        r=p.returncode
        if r==0: pids.extend(l)
    pids.sort()
    return pids

def get_desktop():
    """return 1 for kde, 0 for gnome, -1 none of them"""
    l=get_pids(('kwin','ksmserver',))
    if l: kde=l[0]
    else: kde=None
    l=get_pids(('gnome-session',))
    if l: gnome=l[0]
    else: gnome=None
    if kde:
        if not gnome or kde<gnome: return 1
        else: return 0
    if gnome: return 0
    else: return -1

def run_file_man(mp):
    # TODO: add Dolphin here
    if get_desktop()==0: run_in_bg("nautilus --no-desktop '%s'" % mp)
    elif get_desktop()==1: run_in_bg("konqueror '%s'" % mp)
    elif os.path.exists('/usr/bin/thunar'): run_in_bg("thunar '%s'" % mp)
    elif os.path.exists('/usr/bin/pcmanfm'): run_in_bg("pcmanfm '%s'" % mp)
    elif os.path.exists('/usr/bin/nautilus'): run_in_bg("nautilus --no-desktop '%s'" % mp)
    elif os.path.exists('/usr/bin/konqueror'): run_in_bg("konqueror '%s'" % mp)

def bad(msg):
    dlg = Gtk.MessageDialog (None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE,
            msg)
    dlg.run()
    dlg.destroy()
    
def check_mount_prefix():
    if not os.path.exists(mount_prefix):
        try: os.makedirs(mount_prefix)
        except OSError:
            bad( _("Mount prefix [%s] is not found, please create it.") % mount_prefix )
            sys.exit(1)

class VCDAbout(Gtk.AboutDialog):
    def __init__(self, parent=None):
        Gtk.AboutDialog.__init__(self, parent=parent)
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.connect('delete-event', lambda w, *a: w.hide() or True)
        self.connect('response', lambda w, *a: w.hide() or True)
        try: self.set_program_name("ojuba-virtual-cd")
        except: pass
        self.set_name(_("Ojuba Virtual CD"))
        #about_dlg.set_version(version)
        self.set_copyright("Copyright (c) 2008-2009 Muayyad Saleh Alsadi <alsadi@ojuba.org>")
        self.set_comments(_("Mount CD/DVD images (iso, nrg, bin, mdf, img, ..etc.)"))
        self.set_license("""
        Released under terms on Waqf Public License.
        This program is free software; you can redistribute it and/or modify
        it under the terms of the latest version Waqf Public License as
        published by Ojuba.org.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

        The Latest version of the license can be found on
        "http://www.ojuba.org/wiki/doku.php/waqf/license"

        """)
        self.set_website("http://virtualcd.ojuba.org/")
        self.set_website_label("http://virtualcd.ojuba.org")
        self.set_authors(["Muayyad Saleh Alsadi <alsadi@ojuba.org>", "a.atalla <a.atalla@linuxac.org>"])
        self.run()
        self.destroy()
        
class VCD_mount_dlg(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self,_("Select CD/DVD image file"),buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT, Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        ff=Gtk.FileFilter()
        ff.add_mime_type('application/x-cd-image')
        for i in ('iso','nrg', 'bin','mdf','img'):
            l=list(i)
            ff.add_pattern('*.[%s%s][%s%s][%s%s]' % ( l[0],l[0].upper(), l[1],l[1].upper(), l[2],l[2].upper()))
        self.set_filter(ff)
        self.connect('delete-event', lambda w, *a: w.hide() or True)
        self.connect('response', lambda w, *a: w.hide() or True)

class VCDStatusIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.connect ('popup-menu', self.right_click_event)
        self.set_title(_("OjubaVirtualCD"))
        self.set_from_stock(Gtk.STOCK_CDROM)
        
        self.mount_dlg = VCD_mount_dlg()
        #self.about_dlg = VCDAbout()
        
        self.setup_popup_menu()
        self.startUP()
        self.refresh_cb()
        
        self.set_visible(True)
        
        GObject.timeout_add(15000, self.refresh_timer)
        
    def startUP(self):
        if len(sys.argv)>1:
            if (sys.argv[1]!='--hidden'):
                for i in sys.argv[1:]: self.mount_f(i)
        else: self.mount_cb()
        
    def setup_popup_menu(self):
        self.popup_menu = Gtk.Menu()
        self.mounted_menu = Gtk.Menu()
        self.open_menu = Gtk.Menu()
        
        i = Gtk.MenuItem(_("Mount image"))
        i.connect('activate', self.mount_cb)
        self.popup_menu.add(i)

        # self.mounted_menu.add(Gtk.SeparatorMenuItem())
        i = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_REFRESH, None)
        i.connect('activate', self.refresh_cb)
        i.set_always_show_image(True)
        self.mounted_menu.add(i)
        
        self.open_menu.add(Gtk.SeparatorMenuItem())
        
        i = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_REFRESH, None)
        i.connect('activate', self.refresh_cb)
        i.set_always_show_image(True)
        self.open_menu.add(i)
        
        self.popup_menu.add(Gtk.SeparatorMenuItem())

        self.open_menu_item=i= Gtk.MenuItem(_("Open mounted image"))
        i.set_submenu(self.open_menu)
        self.popup_menu.add(i)


        self.umount_menu_item=i= Gtk.MenuItem(_("Unmount"))
        i.set_submenu(self.mounted_menu)
        self.popup_menu.add(i)

        self.popup_menu.add(Gtk.SeparatorMenuItem())

        i =    Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT, None)
        i.connect('activate', self.about_cb)
        i.set_always_show_image(True)
        self.popup_menu.add(i)
        
        i = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT,None)
        i.connect('activate', Gtk.main_quit)
        i.set_always_show_image(True)
        self.popup_menu.add(i)

    def right_click_event(self, icon, button, time):
        self.popup_menu.show_all()
        self.popup_menu.popup(None, None, Gtk.StatusIcon.position_menu, icon, button, time)

    def refresh_timer(self):
        self.refresh_cb(); return True;
        
    def refresh_cb(self, *args):
        self.popup_menu.popdown()
        mm = Gtk.Menu()
        oo = Gtk.Menu()
        for i in os.listdir(mount_prefix):
            mp = os.path.join(mount_prefix,i)
            if (os.path.ismount(mp)): 
                j = Gtk.MenuItem(i.decode(sys.getfilesystemencoding())) 
                o = Gtk.MenuItem(i.decode(sys.getfilesystemencoding())) 
                j.connect('activate', self.umount_cb, i)
                o.connect('activate', lambda a: run_file_man(mp))
                mm.add(j)
                oo.add(o) 
            mm.add(Gtk.SeparatorMenuItem())
            oo.add(Gtk.SeparatorMenuItem())
        i = Gtk.ImageMenuItem(Gtk.STOCK_REFRESH)
        i.connect('activate', self.refresh_cb)
        mm.add(i)
        i = Gtk.ImageMenuItem(Gtk.STOCK_REFRESH)
        i.connect('activate', self.refresh_cb)
        oo.add(i)
        mounted_menu = mm
        open_menu = oo
        g = self.open_menu_item.get_submenu()
        s = self.umount_menu_item.get_submenu()
        self.umount_menu_item.set_submenu(mm)
        self.open_menu_item.set_submenu(oo)
        del s, g

    def mount_f(self, fn):
        if not os.path.exists(fn): bad(_("File does not exist")); return -1
        l=self.get_label(fn)
        if not l: l=os.path.basename(fn)
        mp=os.path.join( mount_prefix, l )
        if os.path.exists(mp):
            if os.path.ismount(os.path.join(mp)): bad(_("Already mounted")); return -2
            try: os.rmdir(mp)
            except OSError: bad(_("Mount point [%s] already exists, remove it please!") % mp); return -1
        try: os.mkdir(mp)
        except: bad(_('Could not create folder [%s]') % mp.decode(sys.getfilesystemencoding()) ); return -1
        r=os.system('fuseiso -c UTF8 "%s" "%s"' % (fn, mp))
        if r: bad(_("Could not mount [%s]") % mp); return -1
        else: run_file_man(mp)
        self.refresh_cb()
        return 0
    def mount_cb(self, *args):
        if (self.mount_dlg.run()==Gtk.ResponseType.ACCEPT):
            self.mount_f(self.mount_dlg.get_filename())
        self.mount_dlg.hide()

    def get_label_from_blkid(self, fn):
        try:
            p=Popen(['blkid','-o','value','-s','LABEL',fn], 0, stdout=PIPE)
            l=p.communicate()[0].strip()
        except: return None
        r=p.returncode
        if r==0 and l and len(l)>0: return l
        else: return None
    
    def get_label_from_file(self, fn):
        try:
            p=Popen(['file',fn], 0, stdout=PIPE)
            o=p.communicate()[0].split(':',1)[1].strip()
            l=label_re.findall(o)[0].strip()
        except: return None
        r=p.returncode
        if r==0 and l and len(l)>0: return l
        else: return None
    
    def get_label(self, fn):
        return self.get_label_from_blkid(fn) or self.get_label_from_file(fn)

    def umount_cb(self, i, mp): 
        mpp=os.path.join(mount_prefix,mp.encode(sys.getfilesystemencoding()))
        r=os.system("fusermount -u '%s'" % mpp)
        if r: bad(_("Could not unmount [%s]") % mp)
        else: os.rmdir(mpp)
        self.refresh_cb()

    def about_cb(self, *args):
        #self.about_dlg.run()
        return VCDAbout()
    
bus, bus_name, bus_object=None,None,None
try:
    import dbus
    import dbus.service
    #import GObject # for GObject.MainLoop() if no Gtk is to be used
    from dbus.mainloop.glib import DBusGMainLoop

    dbus_loop = DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
except ImportError: pass

def init_dbus():
    global bus_name, bus_object, app
    if not bus: return
    class Manager(dbus.service.Object):
        def __init__(self, bus, path):
                    dbus.service.Object.__init__(self,bus,path)

        @dbus.service.method("org.ojuba.VirtualCD", in_signature='as', out_signature='i')
        def Mount(self,a):
            r=0
            for fn in a: r|=app.mount_f(fn)
            return r

        @dbus.service.method("org.ojuba.VirtualCD", in_signature='', out_signature='s')
        def Version(self):
            return "0.3.0"
    # values from /usr/include/dbus-1.0/dbus/dbus-shared.h
    r=bus.request_name('org.ojuba.VirtualCD', flags=0x4)
    if r!=1:
        print "Another process own OjubaVirtualCD Service, pass request to it: "
        trials=0; appletbus=False
        while(appletbus==False and trials<20):
            print ".",
            try:
                appletbus=bus.get_object("org.ojuba.VirtualCD","/Manager"); break
            except:
                appletbus=False
            time.sleep(1); trials+=1
        print "*"
        if len(sys.argv)==1: print "already running and no arguments passed"; exit(-1)
        if appletbus: exit(appletbus.Mount(sys.argv[1:],dbus_interface='org.ojuba.VirtualCD'))
        else: print "unable to connect"
        exit(-1)
    bus_name = dbus.service.BusName("org.ojuba.VirtualCD", bus)
    bus_object = Manager(bus, '/Manager')

def main():
    global app
    check_mount_prefix()
    for i in glob(os.path.join(mount_prefix,'*')):
        if os.path.isdir(i):
            try: os.rmdir(i)
            except: pass
    init_dbus()
    app = VCDStatusIcon()
    try: Gtk.main()
    except KeyboardInterrupt: print "Exiting..."
    
if __name__ == '__main__':
    main()

