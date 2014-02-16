%global owner ojuba-org
%global commit #Write commit number here

Name:		ojuba-virtual-cd
Summary:	Virtual CD/DVD using fuseiso
Version:	0.3.2
Release:	2
License:	WAQFv2
Group:		System Environment/Base
URL:		http://ojuba.org
Source:		https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Requires:	fuseiso
Requires:	python2
Requires:	pygobject3 >= 3.0.2
BuildRequires:	python2-devel
BuildRequires:	intltool
BuildArch:      noarch

%description
Virtual CD/DVD using fuseiso

%prep
%setup -q -n %{name}-%{commit}

%build
make %{?_smp_mflags}

%install
%makeinstall DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README waqf2-ar.pdf
%{_bindir}/%{name}
%{python2_sitelib}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/locale/*/*/*.mo

%changelog
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
