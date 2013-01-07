%define __os_install_post %{nil}
%define debug_package %{nil}
%define _prefix /usr/local/jboss

Name		: pra-jboss5
Version		: 5.1.0.GA
Release		: 4

License		: LGPL
Summary		: JBoss Application Server
Group		: Applications/Internet

URL		: http://community.jboss.org/en/jbossa
Vendor		: Red Hat
Packager	: Yasser Nabi <ynabi@fsa.gov.uk>

BuildRoot	: %{_builddir}/%{name}-%{version}-buildroot
Source0		: jboss-5.1.0.GA.zip
Source1		: jboss.initd
Source2		: jboss.sysconfig
Prefix		: %{_prefix}
Requires	: jdk >= 1.6.0_24
Provides	: jboss5

%description
JBoss Application Server (or JBoss AS) is a free software/open-source Java EE-based application server. An important distinction for this class of software is that it not only implements a server that runs on Java, but it actually implements the Java EE part of Java. Because it is Java-based, the JBoss application server operates cross-platform: usable on any operating system that supports Java. JBoss AS was developed by JBoss, now a division of Red Hat (http://en.wikipedia.org/wiki/JBoss_application_server)

%pre
if ! id jboss >& /dev/null; then
        adduser jboss -u 1001
fi

%prep
%setup -c -n %{buildroot}/%{_prefix}

%build
# mv %{buildroot}/%{_prefix}/jboss-5.1.0.GA %{buildroot}/%{_prefix}/

%install
%{__install} -D -m 744 %{SOURCE1} %{buildroot}/%{_initrddir}/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%{__install} -d -m 700 %{buildroot}/%{_var}/log/%{name}/

%post
ln -s %{_prefix}/jboss-5.1.0.GA %{_prefix}/%{name}
sed -e "s/^\(JBOSS_HOST=\).*/\1`/sbin/ifconfig eth0 |awk '/inet\ /{ sub(/:/," "); print $3 }'`/" -i %{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf %{buildroot}

%postun
rm -rf %{_prefix}/jboss5
rm -rf %{_var}/log/%{name}

%files 
#####################################################
# defattr sets the default attributes for all files
#####################################################
%attr(770, jboss, jboss) /usr/local/jboss/jboss-5.1.0.GA
# %attr(770, jboss, jboss) /usr/local/jboss/%{name}-%{version}
%attr(700, jboss, jboss) %{_var}/log/%{name}
%attr(-, root, root) %{_initrddir}/%{name}
%config %attr(-, root, root) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Mon Mar 26 2012 Yasser Nabi <ynabi@fsa.gov.uk> 5.1.0GA-4
- Added Provides

* Thu Mar 22 2012 Yasser Nabi <ynabi@fsa.gov.uk> 5.1.0GA-3
- Fixed Log and sysconfig path issue

* Thu Mar 15 2012 Yasser Nabi <ynabi@fsa.gov.uk> 5.1.0GA-2
- Change install path to /usr/local/jboss

* Mon Aug 15 2011 Yasser Nabi <ynabi@fsa.gov.uk> 5.1.0GA-1
- Intial Package of JBoss
