%global owner ojuba-org
%global commit #Write commit number here

Name: ojuba-virtual-cd
Summary: Virtual CD/DVD Driver
Summary(ar): محرك أقراص وهمية
Version: 0.3.2
Release: 3%{?dist}
License: WAQFv2
URL: http://ojuba.org
Source: https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
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
%setup -q -n %{name}-%{commit}

%build
make %{?_smp_mflags}

%install
%make_install

%files
%license waqf2-ar.pdf
%doc README
%{_bindir}/%{name}
%{python2_sitelib}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/locale/*/*/*.mo

%changelog
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
