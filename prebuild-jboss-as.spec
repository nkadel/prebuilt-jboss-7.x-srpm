# Stop trying to replack the jar files
%global __jar_repack 0

Name:		prebuilt-jboss-as
Version:	7.1.1
Release:	0.1%{?dist}
Summary:	JBoss AS, pre-built

Group:		Sysetem Environment/Daemons
License:	GPLv2+
URL:		http://www.jboss.org/jbossas
Source0:	jboss-as-%{version}.Final.tar.gz
Source10:	README.redhat

#BuildRequires:	
Requires:	chkconfig
Requires:	shadow-utils
Requires:	java >= 0:1.6.0
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig

Provides: jboss-as = %{version}-%{release}
# Tarball includes multiple platforms, breaks noarch RPM building
#BuildArch: noarch

%description
JBoss Application Server, deployed from downloaded binary tarball

%prep

%setup -q -n jboss-as-%{version}.Final
# This is a pre-built tarball of jar files, do not configure or build

%{__install} %SOURCE10 README.redhat

%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/%{_datarootdir}/jboss-as
%{__cp} -a . $RPM_BUILD_ROOT/%{_datarootdir}/jboss-as/.

# Leave this added file out of the deployed content, use as doc only.
%{__rm} -f $RPM_BUILD_ROOT/README.redhat

%{__mkdir} -p $RPM_BUILD_ROOT/%{_initddir}
%{__install} -m 755 bin/init.d/jboss-as-standalone.sh $RPM_BUILD_ROOT/%{_initddir}/jboss-as


%{__mkdir} -p $RPM_BUILD_ROOT/etc/sysconfig
%{__install} -m 644 bin/init.d/jboss-as.conf $RPM_BUILD_ROOT//etc/sysconfig

# Default target directories, owned by jboss-as user
%{__mkdir} -p $RPM_BUILD_ROOT/var/run/jboss-as
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/jboss-as

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "jboss-as" user
getent group jboss-as >/dev/null || groupadd -g 440 -r jboss-as
getent passwd jboss-as >/dev/null || \
  useradd -r -u 448 -g jboss-as -s /sbin/nologin \
    -d %{_datarootdir}/jboss-as -c "Jboss Advanced Server" jboss-as
exit 0

%post
# Register the jboss-as service
/sbin/chkconfig --add jboss-as

%preun
if [ $1 = 0 ]; then
   /sbin/service jboss-as stop > /dev/null 2>&1
   /sbin/chkconfig --del jboss-as
fi

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt README.redhat
%doc docs/examples
%config(noreplace) /etc/sysconfig/jboss-as.conf
%{_initddir}/jboss-as
%attr(-,jboss-as,jboss-as) %{_datarootdir}/jboss-as
%attr(755,jboss-as,jboss-as) %dir /var/run/jboss-as
%attr(755,jboss-as,jboss-as) %dir /var/log/jboss-as

%changelog
* Thu Sep 19 2013 Nico Kadel-Garcia <nkadel@gmail.com> - 7.1.1-0.1
- Create inital RPM from binary jboss-as-7.1. tarball

