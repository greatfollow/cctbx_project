from __future__ import division
# LIBTBX_SET_DISPATCHER_NAME phenix.development.model_map_statistics

from scitbx.array_family import flex
import sys, math
import iotbx.pdb
from libtbx.utils import Sorry
import mmtbx.utils
import mmtbx.maps.correlation
from cctbx import maptbx
from cctbx import miller
from mmtbx import monomer_library
import mmtbx.monomer_library.server
import mmtbx.monomer_library.pdb_interpretation
from libtbx import adopt_init_args
from mmtbx.rotamer.rotamer_eval import RotamerEval
from libtbx.test_utils import approx_equal
from mmtbx.maps import correlation
from libtbx.str_utils import format_value
from mmtbx.validation.ramalyze import ramalyze
from mmtbx.validation.cbetadev import cbetadev
from libtbx.utils import null_out


legend = """phenix.development.model_map_statistics:
  Given PDB file and a map compute various statistics.

How to run:
  phenix.development.model_map_statistics model.pdb map.ccp4 resolution=3

Feedback:
  PAfonine@lbl.gov"""

master_params_str = """
  map_file_name = None
    .type = str
  model_file_name = None
    .type = str
  resolution = None
    .type = float
  scattering_table = wk1995  it1992  *n_gaussian  neutron electron
    .type = choice
"""

def master_params():
  return iotbx.phil.parse(master_params_str, process_includes=False)

def broadcast(m, log):
  print >> log, "-"*79
  print >> log, m
  print >> log, "*"*len(m)

def run(args, log=sys.stdout):
  print >> log, "-"*79
  print >> log, legend
  print >> log, "-"*79
  inputs = mmtbx.utils.process_command_line_args(args = args,
    master_params = master_params())
  params = inputs.params.extract()
  # model
  broadcast(m="Input PDB:", log=log)
  file_names = inputs.pdb_file_names
  if(len(file_names) != 1): raise Sorry("PDB file has to given.")
  processed_pdb_file = monomer_library.pdb_interpretation.process(
    mon_lib_srv    = monomer_library.server.server(),
    ener_lib       = monomer_library.server.ener_lib(),
    file_name      = file_names[0],
    force_symmetry = True)
  ph = processed_pdb_file.all_chain_proxies.pdb_hierarchy
  xrs = processed_pdb_file.xray_structure()
  xrs.scattering_type_registry(table = params.scattering_table)
  xrs.show_summary(f=log, prefix="  ")
  # restraints
  sctr_keys = xrs.scattering_type_registry().type_count_dict().keys()
  has_hd = "H" in sctr_keys or "D" in sctr_keys
  geometry = processed_pdb_file.geometry_restraints_manager(
    show_energies      = False,
    assume_hydrogens_all_missing = not has_hd,
    plain_pairs_radius = 5.0)
  # map
  broadcast(m="Input map:", log=log)
  if(inputs.ccp4_map is None): raise Sorry("Map file has to given.")
  inputs.ccp4_map.show_summary(prefix="  ")
  map_data = inputs.ccp4_map.map_data()
  # shift origin if needed
  shift_needed = not \
    (map_data.focus_size_1d() > 0 and map_data.nd() == 3 and
     map_data.is_0_based())
  if(shift_needed):
    N = map_data.all()
    O=map_data.origin()
    map_data = map_data.shift_origin()
    # apply same shift to the model
    a,b,c = xrs.crystal_symmetry().unit_cell().parameters()[:3]
    sites_cart = xrs.sites_cart()
    sx,sy,sz = a/N[0]*O[0], b/N[1]*O[1], c/N[2]*O[2]
    sites_cart_shifted = sites_cart-\
      flex.vec3_double(sites_cart.size(), [sx,sy,sz])
    xrs.set_sites_cart(sites_cart_shifted)
  # estimate resolution
  d_min = params.resolution
  broadcast(m="Map resolution:", log=log)
  if(d_min is None):
    d_min = maptbx.resolution_from_map_and_model(
      map_data=map_data, xray_structure=xrs)
  print >> log, "  d_min: %6.4f"%d_min
  # Compute FSC(map, model)
  broadcast(m="Model-map FSC:", log=log)
  mmtbx.maps.correlation.fsc_model_map(
    xray_structure=xrs, map=map_data, d_min=d_min, log=log)
  #
  # various CC
  cc_calculator = mmtbx.maps.correlation.from_map_and_xray_structure_or_fmodel(
    xray_structure = xrs,
    map_data       = map_data,
    d_min          = d_min)
  broadcast(m="Map-model CC:", log=log)
  print >> log, "Overall:"
  # entire box
  print >> log, "         box: %6.4f"%cc_calculator.cc()
  # all atoms
  print >> log, "around atoms: %6.4f"%cc_calculator.cc(
    selection=flex.bool(xrs.scatterers().size(),True))
  # per chain
  print >> log, "Per chain:"
  for chain in ph.chains():
    print >> log, "  chain %s: %6.4f"%(chain.id, cc_calculator.cc(
      selection=chain.atoms().extract_i_seq()))
  # per residue detailed counts
  #
  print >> log, "Per residue:"
  crystal_gridding = maptbx.crystal_gridding(
    unit_cell             = xrs.unit_cell(),
    space_group_info      = xrs.space_group_info(),
    pre_determined_n_real = map_data.accessor().all())
  f_calc = xrs.structure_factors(d_min=d_min).f_calc()
  fft_map = miller.fft_map(
    crystal_gridding     = crystal_gridding,
    fourier_coefficients = f_calc)
  fft_map.apply_sigma_scaling()
  map_model = fft_map.real_map_unpadded()
  #
  sm = structure_monitor(
    pdb_hierarchy  = ph,
    xray_structure = xrs,
    map_1          = map_data,
    map_2          = map_model,
    geometry       = geometry,
    atom_radius    = 2.0)
#  sm.show()

def min_nonbonded_distance(pair_proxy_list_sorted, xray_structure, selection):
  selw = xray_structure.selection_within(radius = 5.0, selection =
    flex.bool(xray_structure.scatterers().size(), selection)).iselection()
  sites_cart = xray_structure.sites_cart()
  dist_min=1.9+9
  i_min,j_min = None,None
  for i in selw:
    for j in selw:
      if(i<j):
        p = [i,j]
        p.sort()
        if(not p in pair_proxy_list_sorted):
          dist_ij = math.sqrt(
            (sites_cart[i][0]-sites_cart[j][0])**2+
            (sites_cart[i][1]-sites_cart[j][1])**2+
            (sites_cart[i][2]-sites_cart[j][2])**2)
          if(dist_ij<dist_min):
            dist_min = dist_ij
            i_min,j_min = i, j
  return i_min,j_min,dist_min

class residue_monitor(object):
  def __init__(self,
               residue,
               id_str,
               bond_rmsd=None,
               angle_rmsd=None,
               map_cc=None,
               map_min=None,
               map_mean=None,
               rotamer_status=None,
               ramachandran_status=None,
               cbeta_status=None,
               min_nonbonded=None):
    adopt_init_args(self, locals())

  def show(self):
    print "%12s %6s %6s %6s %6s %6s %6s %7s %7s %7s"%(
      self.id_str,
      format_value("%6.3f",self.map_cc),
      format_value("%5.2f",self.map_min),
      format_value("%5.2f",self.map_mean),
      format_value("%6.3f",self.bond_rmsd),
      format_value("%6.2f",self.angle_rmsd),
      format_value("%5.2f",self.min_nonbonded),
      self.rotamer_status,
      self.ramachandran_status,
      self.cbeta_status)

class structure_monitor(object):
  def __init__(self,
               pdb_hierarchy,
               xray_structure,
               map_1, # map data
               map_2,
               geometry,
               atom_radius):
    adopt_init_args(self, locals())
    self.unit_cell = self.xray_structure.unit_cell()
    self.xray_structure = xray_structure.deep_copy_scatterers()
    self.unit_cell = self.xray_structure.unit_cell()
    self.rotamer_manager = RotamerEval()
    #
    self.pair_proxy_list_sorted=[]
    bond_proxies_simple = geometry.pair_proxies(
      sites_cart = self.xray_structure.sites_cart()).bond_proxies.simple
    for proxy in bond_proxies_simple:
      tmp = list(proxy.i_seqs)
      tmp.sort()
      self.pair_proxy_list_sorted.append(tmp)
    self.pair_proxy_list_sorted.sort()
    #
    sc1 = self.xray_structure.sites_cart()
    sc2 = self.pdb_hierarchy.atoms().extract_xyz()
    assert approx_equal(sc1, sc2, 1.e-3)
    #
    self.sites_cart = self.xray_structure.sites_cart()
    self.sites_frac = self.xray_structure.sites_frac()
    #
    self.map_cc_whole_unit_cell = None
    self.map_cc_around_atoms = None
    self.map_cc_per_atom = None
    self.rmsd_b = None
    self.rmsd_a = None
    self.dist_from_start = 0
    self.dist_from_previous = 0
    self.number_of_rotamer_outliers = 0
    self.residue_monitors = None
    #
    ramalyze_obj = ramalyze(pdb_hierarchy=pdb_hierarchy, outliers_only=False)
    self.rotamer_outlier_selection = ramalyze_obj.outlier_selection()
    #
    cbetadev_obj = cbetadev(
        pdb_hierarchy = pdb_hierarchy,
        outliers_only = False,
        out           = null_out())
    self.cbeta_outlier_selection = cbetadev_obj.outlier_selection()
    #
    self.initialize()

  def initialize(self):
    # residue monitors
    print "    ID-------|MAP-----------------|RMSD----------|NONB-|ROTAMER|RAMA---|CBETA--|"
    print "             |CC     MIN    MEAN  |BOND    ANGLE |     |       |       |        "
    self.residue_monitors = []
    sites_cart = self.xray_structure.sites_cart()
    for model in self.pdb_hierarchy.models():
      for chain in model.chains():
        for residue_group in chain.residue_groups():
          for conformer in residue_group.conformers():
            for residue in conformer.residues():
              id_str="%s,%s,%s"%(chain.id,residue.resname,residue.resseq.strip())
              selection = residue.atoms().extract_i_seq()
              cc = correlation.from_map_map_atoms(
                map_1      = self.map_1,
                map_2      = self.map_2,
                sites_cart = self.sites_cart.select(selection),
                unit_cell  = self.unit_cell,
                radius     = self.atom_radius)
              rotamer_status = self.rotamer_manager.evaluate_residue(residue)
              grm = self.geometry.select(iselection=selection)
              es = grm.energies_sites(sites_cart=residue.atoms().extract_xyz())
              ramachandran_status="VALID"
              if(selection[0] in self.rotamer_outlier_selection):
                ramachandran_status="OUTLIER"
              cbeta_status="VALID"
              if(selection[0] in self.cbeta_outlier_selection):
                cbeta_status="OUTLIER"
              mnd = min_nonbonded_distance(
                pair_proxy_list_sorted = self.pair_proxy_list_sorted,
                xray_structure         = self.xray_structure,
                selection              = selection)
              mi,me = self.map_values_min_mean(selection = selection)
              rm = residue_monitor(
                residue             = residue,
                id_str              = id_str,
                bond_rmsd           = es.angle_deviations()[2],
                angle_rmsd          = es.bond_deviations()[2],
                map_cc              = cc,
                map_min             = mi,
                map_mean            = me,
                min_nonbonded       = mnd[2],
                rotamer_status      = rotamer_status,
                ramachandran_status = ramachandran_status,
                cbeta_status        = cbeta_status)
              self.residue_monitors.append(rm)
              rm.show()

  def show(self):
    print "     ID       MAP CC    BOND      ANGLE  NONB     ROTAMER    RAMA      CBETA"
    for rm in self.residue_monitors:
      rm.show()

  def map_values_min_mean(self, selection):
    map_values = flex.double()
    for i in selection:
      mv = self.map_1.eight_point_interpolation(self.sites_frac[i])
      map_values.append(mv)
    mi,ma,me = map_values.min_max_mean().as_tuple()
    return mi, me

  def map_map_sites_cc(self, selection):
    return correlation.from_map_map_atoms(
      map_1      = self.map_1,
      map_2      = self.map_2,
      sites_cart = self.sites_cart.select(selection),
      unit_cell  = self.unit_cell,
      radius     = self.atom_radius)


if (__name__ == "__main__"):
  run(args=sys.argv[1:])