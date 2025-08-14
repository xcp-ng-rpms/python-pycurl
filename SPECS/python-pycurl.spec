%global package_speccommit 54550dedc03bed83f2b4bfca0769066b4dce5f8c
%global usver 7.19.0
%global xsver 20
%global xsrel %{xsver}%{?xscount}%{?xshash}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.19.0
Release: %{?xsrel}%{?dist}
Summary:        A Python interface to libcurl

Group:          Development/Languages
License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0: pycurl-7.19.0.tar.gz
Patch0: 0001-No-longer-keep-copies-of-string-options-since-this-i.patch
Patch1: 0002-Fixes-https-sourceforge.net-tracker-func-detail-aid-.patch
Patch2: 0003-Fixes-refcount-bug-and-provides-better-organization-.patch
Patch3: 0004-Test-for-reset-fixes-refcount-bug.patch
Patch4: 0005-Updating-ChangeLog-with-relevant-changes.patch
Patch5: 0101-test_internals.py-add-a-test-for-ref-counting-of-res.patch
Patch6: 0102-pycurl.c-eliminate-duplicated-code-in-util_write_cal.patch
Patch7: 0103-pycurl.c-allow-to-return-1-from-write-callback.patch
Patch8: 0104-test_write_abort.py-test-returning-1-from-write-call.patch
Patch9: 0105-add-the-GLOBAL_ACK_EINTR-constant-to-the-list-of-exp.patch
Patch10: 0201-Keep-a-reference-to-the-object-used-for-CURLOPT_POST.patch
Patch11: 0202-Add-libcurl-7.34.0-sslversion-options.patch

Requires:       keyutils-libs
BuildRequires:  python-devel
BuildRequires:  openssl-devel

# curl-7.29.0-16 or newer is needed for CURL_SSLVERSION_TLSv1_[0-2]
BuildRequires:  libcurl-devel >= 7.29.0-16

%define __python /usr/bin/python2

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
Requires:       libcurl >= %{libcurl_ver}

Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%autosetup -p1 -n pycurl-%{version}
chmod a-x examples/*

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" %{__python} setup.py build

%check
export PYTHONPATH=$RPM_BUILD_ROOT%{python_sitearch}
make test PYTHON=%{__python}

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%files
%doc COPYING COPYING2 ChangeLog README TODO examples doc tests
%{python_sitearch}/*

%changelog
* Thu May 23 2024 Lin Liu <Lin.Liu01@cloud.com> - 7.19.0-20
- First imported release

