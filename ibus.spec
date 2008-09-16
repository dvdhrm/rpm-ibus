%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define mod_path ibus-0.1
Name:       ibus
Version:    0.1.1.20080916
Release:    1%{?dist}
Summary:    Intelligent Input Bus for Linux OS
License:    LGPLv2+
Group:      System Environment/Libraries
URL:        http://code.google.com/p/ibus/
Source0:    http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:    xinput-ibus

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  python
BuildRequires:  gtk2-devel
BuildRequires:  qt-devel
BuildRequires:  dbus-glib-devel

Requires:   pygtk2
Requires:   dbus-python >= 0.83.0
Requires:   gnome-python2-gconf
Requires:   pyxdg

%description
IBus means Intelligent Input Bus. It is a new input framework for Linux OS. It provides
full featured and user friendly input method user interface. It also may help
developers to develop input method easily.

%package gtk
Summary:    iBus im module for gtk2
Group:      System Environment/Libraries
Requires:   %{name} = %{version}-%{release}

%description gtk
This package contains ibus im module for gtk2

%package qt
Summary:    iBus im module for qt4
Group:      System Environment/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   qt >= 4.4.1

%description qt
This package contains ibus im module for qt4

%define _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/ibus.conf

%prep
%setup -q

%build
%configure --disable-static
# make -C po update-gmo
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f $RPM_BUILD_ROOT%{_libdir}/libibus-gtk.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libibus-gtk.so
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/immodules/im-ibus.la

# install xinput config file
mkdir -pm 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/X11/xinit/xinput.d
install -pm 644 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_xinputconf}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post gtk
%{_bindir}/update-gtk-immodules %{_host} || :

%postun gtk
%{_bindir}/update-gtk-immodules %{_host} || :

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{python_sitelib}/ibus
%{python_sitelib}/ibus/*
%dir %{_datadir}/ibus/
%dir %{_datadir}/ibus/daemon/
%dir %{_datadir}/ibus/gconf/
%dir %{_datadir}/ibus/panel/
%dir %{_datadir}/ibus/setup/
%dir %{_datadir}/ibus/engine/
%dir %{_datadir}/ibus/icons/
%{_bindir}/ibus
%{_bindir}/ibus-setup
%{_libdir}/libibus-gtk.so*
%{_datadir}/ibus/daemon/*
%{_datadir}/ibus/gconf/*
%{_datadir}/ibus/panel/*
%{_datadir}/ibus/setup/*
%{_datadir}/ibus/icons/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_bindir}/ibus-daemon
%{_bindir}/ibus-gconf
%{_bindir}/ibus-panel
%{_bindir}/ibus-x11
%config %{_xinputconf}

%files gtk
%defattr(-,root,root,-)
%doc
%{_libdir}/gtk-2.0/immodules/im-ibus.so

%files qt
%defattr(-,root,root,-)
%doc
%{_libdir}/qt4/plugins/inputmethods/libibus.so

%changelog
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
