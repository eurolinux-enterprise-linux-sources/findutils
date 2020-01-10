Summary: The GNU versions of find utilities (find and xargs)
Name: findutils
Version: 4.5.11
Release: 3%{?dist}
Epoch: 1
License: GPLv3+
Group: Applications/File
URL: http://www.gnu.org/software/findutils/
Source0: ftp://alpha.gnu.org/gnu/findutils/%{name}-%{version}.tar.gz

# do not build locate
Patch1: findutils-4.4.0-no-locate.patch

# learn find to recognize autofs file system by reading /proc/mounts
# as autofs mount points are not listed in /etc/mtab
Patch2: findutils-4.4.2-autofs.patch

# add a new option -xautofs to find to not descend into directories on autofs
# file systems
Patch3: findutils-4.4.2-xautofs.patch

# eliminate compile-time warnings
Patch4: findutils-4.5.7-warnings.patch

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Conflicts: filesystem < 3
Provides: /bin/find
Provides: bundled(gnulib)

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake
BuildRequires: dejagnu
BuildRequires: gettext-devel
BuildRequires: libselinux-devel
BuildRequires: texinfo

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a file name pattern).  The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).

You should install findutils because it includes tools that are very
useful for finding things on your system.

%prep
%setup -q
rm -rf locate
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# needed because of findutils-4.4.0-no-locate.patch
autoreconf -iv

%build
%configure

# uncomment to turn off optimizations
#find -name Makefile | xargs sed -i 's/-O2/-O0/'

make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}

%post
if [ -f %{_infodir}/find.info.gz ]; then
  /sbin/install-info %{_infodir}/find.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/find.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/find.info.gz %{_infodir}/dir || :
  fi
fi

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog
%{_bindir}/find
%{_bindir}/oldfind
%{_bindir}/xargs
%{_mandir}/man1/find.1*
%{_mandir}/man1/oldfind.1*
%{_mandir}/man1/xargs.1*
%{_infodir}/find.info*
%{_infodir}/find-maint.info.gz

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:4.5.11-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:4.5.11-2
- Mass rebuild 2013-12-27

* Sun Feb 03 2013 Kamil Dudka <kdudka@redhat.com> - 1:4.5.11-1
- new upstream release

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 1:4.5.10-7
- fix specfile issues reported by the fedora-review script
- do not use the AM_C_PROTOTYPES macro (removed in Automake 1.12)
- do not require gets() to be declared

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Kamil Dudka <kdudka@redhat.com> - 1:4.5.10-5
- add virtual provides for bundled(gnulib) copylib (#821753)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 1:4.5.10-4
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 1:4.5.10-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 11 2011 Kamil Dudka <kdudka@redhat.com> - 1:4.5.10-1
- new upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 24 2010 Kamil Dudka <kdudka@redhat.com> - 1:4.5.9-2
- fix some bugs in handling of -execdir (Savannah bug #29949)

* Wed May 05 2010 Kamil Dudka <kdudka@redhat.com> - 1:4.5.9-1
- new upstream release, dropped applied patches

* Tue Apr 06 2010 Kamil Dudka <kdudka@redhat.com> - 1:4.5.7-4
- avoid assertion failure due to access permissions (#579476)

* Sun Apr 04 2010 Kamil Dudka <kdudka@redhat.com> - 1:4.5.7-3
- upstream bugfix http://savannah.gnu.org/bugs/?29435

* Sat Apr 03 2010 Kamil Dudka <kdudka@redhat.com> - 1:4.5.7-2
- avoid assertion failure on non-recognized O_CLOEXEC

* Sat Apr 03 2010 Kamil Dudka <kdudka@redhat.com> - 1:4.5.7-1
- new upstream release, dropped applied patches
- eliminated compile-time warnings

* Thu Nov 26 2009 Kamil Dudka <kdudka@redhat.com> - 1:4.4.2-6
- update SELinux patch to the latest upstream (gnulib based) version

* Wed Nov 18 2009 Kamil Dudka <kdudka@redhat.com> - 1:4.4.2-5
- do not fail silently on a remount during traverse (#538536)

* Tue Oct 20 2009 Kamil Dudka <kdudka@redhat.com> - 1:4.4.2-4
- make it possible to recognize an autofs filesystem by find
- add a new find's option -xautofs to not descend directories on autofs
  filesystems

* Mon Sep 14 2009 Kamil Dudka <kdudka@redhat.com> - 1:4.4.2-3
- do process install-info only without --excludedocs(#515914)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  1 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.4.2-1
- Update to findutils-4.4.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 30 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.4.0-1
- Update to findutils-4.4.0
  Resolves: #437733

* Mon Apr 14 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.33-3
- Move find to /bin
  Resolves: #438183

* Fri Mar 28 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.33-2
- Fix xargs ARG_MAX assert
  Resolves: #439168

* Fri Feb 15 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.33-1
- Update to findutils-4.2.33
- Fix License

* Wed Feb 13 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.32-1
- Update to findutils-4.2.32

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.31-4
- Rebuild

* Fri Jan 18 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.31-3
- Rebuild

* Thu Aug 23 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.31-2
- fix license
- rebuild

* Tue Jun 12 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1:4.2.31-1
- Update to findutils-4.2.31
  Resolves: #243732

* Fri Jan  5 2007 Miloslav Trmac <mitr@redhat.com> - 1:4.2.29-2
- Ignore install-info errors in scriptlets

* Sun Nov 26 2006 Miloslav Trmac <mitr@redhat.com> - 1:4.2.29-1
- Update to findutils-4.2.29
- Fix some rpmlint warnings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:4.2.27-4.1
- rebuild

* Sun Feb 19 2006 Miloslav Trmac <mitr@redhat.com> - 1:4.2.27-4
- Report the correct directory when hard link count is inconsistent (#182001)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:4.2.27-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:4.2.27-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Miloslav Trmac <mitr@redhat.com> - 1:4.2.27-3
- Updated SELinux patch, --context is no longer valid (use -context)

* Thu Jan 12 2006 Miloslav Trmac <mitr@redhat.com> - 1:4.2.27-2
- Don't use uninitialized memory in -printf %%Z (#174485)
- Ship more documentation files
- Clean up the spec file a bit

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.27-1
- 4.2.27.
- No longer need arg_max patch.

* Mon Nov 21 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.26-1
- One further arg_max fix for PPC.
- Applied arg_max patch from upstream to fix test suite failures.
- 4.2.26 (fixes bug #173817).

* Tue Oct 11 2005 Dan Walsh <dwalsh@redhat.com> 1:4.2.25-3
- Fix selinux patch

* Mon Sep  5 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.25-2
- 4.2.25.

* Mon Jun 20 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.23-1
- 4.2.23.

* Thu Mar 17 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.20-1
- 4.2.20.

* Mon Mar 14 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.18-3
- Applied patch from Robert Scheck to fix compilation with GCC 4 (bug #151031).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.18-2
- Rebuild for new GCC.

* Mon Feb 21 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.18-1
- 4.2.18.

* Mon Feb 14 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.15-2
- Added nofollow patch from upstream.

* Mon Jan 31 2005 Tim Waugh <twaugh@redhat.com> 1:4.2.15-1
- 4.2.15.  Lots of patches removed due to upstream merge.

* Tue Jan 4 2005 Dan Walsh <dwalsh@redhat.com> 1:4.1.20-8
- Change --context to use fnmatch instead of strcmp

* Tue Dec  7 2004 Tim Waugh <twaugh@redhat.com>
- Removed "G" and "M" size qualifiers from man page, since support for
  those is not in the stable branch (bug #141987).

* Tue Oct 19 2004 Tim Waugh <twaugh@redhat.com> 1:4.1.20-7
- Better xargs ARG_SIZE handling (bug #135129).

* Fri Oct 15 2004 Tim Waugh <twaugh@redhat.com>
- Fixed d_type patch for underquoted m4 macro.

* Fri Oct  8 2004 Tim Waugh <twaugh@redhat.com>
- Use upstream patch for find -size man page fix.

* Wed Oct  6 2004 Tim Waugh <twaugh@redhat.com> 1:4.1.20-6
- Fixed bug #126352.

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 1:4.1.20-5
- Build requires gettext-devel, texinfo (bug #134692).

* Thu Sep 30 2004 Tim Waugh <twaugh@redhat.com> 1:4.1.20-4
- Set re->translate before re_compile_pattern (bug #134190).

* Sun Aug  1 2004 Alan Cox <alan@redhat.com> 1:4.1.20-3
- Fix build with current auto* tools (Steve Grubb)

* Tue Jul  6 2004 Tim Waugh <twaugh@redhat.com> 1:4.1.20-2
- Fix -iregex (bug #127297).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com> 1:4.1.20-1
- Clarify find man page (bug #126098).
- Apply changes by Robert Scheck <redhat@linuxnetz.de> (bug #126352):
  - Upgrade to 4.1.20 and some specfile cleanup

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Tim Waugh <twaugh@redhat.com> 4.1.7-26
- Fixed build requirements (bug #123746).

* Sun Mar 14 2004 Tim Waugh <twaugh@redhat.com> 4.1.7-25
- Apply Jakub Jelinek's patch for xargs -E/-I/-L options.

* Thu Mar 11 2004 Tim Waugh <twaugh@redhat.com> 4.1.7-24
- Apply selinux patch last so that it can be turned off (bug #118025).

* Tue Mar  9 2004 Tim Waugh <twaugh@redhat.com>
- Jakub Jelinek's d_type patch improvement.

* Sun Mar  7 2004 Tim Waugh <twaugh@redhat.com> 4.1.7-23
- Run 'make check'.
- Apply Ulrich Drepper's improvement on the d_type patch.

* Fri Mar  5 2004 Tim Waugh <twaugh@redhat.com> 4.1.7-22
- Apply Jakub Jelinek's d_type patch for improved efficiency with
  many common expressions.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 4.1.7-20
- fix call to is_selinux_enabled

* Thu Oct 30 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-19
- Turn off SELinux

* Thu Oct 30 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-18.sel
- Turn on selinux

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 4.1.7-17
- Rebuilt.

* Fri Oct 10 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-16
- Turn off selinux

* Fri Oct 10 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-15.sel
- Turn on selinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-15
- Turn off selinux

* Thu Aug 28 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-14.sel
- Turn on selinux

* Fri Jul 18 2003 Dan Walsh <dwalsh@redhat.com> 4.1.7-13
- Add SELinux patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 23 2003 Elliot Lee <sopwith@redhat.com> 4.1.7-11
- Remove config.{sub,guess} to make ppc64 work

* Mon Mar 17 2003 Tim Waugh <twaugh@redhat.com> 4.1.7-10
- Make 'xargs -i -n1' behave as expected (bug #86191).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.1.7-9
- rebuilt

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 4.1.7-8
- Ship translations.
- Don't install files not packaged.

* Wed Jul  3 2002 Tim Waugh <twaugh@redhat.com> 4.1.7-7
- Fix usage message (bug #67828).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 4.1.7-6
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 4.1.7-5
- automated rebuild

* Tue Feb 26 2002 Tim Waugh <twaugh@redhat.co,> 4.1.7-4
- Rebuild in new environment.

* Tue Feb 12 2002 Tim Waugh <twaugh@redhat.com> 4.1.7-3
- s/Copyright/License/.
- Fix documentation (bug #53857).

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.7, no additional patch needed anymore

* Thu Feb  8 2001 Preston Brown <pbrown@redhat.com>
- remove extraneous linking to librt/libpthreads.

* Tue Oct 17 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.6

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 28 2000 Preston Brown <pbrown@redhat.com>
- revert to 4.1.5 ( :) ) on the advice of HJ Lu
- patch to fix finding w/ -perm flag

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- revert to 4.1.4
- reapply numblks patch
- generate new nolocate patch, we don't ship it.

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- 4.1.5, FHS paths
- remove mktemp,getshort patches (don't ship locate)
- alpha, numblks patch no longer needed

* Mon Apr  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.1.4
- remove some obsolete patches, adapt others
- fix build on alpha

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix summary
- ma  pages are compressed

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- new description.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- fixed block count bug (# 2141)

* Mon Mar 29 1999 Preston Brown <pbrown@redhat.com>
- patch to fix xargs out of bounds overflow (bug # 1279)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 30)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- remove further updatedb remnants (#1072).

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- added patch for glibc21

* Mon Nov 16 1998 Erik Troan <ewt@redhat.com>
- removed locate stuff (as we now ship slocate)

* Wed Jun 10 1998 Erik Troan <ewt@redhat.com>
- updated updatedb cron script to not look for $TMPNAME.n (which was
  a relic anyway)
- added -b parameters to all of the patches

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Mar 09 1998 Michael K. Johnson <johnsonm@redhat.com>
- make updatedb.cron use mktemp correctly
- make updatedb use mktemp

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- nobody should own tmpfile
- ignore /net

* Wed Nov 05 1997 Michael K. Johnson <johnsonm@redhat.com>
- made updatedb.cron do a better job of cleaning up after itself.

* Tue Oct 28 1997 Donald Barnes <djb@redhat.com>
- fixed 64 bit-ism in getline.c, patch tacked on to end of glibc one

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- added patch for glibc 2.1

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot support

* Tue Oct 14 1997 Michael K. Johnson <johnsonm@redhat.com>
- made updatedb.cron work even if "nobody" can't read /root
- use mktemp in updatedb.cron

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added missing info pages
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built with glibc

* Mon Apr 21 1997 Michael K. Johnson <johnsonm@redhat.com>
- fixed updatedb.cron
