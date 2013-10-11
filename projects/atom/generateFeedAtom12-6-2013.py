Package: man-db
Status: install ok half-configured
Multi-Arch: foreign
Priority: important
Section: doc
Installed-Size: 1736
Maintainer: Colin Watson <cjwatson@debian.org>
Architecture: amd64
Version: 2.6.1-2ubuntu1
Config-Version: 2.6.1-2ubuntu1
Replaces: man, manpages-de (<< 0.5-4), nlsutils
Provides: man, man-browser
Depends: groff-base (>= 1.18.1.1-15), bsdmainutils, debconf (>= 1.2.0) | debconf-2.0, dpkg (>= 1.9.0), libc6 (>= 2.14), libgdbm3 (>= 1.8.3), libpipeline1 (>= 1.1.0), zlib1g (>= 1:1.1.4)
Suggests: groff, less, www-browser
Conflicts: man, suidmanager (<< 0.50)
Conffiles:
 /etc/manpath.config 167675fd93075fb5f6ce1aa5f56a8a22
 /etc/cron.weekly/man-db 643340ce3fb3994ef2ae7b88a2cf3230
 /etc/cron.daily/man-db 18745b8d583be7a4b7a00e9ffc98ac99
Description: on-line manual pager
 This package provides the man command, the primary way of examining the
 on-line help files (manual pages). Other utilities provided include the
 whatis and apropos commands for searching the manual page database, the
 manpath utility for determining the manual page search path, and the
 maintenance utilities mandb, catman and zsoelim. man-db uses the groff
 suite of programs to format and display the manual pages.
Homepage: http://man-db.nongnu.org/
