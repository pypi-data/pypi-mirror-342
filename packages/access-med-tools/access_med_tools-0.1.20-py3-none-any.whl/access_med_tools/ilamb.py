from pathlib import Path
import glob
import os
import xarray
import yaml
import copy
from .utilities import MyParser
from .CMORise import generate_cmip

rootpath = {
    "CMIP6": ["/g/data/fs38/publications/CMIP6", "/g/data/oi10/replicas/CMIP6","/g/data/zv30/cmip/CMIP6"],
    "CMIP5": ["/g/data/r87/", "/g/data/al33/", "/g/data/rr3/"],
    "non-CMIP": ["/g/data/p73/archive/non-CMIP"]
}

mip_vars ={
    'Emon':['cSoil'],
    'Lmon':['cVeg','gpp','lai','nbp','ra','rh','tsl'],
    'Amon':['evspsbl','hfls','hfss','hurs','pr','rlds','rlus','rsds','rsus','tasmax','tasmin','tas'],
    'Omon':['hfds'],
    }

def get_CMIP6_path(mip="*", institute = "*", dataset = "*", exp = "*", ensemble = "*", frequency="*", version="**", var="*"):
    return f"{mip}/{institute}/{dataset}/{exp}/{ensemble}/{frequency}/{var}/**/{version}/*.nc"

def get_CMIP5_path(group="*", mip="*", institute = "*", dataset = "*", exp = "*", ensemble = "*", frequency="*", version="**", var="*"):
    if group=="r87":
        return f"{group}/DRSv3/{mip}/{institute}/{dataset}/{exp}/mon/*/{frequency}/{ensemble}/*/{var}/*.nc"
    if group=="al33":
        return f"{group}/replicas/{mip}/combined/{institute}/{dataset}/{exp}/mon/*/{frequency}/{ensemble}/*/{var}/*.nc"
    if group=="rr3":
        return f"{group}/publications/{mip}/ouput1/{institute}/{dataset}/{exp}/mon/*/{frequency}/{ensemble}/*/{var}/*.nc"


get_path_function = {
    "CMIP6": get_CMIP6_path,
    "CMIP5": get_CMIP5_path
}

def add_model_to_tree(ilamb_root, merge, mip, institute, dataset, project, exp = None, ensemble = None, path = None, variables = None, output = None, output_range = None):
    """
    """

    if mip == 'non-CMIP':
        print(f"CMORisering {exp} and add result to ILAMB Tree")
        if dataset == 'ACCESS-ESM1-6':
            noncmip_path=path
            variables_dict = mip_vars
            variables_dict.pop('Omon')
            if output_range is not None:
                if len(output_range) == 2:
                    if os.path.isdir(f"{path}/output{output_range[0]:03d}") and os.path.isdir(f"{path}/output{output_range[1]:03d}"):
                        output_list=[f"output{num:03d}" for num in range(int(output_range[0]), int(output_range[1]) + 1)]
                    else:
                        print(f"{path}/{output_range[0]}",f"{path}/{output_range[1]}")
                        raise ValueError("start or end in the output_range is not correct")
                else:
                    raise ValueError("Format of output_range is not correct, please input a list [start, end]")
                
            elif isinstance(output,int):
                if os.path.isdir(f"{path}/output{output:03d}"):
                    output_list=[f"output{output:03d}"]
            elif isinstance(output,str):
                if os.path.isdir(f"{path}/output{int(output):03d}"):
                    output_list=[f"output{int(output):03d}"]
            elif isinstance(output,list):
                output_list=[f"output{num:03d}" for num in output]
            else:
                raise ValueError("Wrong type of input value")
            model_root=f"{ilamb_root}/MODELS/{dataset}"
            Path(model_root).mkdir(parents=True,exist_ok=True)
            generate_cmip(noncmip_path,model_root,variables_dict, outputs=output_list, ESM1_6=True, merge=merge)
        
        else:
            if path is None:
                path = rootpath['non-CMIP'][0]
            if variables is None:
                variables_dict=mip_vars.pop('Omon')
            else:
                for item in mip_vars.items():
                    varlist=copy.deepcopy(item[1])
                    for var in varlist:
                        if var not in variables:
                            mip_vars[item[0]].pop(mip_vars[item[0]].index(var))
                for key in copy.deepcopy(mip_vars):
                    if mip_vars[key] == []:
                        mip_vars.pop(key)
                variables_dict=mip_vars                   

            noncmip_path=f"{path}/{dataset}/{exp}"
            model_root=f"{ilamb_root}/MODELS/{dataset}/{exp}"
            Path(model_root).mkdir(parents=True,exist_ok=True)
            print(variables_dict)
            if 'Omon' in variables_dict:
                variables_dict.pop('Omon')

            generate_cmip(noncmip_path,model_root,variables_dict)
    
    else:
        print(f"Adding {dataset} to the ILAMB Tree")
        model_root = f"{ilamb_root}/MODELS/{dataset}/{exp}/{ensemble}"
        Path(model_root).mkdir(parents=True, exist_ok=True)

        for frequency, vars in mip_vars.items():
            for var in vars:
                for path in rootpath[project]:
                    if project=='CMIP5':
                        search_path = os.path.join(path, get_path_function[project](
                            group=path.split('/')[-2],
                            mip=mip,
                            institute=institute, 
                            dataset=dataset, 
                            exp=exp, 
                            ensemble=ensemble, 
                            frequency=frequency,
                        var=var))
                    else:
                        search_path = os.path.join(path, get_path_function[project](
                            mip=mip,
                            institute=institute, 
                            dataset=dataset, 
                            exp=exp, 
                            ensemble=ensemble, 
                            frequency=frequency,
                        var=var))
                    files = glob.glob(search_path)
                    if not files:
                        continue
                    
                    unique_files = []
                    for file in files:
                        filenames = [Path(path).stem for path in unique_files]
                        if Path(file).stem not in filenames:
                            unique_files.append(file)
                    files = unique_files

                    if len(files) > 1:
                        with xarray.open_mfdataset(files, use_cftime=True, combine_attrs='drop_conflicts') as f:
                            f.to_netcdf(f"{model_root}/{var}.nc")
                    else:
                        try:
                            Path(f"{model_root}/{var}.nc").unlink()
                        except:
                            pass
                        Path(f"{model_root}/{var}.nc").symlink_to(f"{files[0]}")

    return


def tree_generator():

    parser=MyParser(description="Generate an ILAMB-ROOT tree")

    parser.add_argument(
        '--datasets',
        default=False,
        nargs="+",
        help="YAML file specifying the model output(s) to add.",
    )

    parser.add_argument(
        '--ilamb_root',
        default=False,
        nargs="+",
        help="Path of the ILAMB-ROOT",
    )

    parser.add_argument(
        '--merge',
        action='store_true',
        help="Merge multiple outputs",

    )

    args = parser.parse_args()
    dataset_file = args.datasets[0]
    ilamb_root = args.ilamb_root[0]
    merge = args.merge

    Path(ilamb_root).mkdir(parents=True, exist_ok=True)
    try:
        Path(f"{ilamb_root}/DATA").unlink()
    except :
        pass
    Path(f"{ilamb_root}/DATA").symlink_to("/g/data/ct11/access-nri/replicas/ILAMB", target_is_directory=True)

    with open(dataset_file, 'r') as file:
        data = yaml.safe_load(file)

    datasets = data["datasets"]
    for dataset in datasets:
        add_model_to_tree(**dataset, ilamb_root=ilamb_root, merge=merge)
    
    return


if __name__=='__main__':
    tree_generator()
    
