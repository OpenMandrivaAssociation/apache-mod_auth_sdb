#Module-Specific definitions
%define mod_name mod_auth_sdb
%define mod_conf 95_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_auth_sdb is a DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.12
Release:	%mkrel 7
Group:		System/Servers
License:	Apache License
URL:		http://shebang.jp/src/apache/
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_auth_sdb-0.12-register.patch
Patch1:		mod_auth_sdb-0.12-apache220.diff
BuildRequires:	sdb-devel
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This module provides Apache user authentication using LibSDB.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

#%{_sbindir}/apxs -c %{mod_name}.c -Wl,-lsdb

%{_sbindir}/apxs \
    -c %{mod_name}.c \
    `%{_bindir}/sdb-config --cflags` \
    `%{_bindir}/sdb-config --libs`

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


