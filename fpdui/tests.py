import unittest
from imports import *
import pickle
from numpy.testing import assert_allclose

os.chdir("../testing files")

class TestFunctions(unittest.TestCase):

    def setUp(self):
        plt.ioff() # prevent mpl from drawing figures
        settings.reset_to_defaults()
        settings.settings['advanced_options'] = 0
        fo = open("data","rb")
        variables['ds'] = pickle.load(fo)
        variables['ds_sel'] = variables['ds']
        variables['bf'] = None
        variables['test'] = True
        fo.close()

    def test_can_browse(self):
        try:
            browseData()
        except:
            self.fail("Browse Data threw an exception and so failed")

    def test_diffraction_center_runs_with_no_sum_diff(self):
        find_diffraction_center()
        self.assertListEqual(variables['cyx'].tolist(), [135,126], "CYX was not accurate")
        self.assertEqual(variables['cr'], 63, "CR was not accurate")

    def test_diffraction_center_runs_with_sum_diff(self):
        find_diffraction_center()
        self.assertListEqual(variables['cyx'].tolist(), [135,126], "CYX was not accurate")
        self.assertEqual(variables['cr'], 63, "CR was not accurate")

    def test_generate_aperture_runs(self):
        try:
            generate_aperture()
        except:
            self.fail("Generate aperture threw an exception and so failed")

    def test_center_of_mass_runs_without_ap(self):
        try:
            del variables["ap"]
        except:
            pass
        calculate_CoM()
        pickle.dump(variables["com_yx"], open("com_yx_nap","wb"))
        correct_com_yx = pickle.load(open("com_yx_nap", "rb"))
        assert_allclose(correct_com_yx,variables["com_yx"])

    def test_center_of_mass_runs_with_ap(self):
        find_diffraction_center()
        generate_aperture()
        calculate_CoM()
        pickle.dump(variables["com_yx"], open("com_yx_ap","wb"))
        correct_com_yx = pickle.load(open("com_yx_ap", "rb"))
        assert_allclose(correct_com_yx,variables["com_yx"])

    def test_browse_CoM(self):
        calculate_sum_im()
        calculate_sum_dif()
        find_diffraction_center()
        calculate_CoM()
        try:
            browse_CoM()
        except:
            self.fail("Browse CoM threw an exception and so failed")

    def test_calculate_VADF(self):
        try:
            calculate_sum_im()
            calculate_sum_dif()
            find_diffraction_center()
            calculateVADF()
        except:
            self.fail("Calculate VADF threw an exception and so failed")
    
unittest.main()
