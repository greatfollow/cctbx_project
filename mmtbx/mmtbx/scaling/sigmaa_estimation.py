from __future__ import division
from mmtbx.scaling import absolute_scaling
from mmtbx.scaling import ext
from cctbx.array_family import flex
import scitbx.lbfgs
from scitbx.math import chebyshev_polynome
from scitbx.math import chebyshev_lsq_fit
from libtbx.math_utils import iround
from libtbx.utils import Sorry
import math
import sys, os

class sigmaa_point_estimator(object):
  def __init__(self,
               target_functor,
               h):
    self.functor = target_functor
    self.h = h
    self.f = None
    self.x = flex.double( [-1.0] )
    self.max = 0.99
    self.min = 0.01
    term_parameters = scitbx.lbfgs.termination_parameters(
      max_iterations = 100 )
    # the parametrisation as a sigmoid makes things difficult at the edges
    exception_handling_parameters = scitbx.lbfgs.exception_handling_parameters(
      ignore_line_search_failed_step_at_lower_bound=True,
      ignore_line_search_failed_step_at_upper_bound=True)

    self.minimizer = scitbx.lbfgs.run(target_evaluator=self,
                                      termination_params=term_parameters,
                                      exception_handling_params=exception_handling_parameters)

    self.sigmaa = self.min+(self.max-self.min)/(1.0+math.exp(-self.x[0]))

  def compute_functional_and_gradients(self):
    sigmaa = self.min+(self.max-self.min)/(1.0+math.exp(-self.x[0]))
    # chain rule bit for sigmoidal function
    dsdx = (self.max-self.min)*math.exp(-self.x[0])/(
      (1.0+math.exp(-self.x[0]))**2.0 )
    f = -self.functor.target(self.h,
                             sigmaa)
    g = -self.functor.dtarget(self.h,
                              sigmaa)*dsdx
    self.f = f
    return f, flex.double([g])

def sigmaa_estimator_kernel_width_d_star_cubed(
      r_free_flags,
      kernel_width_free_reflections):
  assert kernel_width_free_reflections > 0
  n_refl = r_free_flags.size()
  n_free = r_free_flags.data().count(True)
  n_refl_per_bin = kernel_width_free_reflections
  if (n_free != 0):
    n_refl_per_bin *= n_refl / n_free
  n_refl_per_bin = min(n_refl, iround(n_refl_per_bin))
  n_bins = max(1, n_refl / max(1, n_refl_per_bin))
  dsc_min, dsc_max = [dss**(3/2) for dss in r_free_flags.min_max_d_star_sq()]
  return (dsc_max - dsc_min) / n_bins

class sigmaa_estimator(object):
  def __init__(self,
               miller_obs,
               miller_calc,
               r_free_flags,
               kernel_width_free_reflections=None,
               kernel_width_d_star_cubed=None,
               kernel_in_bin_centers=False,
               n_sampling_points=20,
               n_chebyshev_terms=10,
               use_sampling_sum_weights=False):
    assert [kernel_width_free_reflections, kernel_width_d_star_cubed].count(None) == 1
    self.miller_obs = miller_obs.map_to_asu()
    self.miller_calc = abs(miller_calc.map_to_asu())
    self.r_free_flags = r_free_flags.map_to_asu()
    self.kernel_width_free_reflections = kernel_width_free_reflections
    self.kernel_width_d_star_cubed = kernel_width_d_star_cubed
    self.n_chebyshev_terms = n_chebyshev_terms

    assert self.r_free_flags.indices().all_eq(
      self.miller_obs.indices() )

    self.miller_calc = self.miller_calc.common_set(
      self.miller_obs )
    assert self.r_free_flags.indices().all_eq(
      self.miller_calc.indices() )

    assert self.miller_obs.is_real_array()

    if self.miller_obs.is_xray_intensity_array():
      self.miller_obs = self.miller_obs.f_sq_as_f()
    assert self.miller_obs.observation_type() is None or \
           self.miller_obs.is_xray_amplitude_array()
    self.miller_calc = self.miller_calc.set_observation_type(
      self.miller_obs)

    # get normalized data please
    self.normalized_obs_f = absolute_scaling.kernel_normalisation(
      self.miller_obs, auto_kernel=True)
    self.normalized_obs =self.normalized_obs_f.normalised_miller_dev_eps.f_sq_as_f()

    self.normalized_calc_f = absolute_scaling.kernel_normalisation(
      self.miller_calc, auto_kernel=True)
    self.normalized_calc =self.normalized_calc_f.normalised_miller_dev_eps.f_sq_as_f()

    # get the 'free data'
    self.free_norm_obs = self.normalized_obs.select( self.r_free_flags.data() )
    self.free_norm_calc= self.normalized_calc.select( self.r_free_flags.data() )

    if self.free_norm_obs.data().size() <= 0:
      raise RuntimeError("No free reflections.")

    if (self.kernel_width_d_star_cubed is None):
      self.kernel_width_d_star_cubed=sigmaa_estimator_kernel_width_d_star_cubed(
        r_free_flags=self.r_free_flags,
        kernel_width_free_reflections=self.kernel_width_free_reflections)

    self.sigma_target_functor = ext.sigmaa_estimator(
      e_obs     = self.free_norm_obs.data(),
      e_calc    = self.free_norm_calc.data(),
      centric   = self.free_norm_obs.centric_flags().data(),
      d_star_cubed = self.free_norm_obs.d_star_cubed().data() ,
      width=self.kernel_width_d_star_cubed)

    d_star_cubed_overall = self.miller_obs.d_star_cubed().data()
    self.min_h = flex.min( d_star_cubed_overall )
    self.max_h = flex.max( d_star_cubed_overall )
    if (kernel_in_bin_centers):
      self.h_array = flex.double( xrange(1,n_sampling_points*2,2) )*(
        self.max_h-self.min_h)/(n_sampling_points*2)+self.min_h
    else:
      self.min_h *= 0.99
      self.max_h *= 1.01
      self.h_array = flex.double( range(n_sampling_points) )*(
        self.max_h-self.min_h)/float(n_sampling_points-1.0)+self.min_h
    assert self.h_array.size() == n_sampling_points
    self.sigmaa_array = flex.double()
    self.sigmaa_array.reserve(self.h_array.size())
    self.sum_weights = flex.double()
    self.sum_weights.reserve(self.h_array.size())

    for h in self.h_array:
      stimator = sigmaa_point_estimator(self.sigma_target_functor, h)
      self.sigmaa_array.append( stimator.sigmaa )
      self.sum_weights.append(
        self.sigma_target_functor.sum_weights(d_star_cubed=h))

    # fit a smooth function
    reparam_sa = -flex.log( 1.0/self.sigmaa_array -1.0 )
    if (use_sampling_sum_weights):
      w_obs = self.sum_weights
      if (0): # XXX
        max_w = flex.max(w_obs)
        if (max_w > 1): w_obs = w_obs / max_w
      w_obs = flex.sqrt(w_obs)
    else:
      w_obs = None
    fit_lsq = chebyshev_lsq_fit.chebyshev_lsq_fit(
      n_terms=self.n_chebyshev_terms,
      x_obs=self.h_array,
      y_obs=reparam_sa,
      w_obs=w_obs)

    cheb_pol = chebyshev_polynome(
        self.n_chebyshev_terms,
        self.min_h,
        self.max_h,
        fit_lsq.coefs)
    self.sigmaa_array = 1.0/(1.0 + flex.exp(-reparam_sa) )
    self.sigmaa = 1.0/(1.0 + flex.exp(-cheb_pol.f(d_star_cubed_overall)) )

    assert flex.min(self.sigmaa) >= 0
    assert flex.max(self.sigmaa) <= 1
    self.alpha = self.sigmaa*flex.sqrt(
      self.normalized_obs_f.normalizer_for_miller_array/
      self.normalized_calc_f.normalizer_for_miller_array)
    self.beta = (1.0-self.sigmaa*self.sigmaa)*\
                self.normalized_obs_f.normalizer_for_miller_array

    # make them into miller arrays
    self.sigmaa = self.miller_obs.array(data=self.sigmaa)
    self.alpha = self.miller_obs.array(data=self.alpha)
    self.beta = self.miller_obs.array(data=self.beta)

    # now only FOM's need to be computed
    tmp_x = self.sigmaa.data()*self.normalized_calc.data()*self.normalized_obs.data()
    tmp_x = tmp_x / (1.0-self.sigmaa.data()*self.sigmaa.data())
    centric_fom = flex.tanh( tmp_x )
    acentric_fom = scitbx.math.bessel_i1_over_i0( 2.0*tmp_x )
    # we need to make sure centric and acentrics are not mixed up ...
    centrics = self.sigmaa.centric_flags().data()
    centric_fom  = centric_fom.set_selected( ~centrics, 0 )
    acentric_fom = acentric_fom.set_selected( centrics, 0 )
    final_fom =  centric_fom + acentric_fom
    self.fom = self.sigmaa.customized_copy(data=final_fom)

  def alpha_beta(self):
    return self.alpha, self.beta

  def show(self, out=None):
    if out is None:
      out = sys.stdout
    print >> out
    print >> out, "SigmaA estimation summary"
    print >> out, "-------------------------"
    print >> out, "Kernel width d* cubed     :  %.6g" % \
      self.kernel_width_d_star_cubed
    print >> out, "Kernel width free refl.   : ", \
      self.kernel_width_free_reflections
    print >> out, "Number of sampling points : ", self.h_array.size()
    print >> out, "Number of Chebyshev terms : ", self.n_chebyshev_terms
    print >> out
    print >> out, "1/d^3      d    sigmaA  sum weights"
    for h,sa,w in zip( self.h_array, self.sigmaa_array, self.sum_weights ):
      d = (1.0/h)**(1/3)
      print >> out, "%5.4f   %5.2f   %4.3f  %.6g"%(h,d,sa,w)
    print >> out
    print >> out
