Summary:	Daemon for transparent IP (Layer 3) proxy ARP bridging
Summary(pl):	Demon do przezroczystego bridgowania IP proxy ARP (w warstwie 3)
Name:		parprouted
Version:	0.63
Release:	1
Epoch:		1
License:	GPL
Group:		Daemons
Source0:	http://www.hazard.maks.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	12753098a22e82997d1941d6d2284750
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.hazard.maks.net/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
parprouted is a daemon for transparent IP (Layer 3) proxy ARP
bridging. Unlike standard bridging, proxy ARP bridging allows to
bridge Ethernet networks behind wireless nodes. Normal L2 bridging
does not work between wireless nodes because wireless does not know
about MAC addresses used in the wired Ethernet networks.

%description -l pl
parprouted to demon do przezroczystego bridgowania IP proxy ARP (w
warstwie 3.). W przeciwieñstwie do standardowego bridgowania
bridgowanie proxy ARP pozwala na bridgowanie sieci ethernetowych za
bezprzewodowymi wêz³ami. Normalne bridgowanie w warstwie 2. nie dzia³a
pomiêdzy wêz³ami bezprzewodowymi poniewa¿ nie znaj± one adresów MAC
u¿ywanych w przewodowych sieciach Ethernet.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

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
%attr(754,root,root) /etc/rc.d/init.d/*
