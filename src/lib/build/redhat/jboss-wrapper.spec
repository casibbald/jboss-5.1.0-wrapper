%define __os_install_post %{nil}
%define debug_package %{nil}
%define _prefix	/data0 

Name		: jboss-wrapper
Version		: 1
Release		: 3

License		: LGPL
Summary		: JBoss Wrapper
Group		: Applications/Internet

URL		: https://github.com/casibbald/jboss-5.1.0-wrapper
Vendor		: Charles Sibbald
Packager	: Yasser Nabi <ynabi@fsa.gov.uk>

BuildRoot	: %{_builddir}/%{name}-%{version}-buildroot
Source0		: jboss-wrapper.tar.gz
Source1		: jboss-wrapper.init
Source2		: jboss-wrapper.sysconfig
Prefix		: %{_prefix}
Requires	: jdk >= 1.6.0_24, jboss5, cronolog

%description
JBoss Application Server (or JBoss AS) is a free software/open-source Java EE-based application server. An important distinction for this class of software is that it not only implements a server that runs on Java, but it actually implements the Java EE part of Java. Because it is Java-based, the JBoss application server operates cross-platform: usable on any operating system that supports Java. JBoss AS was developed by JBoss, now a division of Red Hat (http://en.wikipedia.org/wiki/JBoss_application_server)

The jboss-wrapper is used to manage application deployment to JBoss

%pre

%prep
%setup -c -n %{buildroot}/%{_prefix}

%build

%install
%{__install} -D -m 744 %{SOURCE1} %{buildroot}/%{_initrddir}/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

%post

%clean
rm -rf %{buildroot}

%postun

%files 
#####################################################
# defattr sets the default attributes for all files
#####################################################
%attr(770, jboss, jboss) %{prefix}/%{name}
%attr(-, root, root) %{_initrddir}/%{name}
%config %attr(-, root, root) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Mon Mar 26 2012 Yasser Nabi <ynabi@fsa.gov.uk> 1-3
- Added cronolog requirement

* Fri Mar 23 2012 Yasser Nabi <ynabi@fsa.gov.uk> 1-2
- Intial jboss-wrapper package

* Fri Mar 23 2012 Yasser Nabi <ynabi@fsa.gov.uk> 1-1
- Intial jboss-wrapper package
