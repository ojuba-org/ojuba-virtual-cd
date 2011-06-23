Name:		ojuba-virtual-cd
Summary:	Virtual CD/DVD using fuseiso
Version:	0.3.0
Release:	5
License:	Waqf
Group:		System Environment/Base
URL:		http://www.ojuba.org
Source:		http://git.ojuba.org/cgit/%{name}/snapshot/%{name}-%{version}.tar.bz2
Requires:	fuseiso python pygtk2
BuildRequires:  intltool
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
Virtual CD/DVD using fuseiso

%prep
%setup -q

%build
./gen-mo.sh
%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/applications/
cp -pa locale $RPM_BUILD_ROOT%{_datadir}/
install -p -m 644 %{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/
install -p -m 755 %{name} $RPM_BUILD_ROOT%{_bindir}

%files
%defattr(-,root,root,-)
%doc LICENSE-en LICENSE-ar.txt README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/locale/*/*/*.mo

%changelog
* Sun Jul 19 2009 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.3.0-5
- add session management
- use ~/.virtuals instead of system /mnt/virtuals
- try to use labels from output of blkid or file
- remove emptry dirs in mount point prefix

* Sat Dec 20 2008 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.2.0-1
- fix permissions to allow all users to share

