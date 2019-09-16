from jinja2 import Environment, FileSystemLoader
import os, stat
from tools.coupling_schemes import CouplingScheme
from problem_setup import get_manufactured_solution
from tools.postproc_errors import create_error_table
from tools.postproc import create_qn_table
import argparse
import sympy as sp
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-gamma", "--gamma", help="parameter gamma to set temporal dependence of heat flux", default=1.0, type=float)
parser.add_argument("-alpha", "--alpha", help="parameter gamma to set temporal dependence of heat flux", default=3.0, type=float)
parser.add_argument("-beta", "--beta", help="parameter gamma to set temporal dependence of heat flux", default=1.2, type=float)
parser.add_argument("-stol", "--solver-tolerance", help="set accepted error of numerical solution w.r.t analytical solution", default=10**-12, type=float)
parser.add_argument("-ctol", "--coupling-tolerance", help="set accepted error of QN coupling", default=10**-12, type=float)
parser.add_argument("-subs", "--plain-subcycling", help="if set, do not interpolate between samples, but use plain subcycling for coupling", dest='plain_subcycling', action='store_true')
parser.add_argument("-t", "--time-dependence", help="choose whether there is a linear (l), quadratic (q) or sinusoidal (s) dependence on time", type=str, default="l")
parser.add_argument("-mth", "--method", help="time stepping method being used", default='ie')
parser.add_argument("-exec", "--executable", help="choose name of executable", default='heat.py')
parser.add_argument('--prefix', '-p', help='Path prefix for results', type=str, default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'experiments'))
parser.add_argument('--code-prefix', '-cp', help='Path prefix for code', type=str, default='~')

args = parser.parse_args()

manufactured_solution = sp.latex(get_manufactured_solution(args.time_dependence, args.alpha, args.beta, args.gamma).subs("x[0]","x").subs("x[1]","y"))

env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),'tools', 'templates'))
)

experiment_path = os.path.realpath(args.prefix)

evaluated_wr = [11, 12, 15, 21, 22, 25, 51, 52, 55]
evaluated_dT = [1.0, 0.5, 0.2, 0.1]
coupling_schemes = [CouplingScheme.SERIAL_FIRST_DIRICHLET.name]

print("parse experiments from {}".format(experiment_path))

error_table, _, _ = create_error_table(experiment_path, evaluated_wr, evaluated_dT, coupling_schemes)

qn_table, _, _ = create_qn_table(experiment_path, evaluated_wr, evaluated_dT, coupling_schemes)

report_template = env.get_template('report.md')

import subprocess
adapter_path = os.path.expanduser(os.path.join(args.code_prefix, "fenics-adapter"))
precice_path = os.path.expanduser(os.path.join(args.code_prefix, "precice"))
waveform_bindings_path = os.path.expanduser(os.path.join(args.code_prefix, "waveform-bindings"))

tutorials_hash = subprocess.check_output(["git", "describe", "--always", "--dirty"]).strip().decode() + " from " + subprocess.check_output(["git", "ls-remote", "--get-url"]).strip().decode()
adapter_hash = subprocess.check_output(["git", "-C", adapter_path, "describe", "--always", "--dirty"]).strip().decode() + " from " + subprocess.check_output(["git", "-C", adapter_path, "ls-remote", "--get-url"]).strip().decode()
waveform_bindings_hash = subprocess.check_output(["git", "-C", waveform_bindings_path, "describe", "--always", "--dirty"]).strip().decode() + " from " + subprocess.check_output(["git", "-C", waveform_bindings_path, "ls-remote", "--get-url"]).strip().decode()
precice_hash = subprocess.check_output(["git", "-C", precice_path, "describe", "--always", "--dirty"]).strip().decode() + " from " + subprocess.check_output(["git", "-C", precice_path, "ls-remote", "--get-url"]).strip().decode()

with open('report.md', "w") as file:
    file.write(report_template.render(date=str(datetime.datetime.now()),
                                      alpha=args.alpha,
                                      beta=args.beta,
                                      gamma=args.gamma,
                                      manufactured_solution=manufactured_solution,
                                      qn_table=qn_table,
                                      error_table=error_table,
                                      tutorials_hash=tutorials_hash,
                                      adapter_hash=adapter_hash,
                                      waveform_bindings_hash=waveform_bindings_hash,
                                      precice_hash=precice_hash,
                                      method=args.method,
                                      executable=args.executable,
                                      time_dependence=args.time_dependence))

