"""Nibabel impementation of DMRIHandler class"""
import nibabel as nib
from dipy.core.gradients import gradient_table
from dipy.segment.mask import median_otsu
import dipy.reconst.dti as dti
from dipy.io import read_bvals_bvecs
from dmri_handler import DMRIHandler

class NibabelDMRIHandler(DMRIHandler):
    """Nibabel implementation of DMRIHandler class"""
    def __init__(self, dmri_file, fbvals, fbvecs):
        """Constructor
            dmri_file - file with diffusion MRI
            fbvals - b-values file
            fbvecs - b-vectors file
        """
        DMRIHandler.__init__(self, dmri_file, fbvals, fbvecs)
        self.tenfit = None

    def get_shape(self):
        if self.tenfit is None:
            return None
        return self.tenfit.shape

    def handle(self):
        img = nib.load(self.dmri_file)
        data = img.get_data()
        bvals, bvecs = read_bvals_bvecs(self.fbvals, self.fbvecs)
        gtab = gradient_table(bvals, bvecs)
        maskdata, mask = median_otsu(data, 3, 1, True,\
                             vol_idx=range(10, 50), dilate=2)
        #print('maskdata.shape (%d, %d, %d, %d)' % maskdata.shape)
        tenmodel = dti.TensorModel(gtab)
        self.tenfit = tenmodel.fit(maskdata)

    def get_eigen_vectors(self):
        if self.tenfit is not None:
            return self.tenfit.evecs
        return self.tenfit

    def get_eigen_values(self):
        if self.tenfit is not None:
            return self.tenfit.evals
        return self.tenfit
