#Module-Specific definitions
%define mod_name mod_auth_sdb
%define mod_conf 95_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.12
Release:	21
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

#%{_bindir}/apxs -c %{mod_name}.c -Wl,-lsdb

%{_bindir}/apxs \
    -c %{mod_name}.c \
    `%{_bindir}/sdb-config --cflags` \
    `%{_bindir}/sdb-config --libs`

%install

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

%files
%doc ChangeLog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-20mdv2012.0
+ Revision: 772580
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-19
+ Revision: 678270
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-18
+ Revision: 645764
- relink against libmysqlclient.so.18

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-17mdv2011.0
+ Revision: 587928
- rebuild

* Fri Apr 23 2010 Funda Wang <fwang@mandriva.org> 1:0.12-16mdv2010.1
+ Revision: 538080
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-15mdv2010.1
+ Revision: 516057
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-14mdv2010.0
+ Revision: 406545
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-13mdv2009.1
+ Revision: 326481
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-12mdv2009.1
+ Revision: 325564
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-11mdv2009.0
+ Revision: 234669
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-10mdv2009.0
+ Revision: 215538
- fix rebuild
- fix buildroot

* Sat Mar 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-9mdv2008.1
+ Revision: 182161
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.12-8mdv2008.1
+ Revision: 170710
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-7mdv2008.0
+ Revision: 82525
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.12-6mdv2007.1
+ Revision: 140620
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-5mdv2007.0
+ Revision: 79337
- Import apache-mod_auth_sdb

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-4mdv2007.0
- rebuild

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-3mdk
- rebuilt against apache-2.2.0 (P1)

* Thu Dec 01 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-2mdk
- rebuilt against openssl-0.9.8a

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.12-1mdk
- rebuilt against MySQL-5.0.15
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.12-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.12-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.12-4mdk
- use the %macro

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.12-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.12-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.12-1mdk
- rebuilt for apache 2.0.53

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.12-2mdk
- rebuilt against MySQL-4.1.x system libs
- rebuilt against sdb-0.6.0 libs
- nuke redundant deps

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.12-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.12-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.12-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.12-1mdk
- built for apache 2.0.49

