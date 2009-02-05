%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?gtk_binary_version: %define gtk_binary_version %(pkg-config  --variable=gtk_binary_version gtk+-2.0)}
%define mod_path ibus-1.1
Name:       ibus
Version:    1.1.0.20090205
Release:    1%{?dist}
Summary:    Intelligent Input Bus for Linux OS
License:    LGPLv2+
Group:      System Environment/Libraries
URL:        http://code.google.com/p/ibus/
Source0:    http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:    xinput-ibus

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define glib_ver %([ -a %{_libdir}/pkgconfig/glib-2.0.pc ] && pkg-config --modversion glib-2.0 | cut -d. -f 1,2 || echo -n "999")

BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  python
BuildRequires:  gtk2-devel
BuildRequires:  dbus-devel
BuildRequires:  qt-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk-doc
BuildRequires:  GConf2-devel
BuildRequires:  pygobject2-devel

Requires(post):  desktop-file-utils
Requires(post):  %{_sbindir}/alternatives
Requires(postun):  desktop-file-utils
Requires(postun):  %{_sbindir}/alternatives

Requires:   glib2 >= %{glib_ver}
Requires:   pygtk2
Requires:   dbus-python >= 0.83.0
Requires:   gnome-python2-gconf
Requires:   notification-daemon
Requires:   pyxdg
Requires:   iso-codes

Obsoletes: 	ibus-anthy <= 1.1.0, ibus-pinyin <= 1.1.0, ibus-m17n <= 1.1.0, ibus-hangul <= 1.1.0, ibus-chewing <= 1.1.0

%define _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/ibus.conf

%description
IBus means Intelligent Input Bus. It is a new input framework for Linux OS. It provides
full featured and user friendly input method user interface. It also may help
developers to develop input method easily.

%package gtk
Summary:    IBus im module for gtk2
Group:      System Environment/Libraries
Requires:   %{name} = %{version}-%{release}

%description gtk
This package contains ibus im module for gtk2

# %package qt
# Summary:    IBus im module for qt4
# Group:      System Environment/Libraries
# Requires:   %{name} = %{version}-%{release}
# Requires:   qt >= 4.4.2
# 
# %description qt
# This package contains ibus im module for qt4

%package devel
Summary:    Development tools for ibus
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   glib2-devel
Requires:   dbus-devel
Requires:   gtk-doc

%description devel
The ibus-devel package contains the header files and developer
docs for ibus.

%prep
%setup -q

%build
%configure --disable-static \
		   --disable-iso-codes-check \
		   --enable-gtk-doc \
		   --disable-qt4-immodule
# make -C po update-gmo
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f $RPM_BUILD_ROOT%{_libdir}/libibus.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/%{gtk_binary_version}/immodules/im-ibus.la

# install xinput config file
mkdir -pm 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/X11/xinit/xinput.d
install -pm 644 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_xinputconf}

# install .desktop files
desktop-file-install --delete-original          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
update-desktop-database -q
%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_xinputconf} 83 || :

%post gtk
%{_bindir}/update-gtk-immodules %{_host} || :

%postun
/sbin/ldconfig
update-desktop-database -q
if [ "$1" = "0" ]; then
  %{_sbindir}/alternatives --remove xinputrc %{_xinputconf} || :
  # if alternative was set to manual, reset to auto
  [ -L %{_sysconfdir}/alternatives/xinputrc -a "`readlink %{_sysconfdir}/alternatives/xinputrc`" = "%{_xinputconf}" ] && %{_sbindir}/alternatives --auto xinputrc || :
fi

%postun gtk
%{_bindir}/update-gtk-immodules %{_host} || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{python_sitelib}/ibus
%{python_sitelib}/ibus/*
%dir %{_datadir}/ibus/
%{_bindir}/ibus-daemon
%{_bindir}/ibus-setup
%{_libdir}/libibus.so*
%{_datadir}/ibus/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_libexecdir}/ibus-gconf
%{_libexecdir}/ibus-ui-gtk
%{_libexecdir}/ibus-x11
%config %{_xinputconf}

%files gtk
%defattr(-,root,root,-)
%{_libdir}/gtk-2.0/%{gtk_binary_version}/immodules/im-ibus.so

# %files qt
# %defattr(-,root,root,-)
# %{_libdir}/qt4/plugins/inputmethods/libibus.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*

%changelog
* Thu Feb 05 2009 Huang Peng <shawn.p.huang@gmail.com> - 1.1.0.20090205-1
- Update to 1.1.0.20090205.

* Tue Feb 03 2009 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20090203-1
- Update to 0.1.1.20090203.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081023-3
- Rebuild for Python 2.6

* Wed Nov 19 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081023-2
- Move libibus-gtk.so from ibus.rpm to ibus-gtk.rpm to fix bug 472146.

* Thu Oct 23 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081023-1
- Update to 0.1.1.20081023.

* Thu Oct 16 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081016-1
- Update to 0.1.1.20081016.

* Tue Oct  7 2008 Jens Petersen <petersen@redhat.com> - 0.1.1.20081006-3
- remove the empty %%doc file entries

* Tue Oct  7 2008 Jens Petersen <petersen@redhat.com> - 0.1.1.20081006-2
- add xinputrc alternative when installing or uninstalling

* Mon Oct 06 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081006-1
- Update to 0.1.1.20081006.

* Sun Oct 05 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081005-1
- Update to 0.1.1.20081005.

* Sat Oct 04 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081004-1
- Update to 0.1.1.20081004.

* Wed Oct 01 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081001-1
- Update to 0.1.1.20081001.

* Tue Sep 30 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080930-1
- Update to 0.1.1.20080930.

* Tue Sep 23 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080923-1
- Update to 0.1.1.20080923.

* Wed Sep 17 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080917-1
- Update to 0.1.1.20080917.

* Tue Sep 16 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080916-1
- Update to 0.1.1.20080916.

* Mon Sep 15 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080914-1
- Update to 0.1.1.20080914.

* Mon Sep 08 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080908-1
- Update to 0.1.1.20080908.

* Mon Sep 01 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Sat Aug 30 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080830-1
- Update to 0.1.1.20080830.

* Mon Aug 25 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080825-1
- Update to 0.1.1.20080825.

* Sat Aug 23 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080823-1
- Update to 0.1.1.20080823.

* Fri Aug 15 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080815-1
- Update to 0.1.1.20080815.

* Thu Aug 12 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080812-1
- Update to 0.1.1.20080812.

* Mon Aug 11 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.0.20080810-2
- Add gnome-python2-gconf in Requires.

* Thu Aug 07 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.0.20080810-1
- The first version.
