
"""
Listing of current dependencies for CCTBX and related applications (including
LABELIT, xia2, DIALS, and Phenix with GUI).  Not all of these can be downloaded
via the web (yet).
"""

from __future__ import division
from bootstrap import Toolbox
from installer_utils import *
import os.path as op
import os
import sys

BASE_CCI_PKG_URL = "http://cci.lbl.gov/cctbx_dependencies"
BASE_XIA_PKG_URL = "http://www.ccp4.ac.uk/xia"
BASE_HDF5_PKG_URL = "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.15-patch1/src"
BASE_PIPY_PKG_URL = "https://pypi.python.org/packages/source"

def pypi_pkg_url(package):
  '''Translate a package filename into a PyPi URL prefix'''
  return "%s/%s/%s" % (BASE_PIPY_PKG_URL,
         package[0],
         package[:package.rindex('-')] if '-' in package else package)

# OpenSSL - needed for Mac OS X 10.11
BASE_OPENSSL_PKG_URL = "https://www.openssl.org/source/"
OPENSSL_PKG = "openssl-1.0.2h.tar.gz"

# from CCI
PYTHON_PKG = "Python-2.7.8_cci.tar.gz"
NUMPY_PKG = "numpy-1.8.1.tar.gz"         # used many places
IMAGING_PKG = "Imaging-1.1.7.tar.gz"     # for labelit, gltbx
REPORTLAB_PKG = "reportlab-2.6.tar.gz"   # for labelit
ZLIB_PKG = "zlib-1.2.7.tar.gz"
SCIPY_PKG = "scipy-0.14.0.tar.gz"        # not used by default
PYRTF_PKG = "PyRTF-0.45.tar.gz"          # for phenix.table_one, etc.
BIOPYTHON_PKG = "biopython-1.64.tar.gz"  # used in iotbx
SPHINX_PKG = "Sphinx-1.2.2.tar.gz"       # for documentation
NUMPYDOC_PKG = "numpydoc-0.5.tar.gz"     # for documentation
IPYTHON_PKG = "ipython-2.1.0.tar.gz"     # IPython
DOCUTILS_PKG = "docutils-0.12.tar.gz"    # docutils
SETUPTOOLS_PKG = "setuptools-12.0.5.tar.gz" # setuptools
PIP_PKG = "pip-6.0.7.tar.gz"             # PIP
VIRTUALENV_PKG = "virtualenv-12.0.6.tar.gz" # virtualenv
LIBSVM_PKG = "libsvm-3.17_cci.tar.gz"

# from PyPi
JUNIT_XML_PKG = "junit-xml-1.6.tar.gz"
MOCK_PKG = "mock-1.0.1.tar.gz"
PYTEST_PKG = "pytest-2.9.1.tar.gz"
PYTEST_DEP_PY = "py-1.4.31.tar.gz"
PYTEST_DEP_COLORAMA = "colorama-0.3.7.tar.gz"

## from xia2 page
#HDF5_PKG = "hdf5-1.8.8.tar.bz2"      # dxtbx
#H5PY_PKG = "h5py-2.0.1-edit.tar.gz"  # dxtbx

H5PY_PKG = "h5py-2.4.0.tar.gz" # dxtbx
HDF5_PKG = "hdf5-1.8.15-patch1.tar.bz2"
CYTHON_PKG = "cython-0.22.tar.gz"

# GUI dependencies
LIBPNG_PKG = "libpng-1.2.52.tar.gz"
FREETYPE_PKG = "freetype-2.4.2.tar.gz"
# Linux-only
# FIXME some of these are getting pretty ancient, time to update?
GETTEXT_PKG = "gettext-0.18.2.tar.gz"
GLIB_PKG = "glib-2.12.11.tar.gz"
EXPAT_PKG = "expat-1.95.8.tar.gz"
FONTCONFIG_PKG = "fontconfig-2.3.95.tar.gz"
RENDER_PKG = "render-0.8.tar.gz"
XRENDER_PKG = "xrender-0.8.3.tar.gz"
XFT_PKG = "xft-2.1.2.tar.gz"
PIXMAN_PKG = "pixman-0.19.2.tar.gz"
CAIRO_PKG = "cairo-1.8.10.tar.gz"
PANGO_PKG = "pango-1.16.1.tar.gz"
ATK_PKG = "atk-1.9.1.tar.gz"
TIFF_PKG = "tiff-v3.6.1.tar.gz"
GTK_PKG = "gtk+-2.10.11.tar.gz"
GTK_ENGINE_PKG = "clearlooks-0.5.tar.gz"
GTK_THEME_PKG = "gtk_themes.tar.gz"
# end Linux-only
FONT_PKG = "fonts.tar.gz"
# FIXME at some point we should switch to using 3.x for all platforms
#WXPYTHON_DEV_PKG = "wxPython-src-3.0.1.0.tar.gz"  # Mac
#WXPYTHON_PKG = "wxPython-src-2.8.12.1.tar.gz"      # Linux
WXPYTHON_DEV_PKG = "wxPython-src-3.0.2.0.tar.bz2"  # all versions
WXPYTHON_PKB = "wxPython-src-3.0.2.0.tar.bz2"
MATPLOTLIB_PKG = "matplotlib-1.3.1.tar.gz"
PY2APP_PKG = "py2app-0.7.3.tar.gz"                    # Mac only
PYOPENGL_PKG = "PyOpenGL-3.1.0.tar.gz"
# https://pypi.python.org/pypi/Send2Trash
SEND2TRASH_PKG = "Send2Trash-1.3.0.tar.gz"

# Windows precompiled compiled base packages
WIN64PYTHON_PKG = "python2.7.9_x86_64_plus_relocatable.zip"
WIN32PYTHON_PKG = "python2.7.9_x86_32_plus_relocatable.zip"
WIN64HDF5_PKG = "HDF5-1.8.16-win64.zip"
WIN32HDF5_PKG = "HDF5-1.8.16-win32.zip"

# Various dependencies from external repositories, distributed as static
# tarballs (since they are not under active development by us or our
# collaborators)
dependency_tarballs = {
  "boost":  ("http://cci.lbl.gov/hot", "boost_hot.tar.gz"),
  "scons":  ("http://cci.lbl.gov/hot", "scons_hot.tar.gz"),
  "annlib": ("http://cci.lbl.gov/hot", "annlib_hot.tar.gz"),
}
# External SVN repositories that may be required for certain components of
# CCTBX to work.  This includes forked versions (with minimal changes) of the
# core CCP4 libraries, MUSCLE, and ksDSSP, but also the development branch
# of CBFLIB.
subversion_repositories = {
  "cbflib":"http://svn.code.sf.net/p/cbflib/code-0/trunk/CBFlib_bleeding_edge",
  "ccp4io": "http://cci.lbl.gov/svn/ccp4io/trunk",
  "ccp4io_adaptbx": "http://cci.lbl.gov/svn/ccp4io_adaptbx/trunk",
  "annlib_adaptbx": "http://cci.lbl.gov/svn/annlib_adaptbx/trunk",
  "gui_resources": "http://cci.lbl.gov/svn/gui_resources/trunk",
  "tntbx": "http://cci.lbl.gov/svn/tntbx/trunk",
  "ksdssp": "http://cci.lbl.gov/svn/ksdssp/trunk",
  "muscle": "http://cci.lbl.gov/svn/muscle/trunk",
  # adding for amber
  "amber_adaptbx": "http://cci.lbl.gov/svn/amber_adaptbx/trunk",
}

# External GIT repositories that may be required for certain components of
# CCTBX to work. Note that the format for git repositories can be more
# sophisticated than that for SVN, and can include multiple possible sources,
# including .zip archives to fall back on when git is not available, and git
# command line parameters
git_repositories = {
  # lz4 and bitshuffle compressions for HDF5
  "hdf5_lz4": ['git@github.com:dectris/HDF5Plugin.git',
               'https://github.com/dectris/HDF5Plugin.git',
               'https://github.com/dectris/HDF5Plugin/archive/master.zip'],
  "bitshuffle": ['git@github.com:kiyo-masui/bitshuffle.git',
                 'https://github.com/kiyo-masui/bitshuffle.git',
                 'https://github.com/kiyo-masui/bitshuffle/archive/master.zip'],
}

class fetch_packages (object) :
  """
  Download manager for the packages defined by this module - this is used by
  install_base_packages.py but also for setting up installer bundles.
  """
  def __init__ (self, dest_dir, log, pkg_dirs=None, no_download=False,
      copy_files=False) :
    self.dest_dir = dest_dir
    self.log = log
    self.pkg_dirs = pkg_dirs
    self.no_download = no_download
    self.copy_files = copy_files
    self.toolbox = Toolbox()

  def __call__ (self,
                pkg_name,
                pkg_url=None,
                output_file=None,
                return_file_and_status=False,
                ) :
    if (pkg_url is None) :
      pkg_url = BASE_CCI_PKG_URL
    if (output_file is None) :
      output_file = pkg_name
    os.chdir(self.dest_dir)
    print >> self.log, "  getting package %s..." % pkg_name
    if (self.pkg_dirs is not None) and (len(self.pkg_dirs) > 0) :
      for pkg_dir in self.pkg_dirs :
        static_file = op.join(pkg_dir, pkg_name)
        if (op.exists(static_file)) :
          print >> self.log, "    using %s" % static_file
          if self.copy_files :
            copy_file(static_file, op.join(self.dest_dir, output_file))
            if return_file_and_status:
              return op.join(self.dest_dir, output_file), 0
            return op.join(self.dest_dir, output_file)
          else :
            if return_file_and_status:
              return static_file, 0
            return static_file
    if (self.no_download) :
      if (op.exists(pkg_name)) :
        print >> self.log, "    using ./%s" % pkg_name
        if return_file_and_status:
          return op.join(self.dest_dir, output_file), 0
        return op.join(self.dest_dir, pkg_name)
      else :
        raise RuntimeError(("Package '%s' not found on local filesystems.  ") %
          pkg_name)
    full_url = "%s/%s" % (pkg_url, pkg_name)
    self.log.write("    downloading from %s : " % pkg_url)

    size = self.toolbox.download_to_file(full_url, output_file, log=self.log)
    if (size == -2):
      print >> self.log, "    using ./%s (cached)" % pkg_name
      if return_file_and_status:
        return op.join(self.dest_dir, output_file), size
      return op.join(self.dest_dir, output_file)
    assert (size > 0), pkg_name
    if return_file_and_status:
      return op.join(self.dest_dir, output_file), size
    return op.join(self.dest_dir, output_file)

def fetch_all_dependencies (dest_dir,
    log,
    pkg_dirs=None,
    copy_files=True,
    gui_packages=True,
    dials_packages=True) :
  """
  Download or copy all dependencies into a local directory (prepping for
  source installer bundling).
  """
  fetch_package = fetch_packages(
    dest_dir=dest_dir,
    log=log,
    pkg_dirs=pkg_dirs,
    copy_files=copy_files)
  for pkg_name in [
      PYTHON_PKG, NUMPY_PKG, IMAGING_PKG, REPORTLAB_PKG, ZLIB_PKG,
      SCIPY_PKG, PYRTF_PKG, BIOPYTHON_PKG, SPHINX_PKG, NUMPYDOC_PKG,
      IPYTHON_PKG,
    ] :
    fetch_package(pkg_name)
  if (gui_packages) :
    for pkg_name in [
        LIBPNG_PKG, FREETYPE_PKG, GETTEXT_PKG, GLIB_PKG, EXPAT_PKG,
        FONTCONFIG_PKG, RENDER_PKG, XRENDER_PKG, XFT_PKG, PIXMAN_PKG,
        CAIRO_PKG, PANGO_PKG, ATK_PKG, TIFF_PKG, GTK_PKG,
        GTK_ENGINE_PKG, GTK_THEME_PKG, FONT_PKG, WXPYTHON_DEV_PKG, WXPYTHON_PKG,
        MATPLOTLIB_PKG, PY2APP_PKG, SEND2TRASH_PKG,
      ] :
      fetch_package(pkg_name)
  if (dials_packages) :
    for pkg_name in [ HDF5_PKG, H5PY_PKG, PYOPENGL_PKG ] :
      fetch_package(pkg_name, BASE_XIA_PKG_URL)

def fetch_svn_repository (pkg_name, pkg_url=None, working_copy=True,
    delete_if_present=False) :
  """
  Download an SVN repository, with or without metadata required for ongoing
  development.
  """
  ## TODO: Merge this with _add_svn in bootstrap.py.
  #        Unnecessary code duplication
  if op.exists(pkg_name) :
    if delete_if_present :
      shutil.rmtree(pkg_name)
    else :
      raise OSError("Directory '%s' already exists.")
  if (pkg_url is None) :
    pkg_url = optional_repositories[pkg_name]
  if working_copy :
    call("svn co --non-interactive --trust-server-cert %s %s" % (pkg_url, pkg_name), sys.stdout)
  else :
    call("svn export --non-interactive --trust-server-cert %s %s" % (pkg_url, pkg_name), sys.stdout)
  assert op.isdir(pkg_name)

def fetch_git_repository(package, use_ssh):
  """ Download a git repository """
  Toolbox.git(package, git_repositories[package], destination=os.path.join(os.getcwd(), package), use_ssh=use_ssh, verbose=True)
  assert op.isdir(package)

def fetch_remote_package (module_name, log=sys.stdout, working_copy=False, use_ssh=False) :
  if (module_name in git_repositories):
    fetch_git_repository(module_name, use_ssh)
  elif (module_name in dependency_tarballs) :
    if op.isdir(module_name) :
      shutil.rmtree(module_name)
    pkg_url, pkg_name = dependency_tarballs[module_name]
    tarfile = module_name + ".tar.gz"
    fetch_packages(
      dest_dir=os.getcwd(),
      log=log).__call__(
        pkg_name=pkg_name,
        pkg_url=pkg_url,
        output_file=tarfile)
    untar(tarfile, log)
    os.remove(tarfile)
  elif (module_name in subversion_repositories) :
    if op.isdir(module_name) :
      shutil.rmtree(module_name)
    pkg_url = subversion_repositories[module_name]
    fetch_svn_repository(
      pkg_name=module_name,
      pkg_url=pkg_url,
      working_copy=working_copy)
