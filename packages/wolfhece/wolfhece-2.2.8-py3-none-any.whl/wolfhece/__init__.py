from . import _add_path

try:
    from osgeo import gdal, osr
    gdal.UseExceptions()
except ImportError as e:
    print(e)
    raise Exception(_('Error importing GDAL library'))

from .apps.version import WolfVersion

__version__ = WolfVersion().get_version()