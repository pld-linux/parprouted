Summary:	daemon for transparent IP (Layer 3) proxy ARP bridging
Name:		parprouted
Version:	0.42
Release:	2
Epoch:		1
License:	GPL
Group:		Daemon
Source0:	http://www.hazard.maks.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	7680ab8850c11d690eb5b802ae67edc1
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
URL:		http://freshmeat.net/projects/parprouted/
Requires(post,preun):   /sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
parprouted is a daemon for transparent IP (Layer 3) proxy ARP bridging.
Unlike standard bridging, proxy ARP bridging allows to bridge Ethernet
networks behind wireless nodes. Normal L2 bridging does not work
between wireless nodes because wireless does not know about MAC
addresses used in the wired Ethernet networks.

%prep
%setup -q 
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add parprouted
if [ -f /var/lock/subsys/parprouted ]; then
        /etc/rc.d/init.d/parprouted restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/parprouted start\" to start parprouted daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/parprouted ]; then
                /etc/rc.d/init.d/parprouted stop 1>&2
        fi
        /sbin/chkconfig --del parprouted
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README 
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
