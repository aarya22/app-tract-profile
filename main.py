import AFQ.utils.streamlines as aus
import AFQ.dti as dti
import nibabel as nib
import codecs
import json
import os
import AFQ.segmentation as seg
import numpy as np

def main():
    with open('config.json') as config_json:
        config = json.load(config_json)

    data_file = str(config['data_file'])
    data_bval = str(config['data_bval'])
    data_bvec = str(config['data_bvec'])
    tracks = str(config['tck_data'])
    img = nib.load(data_file)    

    print("Calculating DTI...")
    if not os.path.exists('./dti_FA.nii.gz'):
        dti_params = dti.fit_dti(data_file, data_bval, data_bvec, out_dir='.')
    else:
        dti_params = {'FA': './dti_FA.nii.gz',
                      'params': './dti_params.nii.gz'}
       
    FA_img = nib.load(dti_params['FA'])
    FA_data = FA_img.get_data()
    print("Extracting tract profiles...")

    path = os.getcwd() + '/profile/'
    if not os.path.exists(path):
        os.makedirs(path)

    tg = nib.streamlines.load(tracks).tractogram
    streamlines = list(tg.apply_affine(np.linalg.inv(img.affine)).streamlines)
    profile = seg.calculate_tract_profile(FA_data, streamlines)
    profile = profile.tolist()
    t = os.path.splitext(os.path.basename(tracks))[0] #remove the .tck from string
    p = path+'/'+'out.json'
    json.dump(profile, codecs.open(p, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    
main()
