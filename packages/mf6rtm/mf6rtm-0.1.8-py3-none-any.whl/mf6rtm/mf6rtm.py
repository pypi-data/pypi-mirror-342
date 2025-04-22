"""The mf6rtm module provides the Mf6RTM class that couples modflowapi and
phreeqcrm.
"""
from pathlib import Path
import os
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PIL import Image
import pandas as pd
import numpy as np
import flopy
import phreeqcrm
import modflowapi
# from modflowapi.extensions import ApiSimulation
from datetime import datetime
# from time import sleep
from . import utils


# global variables
DT_FMT = "%Y-%m-%d %H:%M:%S"

time_units_dic = {
    'seconds': 1,
    'minutes': 60,
    'hours': 3600,
    'days': 86400,
    'years': 31536000,
    'unknown': 1 # if unknown assume seconds
}

def prep_to_run(wd):
    '''Prepares the model to run by checking if the model directory contains the necessary files
    and returns the path to the yaml file (phreeqcrm) and the dll file (mf6 api)'''
    # check if wd exists
    assert os.path.exists(wd), f'{wd} not found'
    # check if file starting with libmf6 exists
    dll = [f for f in os.listdir(wd) if f.startswith('libmf6')]
    assert len(dll) == 1, 'libmf6 dll not found in model directory'
    assert os.path.exists(os.path.join(wd, 'mf6rtm.yaml')), 'mf6rtm.yaml not found in model directory'

    nam = [f for f in os.listdir(wd) if f.endswith('.nam')]
    assert 'mfsim.nam' in nam, 'mfsim.nam file not found in model directory'
    assert 'gwf.nam' in nam, 'gwf.nam file not found in model directory'
    dll = os.path.join(wd, 'libmf6')
    yamlfile = os.path.join(wd, 'mf6rtm.yaml')

    return yamlfile, dll

def solve(wd, reactive=True, nthread=1):
    '''Wrapper to prepare and call solve functions
    '''

    mf6rtm = initialize_interfaces(wd, nthread=nthread)
    if not reactive:
        mf6rtm._set_reactive(reactive)
    success = mf6rtm._solve()
    return success

def initialize_interfaces(wd, nthread=1):
    '''Function to initialize the interfaces for modflowapi and phreeqcrm and returns the mf6rtm object
    '''

    yamlfile, dll = prep_to_run(wd)

    if nthread > 1:
        # set nthreds to nthread
        set_nthread_yaml(yamlfile, nthread=nthread)

    # initialize the interfaces
    mf6api = Mf6API(wd, dll)
    phreeqcrm = PhreeqcBMI(yamlfile)
    mf6rtm = Mf6RTM(wd, mf6api, phreeqcrm)
    return mf6rtm

def set_nthread_yaml(yamlfile, nthread=1):
    '''Function to set the number of threads in the yaml file
    '''
    with open(yamlfile, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'nthreads' in line:
            lines[i] = f'  nthreads: {nthread}\n'
    with open(yamlfile, 'w') as f:
        f.writelines(lines)
    return

def get_mf6_dis(sim):
    '''Function to extract dis from modflow6 sim object
    '''
    dis = sim.get_model(sim.model_names[0]).dis
    nlay = dis.nlay.get_data()
    nrow = dis.nrow.get_data()
    ncol = dis.ncol.get_data()
    return nlay, nrow, ncol


def calc_nxyz_from_dis(sim):
    '''Function to calculate number of cells from dis object
    '''
    nlay, nrow, ncol = get_mf6_dis(sim)
    return nlay*nrow*ncol

def get_mf6_disv(sim):
    #TODO: implement this function
    ...

def determine_grid_type(sim):
    '''Function to determine the grid type of the model
    '''
    # get the grid type
    mf6 = sim.get_model(sim.model_names[0])
    distype = mf6.get_grid_type().name
    return distype

class PhreeqcBMI(phreeqcrm.BMIPhreeqcRM):

    def __init__(self, yaml="mf6rtm.yaml"):
        phreeqcrm.BMIPhreeqcRM.__init__(self)
        self.initialize(yaml)
        self.sat_now = None

    def get_grid_to_map(self):
        '''Function to get grid to map
        '''
        return self.GetGridToMap()

    def _prepare_phreeqcrm_bmi(self):
        '''Prepare phreeqc bmi for reaction calculations
        '''
        self.SetScreenOn(True)
        self.set_scalar("NthSelectedOutput", 0)
        sout_headers = self.GetSelectedOutputHeadings()
        soutdf = pd.DataFrame(columns=sout_headers)

        # set attributes
        self.components = self.get_value_ptr("Components")
        self.ncomps = len(self.components)
        self.soutdf = soutdf
        self.sout_headers = sout_headers

    def _set_ctime(self, ctime):
        '''Set the current time in phreeqc bmi
        '''
        # self.ctime = self.SetTime(ctime*86400)
        self.ctime = ctime

    def set_scalar(self, var_name, value):
        itemsize = self.get_var_itemsize(var_name)
        nbytes = self.get_var_nbytes(var_name)
        dim = nbytes // itemsize

        if dim != 1:
            raise ValueError(f"{var_name} is not a scalar")

        vtype = self.get_var_type(var_name)
        dest = np.empty(1, dtype=vtype)
        dest[0] = value
        x = self.set_value(var_name, dest)

    def _solve_phreeqcrm(self, dt, diffmask):
        '''Function to solve phreeqc bmi
        '''
        # status = phreeqc_rm.SetTemperature([self.init_temp[0]] * self.ncpl)
        # status = phreeqc_rm.SetPressure([2.0] * nxyz)
        self.SetTimeStep(dt*1.0/self.GetTimeConversion())

        if self.sat_now is not None:
            sat = self.sat_now
        else:
            sat = [1]*self.GetGridCellCount()

        self.SetSaturation(sat)

        # update which cells to run depending on conc change between tsteps
        if diffmask is not None:
            # get idx where diffmask is 0
            inact = get_indices(0, diffmask)
            if len(inact) > 0:
                for i in inact:
                    sat[i] = 0
            print(f"{'Cells sent to reactions':<25} | {self.GetGridCellCount()-len(inact):<0}/{self.GetGridCellCount():<15}")
            self.SetSaturation(sat)

        print_selected_output_on = True
        # print_chemistry_on = False
        status = self.SetSelectedOutputOn(print_selected_output_on)
        status = self.SetPrintChemistryOn(False, False, False)
        # reactions loop
        sol_start = datetime.now()

        message = f"{'Reaction loop':<25} | {'Stress period:':<15} {self.kper:<5} | {'Time step:':<15} {self.kstp:<10} | {'Running ...':<10}"
        self.LogMessage(message+'\n')	# log message
        print(message)
        # self.ScreenMessage(message)
        # status = self.RunCells()
        # if status < 0:
        #     print('Error in RunCells: {0}'.format(status))
        self.update()
        td = (datetime.now() - sol_start).total_seconds() / 60.0
        message = f"{'Reaction loop':<25} | {'Stress period:':<15} {self.kper:<5} | {'Time step:':<15} {self.kstp:<10} | {'Completed in :':<10} {td//60:.0f} min {td%60:.4f} sec\n\n"
        self.LogMessage(message)
        print(message)
        # self.ScreenMessage(message)


    def _get_kper_kstp_from_mf6api(self, mf6api):
        '''Function to get the kper and kstp from mf6api
        '''
        assert isinstance(mf6api, Mf6API), 'mf6api must be an instance of Mf6API'
        self.kper = mf6api.kper
        self.kstp = mf6api.kstp
        return


class Mf6API(modflowapi.ModflowApi):
    def __init__(self, wd, dll):
        # TODO: reverse the order of args to match modflowapi?
        modflowapi.ModflowApi.__init__(self, dll, working_directory=wd)
        self.initialize()
        self.sim = flopy.mf6.MFSimulation.load(sim_ws=wd, verbosity_level=0)
        self.fmi = False

    def _prepare_mf6(self):
        '''Prepare mf6 bmi for transport calculations
        '''
        self.modelnmes = [nme.capitalize() for nme in self.sim.model_names]
        self.components = [nme.capitalize() for nme in self.sim.model_names[1:]]
        self.nsln = self.get_subcomponent_count()
        self.sim_start = datetime.now()
        self.ctimes = [0.0]
        self.num_fails = 0

    def _check_fmi(self):
        '''Check if fmi is in the nam file
        '''
        ...
        return

    def _set_simtype_gwt(self):
        '''Set the gwt sim type as sequential or flow interface
        '''
        ...

    def _solve_gwt(self):
        '''Function to solve the transport loop
        '''
        # prep to solve
        for sln in range(1, self.nsln+1):
            self.prepare_solve(sln)
        # the one-based stress period number
        stress_period = self.get_value(self.get_var_address("KPER", "TDIS"))[0]
        time_step = self.get_value(self.get_var_address("KSTP", "TDIS"))[0]

        self.kper = stress_period
        self.kstp = time_step
        msg = f"{'Transport loop':<25} | {'Stress period:':<15} {stress_period:<5} | {'Time step:':<15} {time_step:<10} | {'Running ...':<10}"
        print(msg)
        # mf6 transport loop block
        for sln in range(1, self.nsln+1):
            # if self.fixed_components is not None and modelnmes[sln-1] in self.fixed_components:
            #     print(f'not transporting {modelnmes[sln-1]}')
            #     continue

            # set iteration counter
            kiter = 0
            # max number of solution iterations
            max_iter = self.get_value(self.get_var_address("MXITER", f"SLN_{sln}"))  # FIXME: not sure to define this inside the loop
            self.prepare_solve(sln)

            sol_start = datetime.now()
            while kiter < max_iter:
                convg = self.solve(sln)
                if convg:
                    td = (datetime.now() - sol_start).total_seconds() / 60.0
                    break
                kiter += 1
            if not convg:
                td = (datetime.now() - sol_start).total_seconds() / 60.0
                print("\nTransport stress period: {0} --- time step: {1} --- did not converge with {2} iters --- took {3:10.5G} mins".format(stress_period, time_step, kiter, td))
                self.num_fails += 1
            try:
                self.finalize_solve(sln)
            except:
                pass
        td = (datetime.now() - sol_start).total_seconds() / 60.0
        print(f"{'Transport loop':<25} | {'Stress period:':<15} {stress_period:<5} | {'Time step:':<15} {time_step:<10} | {'Completed in :':<10}  {td//60:.0f} min {td%60:.4f} sec")

    def _check_num_fails(self):
        if self.num_fails > 0:
            print("\nTransport failed to converge {0} times \n".format(self.num_fails))
        else:
            print("\nTransport converged successfully without any fails")

class Mf6RTM(object):
    def __init__(self, wd, mf6api, phreeqcbmi):
        assert isinstance(mf6api, Mf6API), 'MF6API must be an instance of Mf6API'
        assert isinstance(phreeqcbmi, PhreeqcBMI), 'PhreeqcBMI must be an instance of PhreeqcBMI'
        self.mf6api = mf6api
        self.phreeqcbmi = phreeqcbmi
        self.charge_offset = 0.0
        self.wd = wd
        self.sout_fname = 'sout.csv'
        self.reactive = True
        self.epsaqu = 0.0
        self.fixed_components = None
        self.get_selected_output_on = True

        # set discretization
        self._set_dis()
        # set time conversion factor
        self.set_time_conversion()

    def get_saturation_from_mf6(self):
        """
        Get the saturation

        Parameters
        ----------
        mf6 (modflowapi): the modflow api object

        Returns
        -------
        array: the saturation
        """
        sat = {component: self.mf6api.get_value(
            self.mf6api.get_var_address("FMI/GWFSAT", f'{component}')
            ) for component in self.phreeqcbmi.components}
        # select the first component to get the length of the array
        sat = sat[self.phreeqcbmi.components[0]] # saturation is the same for all components
        self.phreeqcbmi.sat_now = sat # set phreeqcmbi saturation
        return sat

    def get_time_units_from_mf6(self):
        '''Function to get the time units from mf6
        '''
        return self.mf6api.sim.tdis.time_units.get_data()

    def set_time_conversion(self):
        '''Function to set the time conversion factor
        '''
        time_units = self.get_time_units_from_mf6()
        self.time_conversion = 1.0 / time_units_dic[time_units]
        self.phreeqcbmi.SetTimeConversion(self.time_conversion)

    def _set_fixed_components(self, fixed_components):
        ...
    def _set_reactive(self, reactive):
        '''Set the model to run only transport or transport and reactions
        '''
        self.reactive = reactive

    def _set_dis(self):
        '''Set the model grid dimensions according to mf6 grid type
        '''
        if determine_grid_type(self.mf6api.sim) == 'DIS':
            self.nlay, self.nrow, self.ncol = get_mf6_dis(self.mf6api.sim)
            self.nxyz = calc_nxyz_from_dis(self.mf6api.sim)
        elif determine_grid_type(self.mf6api.sim) == 'DISV':
            self.nlay = self.mf6api.sim.nlay
            self.ncpl = self.mf6api.sim.ncpl
            self.nxyz = self.nlay*self.ncpl

    def _prepare_to_solve(self):
        '''Prepare the model to solve
        '''
        # check if sout fname exists
        if self._check_sout_exist():
            # if found remove it
            self._rm_sout_file()

        self.mf6api._prepare_mf6()
        self.phreeqcbmi._prepare_phreeqcrm_bmi()

        # get and write sout headers
        self._write_sout_headers()

    def _set_ctime(self):
        '''Set the current time of the simulation from mf6api
        '''
        self.ctime = self.mf6api.get_current_time()
        self.phreeqcbmi._set_ctime(self.ctime)
        return self.ctime

    def _set_etime(self):
        '''Set the end time of the simulation from mf6api
        '''
        self.etime = self.mf6api.get_end_time()
        return self.etime

    def _set_time_step(self):
        self.time_step = self.mf6api.get_time_step()
        return self.time_step

    def _finalize(self):
        '''Finalize the APIs
        '''
        self._finalize_mf6api()
        self._finalize_phreeqcrm()
        return

    def _finalize_mf6api(self):
        '''Finalize the mf6api
        '''
        self.mf6api.finalize()

    def _finalize_phreeqcrm(self):
        '''Finalize the phreeqcrm api
        '''
        self.phreeqcbmi.finalize()

    def _get_cdlbl_vect(self):
        '''Get the concentration array from phreeqc bmi reshape to (ncomps, nxyz)
        '''
        c_dbl_vect = self.phreeqcbmi.GetConcentrations()

        conc = [c_dbl_vect[i:i + self.nxyz] for i in range(0, len(c_dbl_vect), self.nxyz)]  # reshape array
        return conc

    def _set_conc_at_current_kstep(self, c_dbl_vect):
        '''Saves the current concentration array to the object
        '''
        self.current_iteration_conc = np.reshape(c_dbl_vect, (self.phreeqcbmi.ncomps, self.nxyz))

    def _set_conc_at_previous_kstep(self, c_dbl_vect):
        '''Saves the current concentration array to the object
        '''
        self.previous_iteration_conc = np.reshape(c_dbl_vect, (self.phreeqcbmi.ncomps, self.nxyz))

    def _transfer_array_to_mf6(self):
        '''Transfer the concentration array to mf6
        '''
        c_dbl_vect = self._get_cdlbl_vect()

        # check if reactive cells were skipped due to small changes from transport and replace with previous conc
        if self._check_previous_conc_exists() and self._check_inactive_cells_exist(self.diffmask):
            c_dbl_vect = self._replace_inactive_cells(c_dbl_vect, self.diffmask)
        else:
            pass

        conc_dic = {}
        for e, c in enumerate(self.phreeqcbmi.components):
            # conc_dic[c] = np.reshape(c_dbl_vect[e], (self.nlay, self.nrow, self.ncol))
            conc_dic[c] = c_dbl_vect[e]
        # Set concentrations in mf6
            if c.lower() == 'charge':
                self.mf6api.set_value(f'{c.upper()}/X', concentration_l_to_m3(conc_dic[c]) + self.charge_offset)
            else:
                self.mf6api.set_value(f'{c.upper()}/X', concentration_l_to_m3(conc_dic[c]))
        return c_dbl_vect

    def _check_previous_conc_exists(self):
        '''Function to replace inactive cells in the concentration array
        '''
        # check if self.previous_iteration_conc is a property
        if not hasattr(self, 'previous_iteration_conc'):
            return False
        else:
            return True

    def _check_inactive_cells_exist(self, diffmask):
        '''Function to check if inactive cells exist in the concentration array
        '''
        inact = get_indices(0, diffmask)
        if len(inact) > 0:
            return True
        else:
            return False

    def _replace_inactive_cells(self, c_dbl_vect, diffmask):
        '''Function to replace inactive cells in the concentration array
        '''
        c_dbl_vect = np.reshape(c_dbl_vect, (self.phreeqcbmi.ncomps, self.nxyz))
        # get inactive cells
        inactive_idx = [get_indices(0, diffmask) for k in range(self.phreeqcbmi.ncomps)]
        c_dbl_vect[:, inactive_idx] = self.previous_iteration_conc[:, inactive_idx]
        c_dbl_vect = c_dbl_vect.flatten()
        conc = [c_dbl_vect[i:i + self.nxyz] for i in range(0, len(c_dbl_vect), self.nxyz)]
        return conc

    def _transfer_array_to_phreeqcrm(self):
        '''Transfer the concentration array to phreeqc bmi
        '''
        mf6_conc_array = []
        for c in self.phreeqcbmi.components:
            if c.lower() == 'charge':
                mf6_conc_array.append(concentration_m3_to_l(self.mf6api.get_value(self.mf6api.get_var_address("X", f'{c.upper()}')) - self.charge_offset))

            else:
                mf6_conc_array.append(concentration_m3_to_l(self.mf6api.get_value(self.mf6api.get_var_address("X", f'{c.upper()}'))))

        c_dbl_vect = np.reshape(mf6_conc_array, self.nxyz*self.phreeqcbmi.ncomps)
        self.phreeqcbmi.SetConcentrations(c_dbl_vect)

        #set the kper and kstp
        self.phreeqcbmi._get_kper_kstp_from_mf6api(self.mf6api) # FIXME: calling this func here is not ideal

        return c_dbl_vect

    def _update_selected_output(self):
        '''Update the selected output dataframe and save to attribute
        '''
        self._get_selected_output()
        updf = pd.concat([self.phreeqcbmi.soutdf.astype(self._current_soutdf.dtypes), self._current_soutdf])
        self._update_soutdf(updf)

    def __replace_inactive_cells_in_sout(self, sout, diffmask):
        '''Function to replace inactive cells in the selected output dataframe
        '''
        # match headers in components closest string

        inactive_idx = get_indices(0, diffmask)

        sout[:, inactive_idx] = self._sout_k[:, inactive_idx]
        return sout

    def _get_selected_output(self):
        '''Get the selected output from phreeqc bmi and replace skipped reactive cells with previous conc
        '''
        # selected ouput
        self.phreeqcbmi.set_scalar("NthSelectedOutput", 0)
        sout = self.phreeqcbmi.GetSelectedOutput()
        sout = [sout[i:i + self.nxyz] for i in range(0, len(sout), self.nxyz)]
        sout = np.array(sout)
        if self._check_inactive_cells_exist(self.diffmask) and hasattr(self, '_sout_k'):

            sout = self.__replace_inactive_cells_in_sout(sout, self.diffmask)
        self._sout_k = sout #save sout to a private attribute
        # add time to selected ouput
        sout[0] = np.ones_like(sout[0])*(self.ctime+self.time_step)
        df = pd.DataFrame(columns=self.phreeqcbmi.soutdf.columns)
        for col, arr in zip(df.columns, sout):
            df[col] = arr
        self._current_soutdf = df

    def _update_soutdf(self, df):
        '''Update the selected output dataframe to phreeqcrm object
        '''
        self.phreeqcbmi.soutdf = df

    def _check_sout_exist(self):
        '''Check if selected output file exists
        '''
        if os.path.exists(os.path.join(self.wd, self.sout_fname)):
            return True
        else :
            return False

    def _write_sout_headers(self):
        '''Write selected output headers to a file
        '''
        with open(os.path.join(self.wd,self.sout_fname), 'w') as f:
            f.write(','.join(self.phreeqcbmi.sout_headers))
            f.write('\n')

    def _rm_sout_file(self):
        '''Remove the selected output file
        '''
        try:
            os.remove(os.path.join(self.wd, self.sout_fname))
        except:
            pass

    def _append_to_soutdf_file(self):
        '''Append the current selected output to the selected output file
        '''
        assert not self._current_soutdf.empty, 'current sout is empty'
        self._current_soutdf.to_csv(os.path.join(self.wd, self.sout_fname), mode='a', index=False, header=False)

    def _export_soutdf(self):
        '''Export the selected output dataframe to a csv file
        '''
        self.phreeqcbmi.soutdf.to_csv(os.path.join(self.wd, self.sout_fname), index=False)

    def _solve(self):
        '''Solve the model
        '''
        success = False  # initialize success flag
        sim_start = datetime.now()
        self._prepare_to_solve()

        # check sout was created
        assert self._check_sout_exist(), f'{self.sout_fname} not found'

        print("Starting transport solution at {0}".format(sim_start.strftime(DT_FMT)))
        # print(f"Solving the following components: {', '.join([nme for nme in self.mf6api.modelnmes])}")
        ctime = self._set_ctime()
        etime = self._set_etime()
        while ctime < etime:
            temp_time = datetime.now()
            print(f"Starting solution at {temp_time.strftime(DT_FMT)}")
            # length of the current solve time
            dt = self._set_time_step()
            self.mf6api.prepare_time_step(dt)
            self.mf6api._solve_gwt()

            # get saturation
            self.get_saturation_from_mf6()

            if self.reactive:
                # reaction block
                c_dbl_vect = self._transfer_array_to_phreeqcrm()
                self._set_conc_at_current_kstep(c_dbl_vect)
                if ctime == 0.0:
                    self.diffmask = np.ones(self.nxyz)
                else:
                    diffmask = get_conc_change_mask(self.current_iteration_conc,
                                self.previous_iteration_conc,
                                self.phreeqcbmi.ncomps, self.nxyz,
                                treshold=self.epsaqu)
                    self.diffmask = diffmask
                # solve reactions
                self.phreeqcbmi._solve_phreeqcrm(dt, diffmask = self.diffmask)
                c_dbl_vect = self._transfer_array_to_mf6()
                if self.get_selected_output_on:
                    # get sout and update df
                    self._update_selected_output()
                    # append current sout rows to file
                    self._append_to_soutdf_file()
                self._set_conc_at_previous_kstep(c_dbl_vect)

            self.mf6api.finalize_time_step()
            ctime = self._set_ctime()  # update the current time tracking

        sim_end = datetime.now()
        td = (sim_end - sim_start).total_seconds() / 60.0

        self.mf6api._check_num_fails()

        print("\nReactive transport solution finished at {0} --- it took: {1:10.5G} mins".format(sim_end.strftime(DT_FMT), td))

        # Clean up and close api objs
        try:
            self._finalize()
            success = True
            print(mrbeaker())
            print('\nMR BEAKER IMPORTANT MESSAGE: MODEL RUN FINISHED BUT CHECK THE RESULTS .. THEY ARE PROLY RUBBISH\n')
        except:
            print('MR BEAKER IMPORTANT MESSAGE: SOMETHING WENT WRONG. BUMMER\n')
            pass
        return success

def get_indices(element, lst):
    return [i for i, x in enumerate(lst) if x == element]

def get_less_than_zero_idx(arr):
    '''Function to get the index of all occurrences of <0 in an array
    '''
    idx = np.where(arr < 0)
    return idx

def get_inactive_idx(arr, val = 1e30):
    '''Function to get the index of all occurrences of <0 in an array
    '''
    idx = list(np.where(arr >= val)[0])
    return idx

def get_conc_change_mask(ci, ck, ncomp, nxyz, treshold=1e-10):
    '''Function to get the active-inactive cell mask for concentration change to inform phreeqc which cells to update
    '''
    # reshape arrays to 2D (nxyz, ncomp)
    ci = ci.reshape(nxyz, ncomp)
    ck = ck.reshape(nxyz, ncomp)+1e-30

    # get the difference between the two arrays and divide by ci
    diff = np.abs((ci - ck.reshape(-1*nxyz, ncomp))/ci) < treshold
    diff = np.where(diff, 0, 1)
    diff = diff.sum(axis=1)

    # where values <0 put -1 else 1
    diff = np.where(diff == 0, 0, 1)
    return diff

def mrbeaker():
    '''ASCII art of Mr. Beaker
    '''
    # get the path of this file
    whereismrbeaker = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mrbeaker.png')
    mr_beaker_image = Image.open(whereismrbeaker)

    # Resize the image to fit the terminal width
    terminal_width = 80  # Adjust this based on your terminal width
    aspect_ratio = mr_beaker_image.width / mr_beaker_image.height
    terminal_height = int(terminal_width / aspect_ratio*0.5)
    mr_beaker_image = mr_beaker_image.resize((terminal_width, terminal_height))

    # Convert the image to grayscale
    mr_beaker_image = mr_beaker_image.convert("L")

    # Convert the grayscale image to ASCII art
    ascii_chars = "%,.?>#*+=-:."

    mrbeaker = ""
    for y in range(int(mr_beaker_image.height)):
        mrbeaker += "\n"
        for x in range(int(mr_beaker_image.width)):
            pixel_value = mr_beaker_image.getpixel((x, y))
            mrbeaker += ascii_chars[pixel_value // 64]
        mrbeaker += "\n"
    return mrbeaker


def flatten_list(xss):
    '''Flatten a list of lists
    '''
    return [x for xs in xss for x in xs]


def concentration_l_to_m3(x):
    '''Convert M/L to M/m3
    '''
    c = x*1e3
    return c


def concentration_m3_to_l(x):
    '''Convert M/L to M/m3
    '''
    c = x*1e-3
    return c


def concentration_to_massrate(q, conc):
    '''Calculate mass rate from rate (L3/T) and concentration (M/L3)
    '''
    mrate = q*conc  # M/T
    return mrate


def concentration_volbulk_to_volwater(conc_volbulk, porosity):
    '''Calculate concentrations as volume of pore water from bulk volume and porosity
    '''
    conc_volwater = conc_volbulk*(1/porosity)
    return conc_volwater


def run_cmd():
    # get the current directory
    cwd = os.getcwd()
    # run the solve function
    solve(cwd)
