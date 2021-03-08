Summary: nethserver-zabbix sets up the monitoring system
%define name nethserver-zabbix
Name: %{name}
%define version 0.0.1
%define release 8
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
#Requires: zabbix-web-pgsql-scl
Requires: nethserver-postgresql
Requires: zabbix-server-pgsql
Requires: zabbix-agent,zabbix-web,net-snmp-utils,php-pgsql
Requires: nethserver-rh-php73-php-fpm,nethserver-net-snmp
Requires: nmap
Conflicts: nethserver-zabbix22
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
NethServer Zabbix configuration
%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%attr(0440,root,root) /etc/sudoers.d/50_nsapi_nethserver_zabbix
%attr(0775,root,root) /usr/libexec/nethserver/api/%{name}/read
%attr(0770,root,root) /usr/local/bin/zabbixUnicode.sh
%attr(0770,root,root) /usr/local/bin/nethbackup_check
%attr(0755,postgres,postgres) /var/lib/nethserver/zabbix/backup
%doc COPYING


%package client
Summary: Zabbix client configuration
Requires: %{name} >= %{version}-%{release}
%description client
Zabbix client configuration
%files client -f client.lst
%defattr(-,root,root)
%doc COPYING
%doc README.rst
%dir %{_nseventsdir}/%{name}-client-update

#%pre
#getent passwd zabbix >/dev/null || useradd -m -d /var/lib/zabbix -s /bin/bash zabbix
#exit 0

%prep
%setup

%build

mkdir -p root/var/lib/nethserver/zabbix/backup
mkdir -p client/%{_nseventsdir}/%{name}-client-update
mkdir -p server/%{_nseventsdir}/%{name}-update

for package in server client; do
    if [[ -f createlinks-${package} ]]; then
        # Hack around createlinks output dir prefix, hardcoded as "root/":
        rm -f root
        ln -sf ${package} root
        perl createlinks-${package}
    fi
    ( cd ${package} ; %{makedocs} )
    %{genfilelist} ${PWD}/${package} | \
          grep -v -e '/etc/sudoers.d/' \
          >> ${package}.lst
    # !!! Do not create any file or directory after genfilelist invocation !!!
done


%install
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a ui/* %{buildroot}/usr/share/cockpit/%{name}/


for package in server client; do
    (cd ${package}; find . -depth -print | cpio -dump %{buildroot})
done

%post

%postun

%changelog
* Mon May 18 2020 Markus Neuberger <info@markusneuberger.at> - 0.0.1-8
- Add support for Zabbix 5 LTS - thanks to dz00te
* Mon Mar 23 2020 Markus Neuberger <info@markusneuberger.at> - 0.0.1-7
- Add new images - thanks to Andy Wismer
- Add Zabbix application to cockpit
- New zabbix DBs are created with unicode
- Add script zabbixUnicode to migrate old db to unicode
- Add HTTPS redirect
* Thu Mar 08 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-6
- Add backup-config - thanks to Andy Wismer
- Add backup-data - thanks to Andy Wismer
- Add zabbix postgresql db backup/restore - thanks to Andy Wismer
* Sun Feb 25 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-5
- Added nice map images - thanks to Andy Wismer
- Added backup script - thanks to Emiliano Vavassori
* Mon Jan 29 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-4
- Change from mysql to postgresql - thanks to Emiliano Vavassori
- Integrating zabbix service - thanks to Emiliano Vavassori
- Adding SNMP support and MIBs - thanks to Emiliano Vavassori
* Sat Jan 27 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-3
- Changed versioning
* Sat Dec 09 2017 Markus Neuberger <info@markusneuberger.at> - 0.0.1-2
- Added automatic initial config
* Mon Dec 04 2017 Markus Neuberger <info@markusneuberger.at> - 0.0.1-1
- Initial NS7 release
- Added conflicts nethserver-zabbix22
