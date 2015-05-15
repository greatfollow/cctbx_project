from __future__ import division

from libtbx import adopt_init_args
from scitbx.array_family import flex


# catch-all class for handling any higher-level restraints (such as
# Ramachandran, rotamer, H-bonds, etc.)

class manager (object) :
  def __init__ (self,
                reference_manager=None,
                den_manager=None,
                flags=None) :
    adopt_init_args(self, locals())
    if self.flags is None:
      import mmtbx.geometry_restraints.flags
      self.flags = mmtbx.geometry_restraints.flags.flags(default=True)
    if (self.reference_manager is None) :
      from mmtbx.geometry_restraints import reference
      self.reference_manager = reference.manager()

  def get_n_proxies(self):
    return self.get_n_reference_coordinate_proxies() + \
           self.get_n_reference_torsion_proxies() +\
           self.get_n_den_proxies()

  def get_n_reference_coordinate_proxies(self):
    if self.reference_manager is not None:
      if self.reference_manager.reference_coordinate_proxies is not None:
        return len(self.reference_manager.reference_coordinate_proxies)
    return 0

  def get_n_reference_torsion_proxies(self):
    if self.reference_manager is not None:
      if self.reference_manager.reference_torsion_proxies is not None:
        return len(self.reference_manager.reference_torsion_proxies)
    return 0

  def get_n_den_proxies(self):
    if self.den_manager is not None:
      return len(self.den_manager.den_proxies)
    return 0

  def restraints_residual_sum (self,
                               sites_cart,
                               gradient_array=None) :
    if (gradient_array is None) :
      from scitbx.array_family import flex
      gradient_array = flex.vec3_double(sites_cart.size(), (0.0,0.0,0.0))
    target = 0
    if (self.reference_manager is not None and
        self.flags.reference) :
      if (self.reference_manager.reference_coordinate_proxies is not None or
          self.reference_manager.reference_torsion_proxies is not None):
        target += self.reference_manager.target_and_gradients(
          sites_cart=sites_cart,
          gradient_array=gradient_array)
    if (self.den_manager is not None and
        self.flags.den) :
      #print "DEN target is in geneneric manager"
      den_target = self.den_manager.target_and_gradients(
        sites_cart=sites_cart,
        gradient_array=gradient_array)
      #print "DEN target: %.1f" % den_target
      target += den_target
    return target

  def rotamers (self) :
    return None #self.rotamer_manager

  def select (self,
              n_seq,
              iselection) :
    den_manager = None
    if (self.den_manager is not None) :
      den_manager = self.den_manager.select(n_seq, iselection)
    return manager(
      den_manager=den_manager,
      flags=self.flags)
