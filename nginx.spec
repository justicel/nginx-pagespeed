#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx

Summary: nginx is a high performance web server
Name: nginx
Version: 1.4.0
Release: 1%{?dist}.ngx
Vendor: nginx inc.
URL: http://nginx.org/

Source0: http://nginx.org/download/%{name}-%{version}.tar.gz
Source1: logrotate
Source2: nginx.init
Source3: nginx.sysconf
Source4: nginx.conf
Source5: nginx.vh.default.conf
Source6: nginx.vh.example_ssl.conf
Source7: nginx.suse.init
Source8: lua-nginx-module.tar.gz
Source9: nginx-sticky-module-read-only.tar.gz
Source10: nginx_upstream_check_module.tar.gz
Source11: ngx_cache_purge.tar.gz
Source12: ngx_pagespeed.tar.gz

#Patch for nginx_upstream_check_module
#Currently borked with 1.4.0
#Patch0: check_1.2.6+.patch

License: 2-clause BSD-like license
%if 0%{?suse_version}
Group: Productivity/Networking/Web/Servers
%else
Group: System Environment/Daemons
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: lua-devel
BuildRequires: perl
%if 0%{?suse_version}
BuildRequires: libopenssl-devel
Requires(pre): pwdutils
%else
BuildRequires: openssl-devel
Requires: initscripts >= 8.36
Requires(pre): shadow-utils
Requires(post): chkconfig
%endif
Provides: webserver

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server

%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: nginx
%description debug
not stripped version of nginx build with the debugging log support

%prep
%setup -q
%setup -T -D -a 8 -a 9 -a 10 -a 11 -a 12

# %patch0 -p1 

%build
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
	--with-http_spdy_module \
        --add-module=%{_builddir}/nginx-%{version}/lua-nginx-module \
        --add-module=%{_builddir}/nginx-%{version}/nginx-sticky-module-read-only \
        --add-module=%{_builddir}/nginx-%{version}/ngx_cache_purge \
        --add-module=%{_builddir}/nginx-%{version}/ngx_pagespeed \
        --with-ipv6 \
        --with-debug \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/%{name}-%{version}/objs/nginx \
        %{_builddir}/%{name}-%{version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-http_spdy_module \
        --add-module=%{_builddir}/nginx-%{version}/lua-nginx-module \
        --add-module=%{_builddir}/nginx-%{version}/nginx-sticky-module-read-only \
        --add-module=%{_builddir}/nginx-%{version}/ngx_cache_purge \
        --add-module=%{_builddir}/nginx-%{version}/ngx_pagespeed \
        --with-ipv6 \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx

%endif
# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/%{name}-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

#Install docs for nginx cache-purge
mv ngx_cache_purge/CHANGES ngx_cache_purge/CHANGES.ngx_cache_purge
mv ngx_cache_purge/README.md ngx_cache_purge/README.ngx_cache_purge
mv ngx_cache_purge/LICENSE ngx_cache_purge/LICENSE.ngx_cache_purge

#Install docs for nginx lua
mv lua-nginx-module/Changes lua-nginx-module/CHANGES.lua-nginx-module
mv lua-nginx-module/README lua-nginx-module/README.lua-nginx-module

#Install docs for nginx sticky-module
mv nginx-sticky-module-read-only/LICENSE nginx-sticky-module-read-only/LICENSE.nginx-sticky-module-read-only
mv nginx-sticky-module-read-only/README nginx-sticky-module-read-only/README.nginx-stick-module-read-only

#Install docs for nginx upstream_check
#mv nginx_upstream_check_module/CHANGES nginx_upstream_check_module/CHANGES.nginx_upstream_check_module
#mv nginx_upstream_check_module/README nginx_upstream_check_module/README.nginx_upstream_check_module

#Install docs for nginx_pagespeed
mv ngx_pagespeed/LICENSE ngx_pagespeed/LICENSE.ngx_pagespeed
mv ngx_pagespeed/README.md ngx_pagespeed/README.nginx_pagespeed

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE CHANGES README 
%doc ngx_cache_purge/CHANGES.ngx_cache_purge ngx_cache_purge/README.ngx_cache_purge ngx_cache_purge/LICENSE.ngx_cache_purge
%doc lua-nginx-module/CHANGES.lua-nginx-module lua-nginx-module/README.lua-nginx-module
%doc nginx-sticky-module-read-only/LICENSE.nginx-sticky-module-read-only nginx-sticky-module-read-only/README.nginx-stick-module-read-only
#%doc nginx_upstream_check_module/CHANGES.nginx_upstream_check_module nginx_upstream_check_module/README.nginx_upstream_check_module
%doc ngx_pagespeed/LICENSE.ngx_pagespeed ngx_pagespeed/README.nginx_pagespeed

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%{_initrddir}/nginx

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add nginx
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using NGINX!

Check out our community web site:
* http://nginx.org/en/support.html

If you have questions about commercial support for NGINX please visit:
* http://www.nginx.com/support.html

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service nginx upgrade &>/dev/null || :
fi

%changelog
* Wed Apr 24 2013 Sergey Budnevitch <sb@nginx.com>
- gunzip module added
- 1.4.0

* Tue Apr  2 2013 Sergey Budnevitch <sb@nginx.com>
- set permissions on default log files at installation
- 1.2.8

* Tue Feb 12 2013 Sergey Budnevitch <sb@nginx.com>
- excess slash removed from --prefix
- 1.2.7

* Tue Dec 11 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.6

* Tue Nov 13 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.5

* Tue Sep 25 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.4

* Tue Aug  7 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.3
- nginx-debug package now actually contains non stripped binary

* Tue Jul  3 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.2

* Tue Jun  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.1

* Mon Apr 23 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.0

* Thu Apr 12 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.15

* Thu Mar 15 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.14
- OpenSUSE init script and SuSE specific changes to spec file added

* Mon Mar  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.13

* Mon Feb  6 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.12
- banner added to install script

* Thu Dec 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.11
- init script enhancements (thanks to Gena Makhomed)
- one second sleep during upgrade replaced with 0.1 sec usleep

* Tue Nov 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.10

* Tue Nov  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.9
- nginx-debug package added

* Tue Oct 11 2011 Sergey Budnevitch <sb@nginx.com>
- spec file cleanup (thanks to Yury V. Zaytsev)
- log dir permitions fixed
- logrotate creates new logfiles with nginx owner
- "upgrade" argument to init-script added (based on fedora one)

* Sat Oct  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.8
- built with mp4 module

* Fri Sep 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.7

* Tue Aug 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.6
