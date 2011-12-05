%define pkgname twm

Summary: X.Org X11 twm window manager
Name: xorg-x11-%{pkgname}
# NOTE: Remove Epoch line if package gets renamed to something like "twm"
Epoch: 1
Version: 1.0.3
Release: 5.1%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.x.org/pub/individual/app/%{pkgname}-%{version}.tar.bz2

BuildRequires: pkgconfig
# checking TWM_LIBS... -lXmu -lXt -lSM -lICE -lXext -lX11 -ldl
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXmu-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXext-devel
# FIXME: twm fails to link to libXau, however upstream ./configure checks, do
# not check for libXau in X11R7 RC2.  fdo#5065
BuildRequires: libXau-devel

# FIXME: monolithic twm packaging has a hard dep on xterm, which might still
# be required.  We'll have to examine the twm configuration files.
#Requires: xterm
Provides: twm

Obsoletes: XFree86-twm
# NOTE: The twm.1 manpage was moved from the XFree86 package to the twm
# package to fix bug #70025 on July 29 2002.  This must remain here as
# long as we support upgrading from OS releases that contained a version
# of XFree86 less than that indicated, both for the RHEL case, RHL case,
# and Fedora Core case. - Mike A. Harris<mharris@redhat.com>
Conflicts: XFree86 <= 4.2.0-57.1

%description
X.Org X11 twm window manager

%prep
%setup -q -n %{pkgname}-%{version}

%build
# FIXME: Work around pointer aliasing warnings from compiler for now
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Upstream sources do not create the system wide twm config dir, nor
# install the default config file currently.  We'll work around it here for now.
{
   echo "FIXME: Upstream doesn't install systemwide config by default"
   mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/twm
   install -m 0644 src/system.twmrc $RPM_BUILD_ROOT%{_sysconfdir}/X11/twm/
   rm $RPM_BUILD_ROOT%{_datadir}/X11/twm/system.twmrc
}
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README ChangeLog
%{_bindir}/twm
#%dir %{_mandir}/man1x
%{_mandir}/man1/twm.1*
%dir %{_sysconfdir}/X11/twm
%config %{_sysconfdir}/X11/twm/system.twmrc

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:1.0.3-5.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.3-3
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0.3-2
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Dave Airlie <airlied@redhat.com> - 1.0.3-1
- Upgrade to 1.0.3 - fix URI for source
- no sure about the system.twmrc, rm the spare copy for now

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1:1.0.1-4
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.0.1-4
- Don't install INSTALL

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.0.1-3.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-3
- Bump and rebuild with minor specfile cleanups.
- Add documentation to doc list, even though half of it is 0 bytes. Ah well.

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-2
- Added "BuildRequires: pkgconfig" for (#194186)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-1
- Updated to twm 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1:1.0.0-1
- Updated to twm 1.0.0 from X11R7 RC4.
- Change manpage dir from man1x to man1 to match RC4 default.

* Tue Nov 15 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-4
- Added "BuildRequires: libXau-devel", as twm fails without it, but does not
  check for it with ./configure.  Bug (fdo#5065)

* Wed Nov 02 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-3
- Actually spell RPM_OPT_FLAGS correctly this time.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-2
- Build with -fno-strict-aliasing to work around possible pointer aliasing
  issues

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-1
- Updated to twm 0.99.1 from X11R7 RC1.
- Added Epoch 1 to package, to be able to change the version number from the
  X11R7 release number to the actual twm version.
- Change manpage location to 'man1x' in file manifest

* Wed Oct 05 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-2
- Update BuildRequires to match new library naming scheme
- Use Fedora Extras style BuildRoot declaration

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-1
- Initial build.
