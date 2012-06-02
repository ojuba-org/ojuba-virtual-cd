Name:		ojuba-virtual-cd
Summary:	Virtual CD/DVD using fuseiso
Version:	0.3.2
Release:	1
License:	Waqf
Group:		System Environment/Base
URL:		http://www.ojuba.org
Source:		http://git.ojuba.org/cgit/%{name}/snapshot/%{name}-%{version}.tar.bz2
Requires:	fuseiso python
Requires:   pygobject3 >= 3.0.2
BuildRequires:  intltool
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
Virtual CD/DVD using fuseiso

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE-en LICENSE-ar.txt README
%{_bindir}/%{name}
%{python_sitelib}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/locale/*/*/*.mo

%changelog
* Sun Jun 2 2012 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.3.2-1
- port to gtk3

* Sun Jul 19 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.3.0-5
- add session management
- use ~/.virtuals instead of system /mnt/virtuals
- try to use labels from output of blkid or file
- remove emptry dirs in mount point prefix

* Sat Dec 20 2008 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.2.0-1
- fix permissions to allow all users to share

