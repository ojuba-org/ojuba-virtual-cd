%global owner ojuba-org

Name: ojuba-virtual-cd
Summary: Virtual CD/DVD Driver
Summary(ar): محرك أقراص وهمية
Version: 0.4
Release: 1%{?dist}
License: WAQFv2
URL: http://ojuba.org
Source: https://github.com/%{owner}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Requires: fuseiso
Requires: python2
Requires: pygobject3 >= 3.0.2
BuildRequires: python2-devel
BuildRequires: intltool
BuildArch: noarch

%description
Virtual CD/DVD using fuseiso

%description -l ar
محرّك أقراص وهمية متوافق مع فيوزآيزو

%prep
%autosetup -n %{name}-%{version}

%build
make %{?_smp_mflags}

%install
%make_install



# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2017 Mosaab Alzoubi <moceap@hotmail.com> -->
<!--
EmailAddress: moceap@hotmail.com
SentUpstream: 2017-2-18
-->
<application>
  <id type="desktop">%{name}.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <summary>Virtual CD/DVD Driver</summary>
  <summary xml:lang="ar">محرك أقراص وهمية</summary>
  <description>
    <p>
	Virtual CD/DVD Driver.
    </p>
  </description>
  <description xml:lang="ar">
    <p>
	محرك أقراص وهمية.
    </p>
  </description>
  <url type="homepage">https://github.com/ojuba-org/%{name}</url>
  <screenshots>
    <screenshot type="default">http://ojuba.org/screenshots/%{name}.png</screenshot>
  </screenshots>
  <updatecontact>moceap@hotmail.com</updatecontact>
</application>
EOF



%files
%license waqf2-ar.pdf
%doc README
%{_bindir}/%{name}
%{python2_sitelib}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/locale/*/*/*.mo

%changelog
* Sun Feb 19 2017 Mosaab Alzoubi <moceap@hotmail.com> - 0.4-1
- Update to 0.4
- Support Wayland
- New Icon
- Add Arabic data
- New way to Github
- Add Appdata

* Wed Jul 22 2015 Mosaab Alzoubi <moceap@hotmail.com> - 0.3.2-3
- Gereral Revision
- Add Arabic Summary and Discription
- Fix requires
- Use %%make_install
- Remove old ATTR way
- Remove Group tag
- Use %%license

* Sun Feb 16 2014 Mosaab Alzoubi <moceap@hotmail.com> - 0.3.2-2
- General Revision.

* Sun Jun 2 2012 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.3.2-1
- port to gtk3

* Sun Jul 19 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.3.0-5
- add session management
- use ~/.virtuals instead of system /mnt/virtuals
- try to use labels from output of blkid or file
- remove emptry dirs in mount point prefix

* Sat Dec 20 2008 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.2.0-1
- fix permissions to allow all users to share
