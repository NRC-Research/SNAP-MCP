"""Auto-generated MELCOR enum classes.

Generated from *SelEditor.java files in cfnplugin.melcor.editors.enums.
Do not edit by hand — re-run tools/generate_bindings.py instead.
"""


class BHRightBoundaryIbcbhSel(object):
    """Enumeration of BHRightBoundaryIbcbhSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BHRightBoundaryIbcbhSel instance for a given integer value."""
        _MAP = {
            1: BHRightBoundaryIbcbhSel.v_1_Calculated_by_HS_Package(),
            4000: BHRightBoundaryIbcbhSel.v_4XXX_Tabular_Function_of_Time(),
            5000: BHRightBoundaryIbcbhSel.v_5XXX_Tabular_Function_of_Temp(),
            6000: BHRightBoundaryIbcbhSel.v_6XXX_Control_Function(),
        }
        return _MAP.get(v, BHRightBoundaryIbcbhSel("unknown_{}".format(v), v))

    @staticmethod
    def v_1_Calculated_by_HS_Package():
        """Returns the BHRightBoundaryIbcbhSel value for '[1] Calculated by HS Package'."""
        return BHRightBoundaryIbcbhSel('v_1_Calculated_by_HS_Package', 1)

    @staticmethod
    def v_4XXX_Tabular_Function_of_Time():
        """Returns the BHRightBoundaryIbcbhSel value for '[4XXX] Tabular Function of Time'."""
        return BHRightBoundaryIbcbhSel('v_4XXX_Tabular_Function_of_Time', 4000)

    @staticmethod
    def v_5XXX_Tabular_Function_of_Temp():
        """Returns the BHRightBoundaryIbcbhSel value for '[5XXX] Tabular Function of Temp'."""
        return BHRightBoundaryIbcbhSel('v_5XXX_Tabular_Function_of_Temp', 5000)

    @staticmethod
    def v_6XXX_Control_Function():
        """Returns the BHRightBoundaryIbcbhSel value for '[6XXX] Control Function'."""
        return BHRightBoundaryIbcbhSel('v_6XXX_Control_Function', 6000)


class BHRightBoundaryIflobhSel(object):
    """Enumeration of BHRightBoundaryIflobhSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BHRightBoundaryIflobhSel instance for a given integer value."""
        _MAP = {
            0: BHRightBoundaryIflobhSel.Internal_Flow(),
            1: BHRightBoundaryIflobhSel.External_Flow(),
        }
        return _MAP.get(v, BHRightBoundaryIflobhSel("unknown_{}".format(v), v))

    @staticmethod
    def Internal_Flow():
        """Returns the BHRightBoundaryIflobhSel value for 'Internal Flow'."""
        return BHRightBoundaryIflobhSel('Internal_Flow', 0)

    @staticmethod
    def External_Flow():
        """Returns the BHRightBoundaryIflobhSel value for 'External Flow'."""
        return BHRightBoundaryIflobhSel('External_Flow', 1)


class BHToRNClassSel(object):
    """Enumeration of BHToRNClassSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BHToRNClassSel instance for a given integer value."""
        _MAP = {
            0: BHToRNClassSel.None_(),
            1: BHToRNClassSel.Noble_Gas(),
            2: BHToRNClassSel.Alkali_Metals(),
            3: BHToRNClassSel.Alkaline_Earths(),
            4: BHToRNClassSel.Halogens(),
            5: BHToRNClassSel.Chalcogens(),
            6: BHToRNClassSel.Platinoids(),
            7: BHToRNClassSel.Early_Transition_Elements(),
            8: BHToRNClassSel.Tetravalent(),
            9: BHToRNClassSel.Trivalents(),
            10: BHToRNClassSel.Uranium(),
            11: BHToRNClassSel.More_Volatile_Main_Group(),
            12: BHToRNClassSel.Less_Volatile_Main_Group(),
            13: BHToRNClassSel.Boron(),
            14: BHToRNClassSel.Water(),
            15: BHToRNClassSel.Concrete(),
            15: BHToRNClassSel.Cesium_Iodide(),
        }
        return _MAP.get(v, BHToRNClassSel("unknown_{}".format(v), v))

    @staticmethod
    def None_():
        """Returns the BHToRNClassSel value for 'None'."""
        return BHToRNClassSel('None_', 0)

    @staticmethod
    def Noble_Gas():
        """Returns the BHToRNClassSel value for 'Noble Gas'."""
        return BHToRNClassSel('Noble_Gas', 1)

    @staticmethod
    def Alkali_Metals():
        """Returns the BHToRNClassSel value for 'Alkali Metals'."""
        return BHToRNClassSel('Alkali_Metals', 2)

    @staticmethod
    def Alkaline_Earths():
        """Returns the BHToRNClassSel value for 'Alkaline Earths'."""
        return BHToRNClassSel('Alkaline_Earths', 3)

    @staticmethod
    def Halogens():
        """Returns the BHToRNClassSel value for 'Halogens'."""
        return BHToRNClassSel('Halogens', 4)

    @staticmethod
    def Chalcogens():
        """Returns the BHToRNClassSel value for 'Chalcogens'."""
        return BHToRNClassSel('Chalcogens', 5)

    @staticmethod
    def Platinoids():
        """Returns the BHToRNClassSel value for 'Platinoids'."""
        return BHToRNClassSel('Platinoids', 6)

    @staticmethod
    def Early_Transition_Elements():
        """Returns the BHToRNClassSel value for 'Early Transition Elements'."""
        return BHToRNClassSel('Early_Transition_Elements', 7)

    @staticmethod
    def Tetravalent():
        """Returns the BHToRNClassSel value for 'Tetravalent'."""
        return BHToRNClassSel('Tetravalent', 8)

    @staticmethod
    def Trivalents():
        """Returns the BHToRNClassSel value for 'Trivalents'."""
        return BHToRNClassSel('Trivalents', 9)

    @staticmethod
    def Uranium():
        """Returns the BHToRNClassSel value for 'Uranium'."""
        return BHToRNClassSel('Uranium', 10)

    @staticmethod
    def More_Volatile_Main_Group():
        """Returns the BHToRNClassSel value for 'More Volatile Main Group'."""
        return BHToRNClassSel('More_Volatile_Main_Group', 11)

    @staticmethod
    def Less_Volatile_Main_Group():
        """Returns the BHToRNClassSel value for 'Less Volatile Main Group'."""
        return BHToRNClassSel('Less_Volatile_Main_Group', 12)

    @staticmethod
    def Boron():
        """Returns the BHToRNClassSel value for 'Boron'."""
        return BHToRNClassSel('Boron', 13)

    @staticmethod
    def Water():
        """Returns the BHToRNClassSel value for 'Water'."""
        return BHToRNClassSel('Water', 14)

    @staticmethod
    def Concrete():
        """Returns the BHToRNClassSel value for 'Concrete'."""
        return BHToRNClassSel('Concrete', 15)

    @staticmethod
    def Cesium_Iodide():
        """Returns the BHToRNClassSel value for 'Cesium Iodide'."""
        return BHToRNClassSel('Cesium_Iodide', 15)


class BMatSel(object):
    """Enumeration of BMatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BMatSel instance for a given integer value."""
        _MAP = {
            0: BMatSel.Steam(),
            1: BMatSel.Carbon_Dioxide(),
            2: BMatSel.Oxygen(),
            3: BMatSel.Hydrogen(),
            4: BMatSel.Deuterium(),
            5: BMatSel.Carbon_Monoxide(),
        }
        return _MAP.get(v, BMatSel("unknown_{}".format(v), v))

    @staticmethod
    def Steam():
        """Returns the BMatSel value for 'Steam'."""
        return BMatSel('Steam', 0)

    @staticmethod
    def Carbon_Dioxide():
        """Returns the BMatSel value for 'Carbon Dioxide'."""
        return BMatSel('Carbon_Dioxide', 1)

    @staticmethod
    def Oxygen():
        """Returns the BMatSel value for 'Oxygen'."""
        return BMatSel('Oxygen', 2)

    @staticmethod
    def Hydrogen():
        """Returns the BMatSel value for 'Hydrogen'."""
        return BMatSel('Hydrogen', 3)

    @staticmethod
    def Deuterium():
        """Returns the BMatSel value for 'Deuterium'."""
        return BMatSel('Deuterium', 4)

    @staticmethod
    def Carbon_Monoxide():
        """Returns the BMatSel value for 'Carbon Monoxide'."""
        return BMatSel('Carbon_Monoxide', 5)


class BatchReleaseSel(object):
    """Enumeration of BatchReleaseSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BatchReleaseSel instance for a given integer value."""
        _MAP = {
            0: BatchReleaseSel.Control_Volume_Names(),
            1: BatchReleaseSel.Control_Volume_Types(),
        }
        return _MAP.get(v, BatchReleaseSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Volume_Names():
        """Returns the BatchReleaseSel value for 'Control Volume Names'."""
        return BatchReleaseSel('Control_Volume_Names', 0)

    @staticmethod
    def Control_Volume_Types():
        """Returns the BatchReleaseSel value for 'Control Volume Types'."""
        return BatchReleaseSel('Control_Volume_Types', 1)


class BottomHeadIeukeySel(object):
    """Enumeration of BottomHeadIeukeySel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BottomHeadIeukeySel instance for a given integer value."""
        _MAP = {
            1: BottomHeadIeukeySel.zr(),
            2: BottomHeadIeukeySel.fe(),
            3: BottomHeadIeukeySel.cr(),
            4: BottomHeadIeukeySel.ni(),
            5: BottomHeadIeukeySel.blank(),
            6: BottomHeadIeukeySel.ag(),
            7: BottomHeadIeukeySel.cdin(),
            8: BottomHeadIeukeySel.blank(),
            9: BottomHeadIeukeySel.blank(),
            10: BottomHeadIeukeySel.b4c(),
            11: BottomHeadIeukeySel.zro2(),
            12: BottomHeadIeukeySel.feo(),
            13: BottomHeadIeukeySel.fe2o3(),
            14: BottomHeadIeukeySel.fe3o4(),
            15: BottomHeadIeukeySel.cr2o3(),
            16: BottomHeadIeukeySel.nio(),
            17: BottomHeadIeukeySel.b2o3(),
            18: BottomHeadIeukeySel.uo2(),
            19: BottomHeadIeukeySel.blank(),
            20: BottomHeadIeukeySel.blank(),
        }
        return _MAP.get(v, BottomHeadIeukeySel("unknown_{}".format(v), v))

    @staticmethod
    def zr():
        """Returns the BottomHeadIeukeySel value for 'zr'."""
        return BottomHeadIeukeySel('zr', 1)

    @staticmethod
    def fe():
        """Returns the BottomHeadIeukeySel value for 'fe'."""
        return BottomHeadIeukeySel('fe', 2)

    @staticmethod
    def cr():
        """Returns the BottomHeadIeukeySel value for 'cr'."""
        return BottomHeadIeukeySel('cr', 3)

    @staticmethod
    def ni():
        """Returns the BottomHeadIeukeySel value for 'ni'."""
        return BottomHeadIeukeySel('ni', 4)

    @staticmethod
    def blank():
        """Returns the BottomHeadIeukeySel value for 'blank'."""
        return BottomHeadIeukeySel('blank', 5)

    @staticmethod
    def ag():
        """Returns the BottomHeadIeukeySel value for 'ag'."""
        return BottomHeadIeukeySel('ag', 6)

    @staticmethod
    def cdin():
        """Returns the BottomHeadIeukeySel value for 'cdin'."""
        return BottomHeadIeukeySel('cdin', 7)

    @staticmethod
    def blank():
        """Returns the BottomHeadIeukeySel value for 'blank'."""
        return BottomHeadIeukeySel('blank', 8)

    @staticmethod
    def blank():
        """Returns the BottomHeadIeukeySel value for 'blank'."""
        return BottomHeadIeukeySel('blank', 9)

    @staticmethod
    def b4c():
        """Returns the BottomHeadIeukeySel value for 'b4c'."""
        return BottomHeadIeukeySel('b4c', 10)

    @staticmethod
    def zro2():
        """Returns the BottomHeadIeukeySel value for 'zro2'."""
        return BottomHeadIeukeySel('zro2', 11)

    @staticmethod
    def feo():
        """Returns the BottomHeadIeukeySel value for 'feo'."""
        return BottomHeadIeukeySel('feo', 12)

    @staticmethod
    def fe2o3():
        """Returns the BottomHeadIeukeySel value for 'fe2o3'."""
        return BottomHeadIeukeySel('fe2o3', 13)

    @staticmethod
    def fe3o4():
        """Returns the BottomHeadIeukeySel value for 'fe3o4'."""
        return BottomHeadIeukeySel('fe3o4', 14)

    @staticmethod
    def cr2o3():
        """Returns the BottomHeadIeukeySel value for 'cr2o3'."""
        return BottomHeadIeukeySel('cr2o3', 15)

    @staticmethod
    def nio():
        """Returns the BottomHeadIeukeySel value for 'nio'."""
        return BottomHeadIeukeySel('nio', 16)

    @staticmethod
    def b2o3():
        """Returns the BottomHeadIeukeySel value for 'b2o3'."""
        return BottomHeadIeukeySel('b2o3', 17)

    @staticmethod
    def uo2():
        """Returns the BottomHeadIeukeySel value for 'uo2'."""
        return BottomHeadIeukeySel('uo2', 18)

    @staticmethod
    def blank():
        """Returns the BottomHeadIeukeySel value for 'blank'."""
        return BottomHeadIeukeySel('blank', 19)

    @staticmethod
    def blank():
        """Returns the BottomHeadIeukeySel value for 'blank'."""
        return BottomHeadIeukeySel('blank', 20)


class BottomHeadImwdebSel(object):
    """Enumeration of BottomHeadImwdebSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BottomHeadImwdebSel instance for a given integer value."""
        _MAP = {
            0: BottomHeadImwdebSel.No_Metal_Steam_Reaction(),
            1: BottomHeadImwdebSel.Cylindrical_Metal_Steam_Reaction(),
            2: BottomHeadImwdebSel.SS_oxidation_only_no_Zr_oxidation(),
            3: BottomHeadImwdebSel.Zr_oxidation_only_no_SS_oxidation(),
        }
        return _MAP.get(v, BottomHeadImwdebSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Metal_Steam_Reaction():
        """Returns the BottomHeadImwdebSel value for 'No Metal/Steam Reaction'."""
        return BottomHeadImwdebSel('No_Metal_Steam_Reaction', 0)

    @staticmethod
    def Cylindrical_Metal_Steam_Reaction():
        """Returns the BottomHeadImwdebSel value for 'Cylindrical Metal/Steam Reaction'."""
        return BottomHeadImwdebSel('Cylindrical_Metal_Steam_Reaction', 1)

    @staticmethod
    def SS_oxidation_only_no_Zr_oxidation():
        """Returns the BottomHeadImwdebSel value for 'SS oxidation only; no Zr oxidation'."""
        return BottomHeadImwdebSel('SS_oxidation_only_no_Zr_oxidation', 2)

    @staticmethod
    def Zr_oxidation_only_no_SS_oxidation():
        """Returns the BottomHeadImwdebSel value for 'Zr oxidation only; no SS oxidation.'."""
        return BottomHeadImwdebSel('Zr_oxidation_only_no_SS_oxidation', 3)


class BurnActiveSel(object):
    """Enumeration of BurnActiveSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the BurnActiveSel instance for a given integer value."""
        _MAP = {
            0: BurnActiveSel.BUR_package_active(),
            1: BurnActiveSel.BUR_package_not_active(),
        }
        return _MAP.get(v, BurnActiveSel("unknown_{}".format(v), v))

    @staticmethod
    def BUR_package_active():
        """Returns the BurnActiveSel value for 'BUR package active'."""
        return BurnActiveSel('BUR_package_active', 0)

    @staticmethod
    def BUR_package_not_active():
        """Returns the BurnActiveSel value for 'BUR package not active'."""
        return BurnActiveSel('BUR_package_not_active', 1)


class CCSel(object):
    """Enumeration of CCSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CCSel instance for a given integer value."""
        _MAP = {
            -1: CCSel.Constant_Completeness(),
            0: CCSel.HECTR_Correlation(),
        }
        return _MAP.get(v, CCSel("unknown_{}".format(v), v))

    @staticmethod
    def Constant_Completeness():
        """Returns the CCSel value for 'Constant Completeness'."""
        return CCSel('Constant_Completeness', -1)

    @staticmethod
    def HECTR_Correlation():
        """Returns the CCSel value for 'HECTR Correlation'."""
        return CCSel('HECTR_Correlation', 0)


class CFRangeTypeSel(object):
    """Enumeration of CFRangeTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CFRangeTypeSel instance for a given integer value."""
        _MAP = {
            0: CFRangeTypeSel.Control_Volumes(),
            1: CFRangeTypeSel.Flow_Paths(),
            2: CFRangeTypeSel.Control_Functions(),
            3: CFRangeTypeSel.Heat_Structures(),
            4: CFRangeTypeSel.Core_Cells(),
            5: CFRangeTypeSel.Core_Components(),
            6: CFRangeTypeSel.Materials(),
        }
        return _MAP.get(v, CFRangeTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Volumes():
        """Returns the CFRangeTypeSel value for 'Control Volumes'."""
        return CFRangeTypeSel('Control_Volumes', 0)

    @staticmethod
    def Flow_Paths():
        """Returns the CFRangeTypeSel value for 'Flow Paths'."""
        return CFRangeTypeSel('Flow_Paths', 1)

    @staticmethod
    def Control_Functions():
        """Returns the CFRangeTypeSel value for 'Control Functions'."""
        return CFRangeTypeSel('Control_Functions', 2)

    @staticmethod
    def Heat_Structures():
        """Returns the CFRangeTypeSel value for 'Heat Structures'."""
        return CFRangeTypeSel('Heat_Structures', 3)

    @staticmethod
    def Core_Cells():
        """Returns the CFRangeTypeSel value for 'Core Cells'."""
        return CFRangeTypeSel('Core_Cells', 4)

    @staticmethod
    def Core_Components():
        """Returns the CFRangeTypeSel value for 'Core Components'."""
        return CFRangeTypeSel('Core_Components', 5)

    @staticmethod
    def Materials():
        """Returns the CFRangeTypeSel value for 'Materials'."""
        return CFRangeTypeSel('Materials', 6)


class CFTFNoSel(object):
    """Enumeration of CFTFNoSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CFTFNoSel instance for a given integer value."""
        _MAP = {
            0: CFTFNoSel.NO(),
            1: CFTFNoSel.CF(),
            2: CFTFNoSel.TF(),
        }
        return _MAP.get(v, CFTFNoSel("unknown_{}".format(v), v))

    @staticmethod
    def NO():
        """Returns the CFTFNoSel value for 'NO'."""
        return CFTFNoSel('NO', 0)

    @staticmethod
    def CF():
        """Returns the CFTFNoSel value for 'CF'."""
        return CFTFNoSel('CF', 1)

    @staticmethod
    def TF():
        """Returns the CFTFNoSel value for 'TF'."""
        return CFTFNoSel('TF', 2)


class CVAtmSel(object):
    """Enumeration of CVAtmSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CVAtmSel instance for a given integer value."""
        _MAP = {
            0: CVAtmSel.Water_Partial_Pressure(),
            1: CVAtmSel.Relative_Humidity(),
            2: CVAtmSel.Dewpoint_Temperature(),
        }
        return _MAP.get(v, CVAtmSel("unknown_{}".format(v), v))

    @staticmethod
    def Water_Partial_Pressure():
        """Returns the CVAtmSel value for 'Water Partial Pressure'."""
        return CVAtmSel('Water_Partial_Pressure', 0)

    @staticmethod
    def Relative_Humidity():
        """Returns the CVAtmSel value for 'Relative Humidity'."""
        return CVAtmSel('Relative_Humidity', 1)

    @staticmethod
    def Dewpoint_Temperature():
        """Returns the CVAtmSel value for 'Dewpoint Temperature'."""
        return CVAtmSel('Dewpoint_Temperature', 2)


class CVFogSel(object):
    """Enumeration of CVFogSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CVFogSel instance for a given integer value."""
        _MAP = {
            0: CVFogSel.Mass_of_Fog(),
            1: CVFogSel.Volume_Fraction(),
        }
        return _MAP.get(v, CVFogSel("unknown_{}".format(v), v))

    @staticmethod
    def Mass_of_Fog():
        """Returns the CVFogSel value for 'Mass of Fog'."""
        return CVFogSel('Mass_of_Fog', 0)

    @staticmethod
    def Volume_Fraction():
        """Returns the CVFogSel value for 'Volume Fraction'."""
        return CVFogSel('Volume_Fraction', 1)


class CVHPkgAtmcsSel(object):
    """Enumeration of CVHPkgAtmcsSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CVHPkgAtmcsSel instance for a given integer value."""
        _MAP = {
            0: CVHPkgAtmcsSel.Default(),
            1: CVHPkgAtmcsSel.FMOD_FEM(),
        }
        return _MAP.get(v, CVHPkgAtmcsSel("unknown_{}".format(v), v))

    @staticmethod
    def Default():
        """Returns the CVHPkgAtmcsSel value for 'Default'."""
        return CVHPkgAtmcsSel('Default', 0)

    @staticmethod
    def FMOD_FEM():
        """Returns the CVHPkgAtmcsSel value for 'FMOD (FEM)'."""
        return CVHPkgAtmcsSel('FMOD_FEM', 1)


class CVHPoolSel(object):
    """Enumeration of CVHPoolSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CVHPoolSel instance for a given integer value."""
        _MAP = {
            1: CVHPoolSel.Only_Pool(),
            2: CVHPoolSel.Only_Atmosphere(),
            3: CVHPoolSel.Both(),
        }
        return _MAP.get(v, CVHPoolSel("unknown_{}".format(v), v))

    @staticmethod
    def Only_Pool():
        """Returns the CVHPoolSel value for 'Only Pool'."""
        return CVHPoolSel('Only_Pool', 1)

    @staticmethod
    def Only_Atmosphere():
        """Returns the CVHPoolSel value for 'Only Atmosphere'."""
        return CVHPoolSel('Only_Atmosphere', 2)

    @staticmethod
    def Both():
        """Returns the CVHPoolSel value for 'Both'."""
        return CVHPoolSel('Both', 3)


class CavLayerSel(object):
    """Enumeration of CavLayerSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CavLayerSel instance for a given integer value."""
        _MAP = {
            0: CavLayerSel.HOX_Heavy_Oxide(),
            1: CavLayerSel.LOX_Light_Oxide(),
            2: CavLayerSel.MET_Metal(),
            3: CavLayerSel.HMX_Heavy_Mixture(),
            4: CavLayerSel.LMX_Light_Mixture(),
        }
        return _MAP.get(v, CavLayerSel("unknown_{}".format(v), v))

    @staticmethod
    def HOX_Heavy_Oxide():
        """Returns the CavLayerSel value for '[HOX] Heavy Oxide'."""
        return CavLayerSel('HOX_Heavy_Oxide', 0)

    @staticmethod
    def LOX_Light_Oxide():
        """Returns the CavLayerSel value for '[LOX] Light Oxide'."""
        return CavLayerSel('LOX_Light_Oxide', 1)

    @staticmethod
    def MET_Metal():
        """Returns the CavLayerSel value for '[MET] Metal'."""
        return CavLayerSel('MET_Metal', 2)

    @staticmethod
    def HMX_Heavy_Mixture():
        """Returns the CavLayerSel value for '[HMX] Heavy Mixture'."""
        return CavLayerSel('HMX_Heavy_Mixture', 3)

    @staticmethod
    def LMX_Light_Mixture():
        """Returns the CavLayerSel value for '[LMX] Light Mixture'."""
        return CavLayerSel('LMX_Light_Mixture', 4)


class CavRadModSel(object):
    """Enumeration of CavRadModSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CavRadModSel instance for a given integer value."""
        _MAP = {
            0: CavRadModSel.Tabular_Function(),
            1: CavRadModSel.Constant(),
        }
        return _MAP.get(v, CavRadModSel("unknown_{}".format(v), v))

    @staticmethod
    def Tabular_Function():
        """Returns the CavRadModSel value for 'Tabular Function'."""
        return CavRadModSel('Tabular_Function', 0)

    @staticmethod
    def Constant():
        """Returns the CavRadModSel value for 'Constant'."""
        return CavRadModSel('Constant', 1)


class CfClassSel(object):
    """Enumeration of CfClassSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CfClassSel instance for a given integer value."""
        _MAP = {
            0: CfClassSel.Normal(),
            1: CfClassSel.Latch(),
            2: CfClassSel.One_Shot(),
        }
        return _MAP.get(v, CfClassSel("unknown_{}".format(v), v))

    @staticmethod
    def Normal():
        """Returns the CfClassSel value for 'Normal'."""
        return CfClassSel('Normal', 0)

    @staticmethod
    def Latch():
        """Returns the CfClassSel value for 'Latch'."""
        return CfClassSel('Latch', 1)

    @staticmethod
    def One_Shot():
        """Returns the CfClassSel value for 'One-Shot'."""
        return CfClassSel('One_Shot', 2)


class CfCreepSel(object):
    """Enumeration of CfCreepSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CfCreepSel instance for a given integer value."""
        _MAP = {
            1: CfCreepSel.A_508_class_2_Carbon_Steel(),
            2: CfCreepSel.v_316_Stainless_Steel(),
            3: CfCreepSel.Inconel_600(),
            4: CfCreepSel.Default_COR_LH_Steel(),
            5: CfCreepSel.Default_COR_SS_Steel(),
            6: CfCreepSel.User_Defined(),
        }
        return _MAP.get(v, CfCreepSel("unknown_{}".format(v), v))

    @staticmethod
    def A_508_class_2_Carbon_Steel():
        """Returns the CfCreepSel value for 'A-508, class 2 Carbon Steel'."""
        return CfCreepSel('A_508_class_2_Carbon_Steel', 1)

    @staticmethod
    def v_316_Stainless_Steel():
        """Returns the CfCreepSel value for '316 Stainless Steel'."""
        return CfCreepSel('v_316_Stainless_Steel', 2)

    @staticmethod
    def Inconel_600():
        """Returns the CfCreepSel value for 'Inconel 600'."""
        return CfCreepSel('Inconel_600', 3)

    @staticmethod
    def Default_COR_LH_Steel():
        """Returns the CfCreepSel value for 'Default COR LH Steel'."""
        return CfCreepSel('Default_COR_LH_Steel', 4)

    @staticmethod
    def Default_COR_SS_Steel():
        """Returns the CfCreepSel value for 'Default COR SS Steel'."""
        return CfCreepSel('Default_COR_SS_Steel', 5)

    @staticmethod
    def User_Defined():
        """Returns the CfCreepSel value for 'User Defined'."""
        return CfCreepSel('User_Defined', 6)


class CmpndMassAddSel(object):
    """Enumeration of CmpndMassAddSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CmpndMassAddSel instance for a given integer value."""
        _MAP = {
            0: CmpndMassAddSel.Do_Not_Create_Classes(),
            1: CmpndMassAddSel.Specify_Classes(),
        }
        return _MAP.get(v, CmpndMassAddSel("unknown_{}".format(v), v))

    @staticmethod
    def Do_Not_Create_Classes():
        """Returns the CmpndMassAddSel value for 'Do Not Create Classes'."""
        return CmpndMassAddSel('Do_Not_Create_Classes', 0)

    @staticmethod
    def Specify_Classes():
        """Returns the CmpndMassAddSel value for 'Specify Classes'."""
        return CmpndMassAddSel('Specify_Classes', 1)


class CodeTypeSel(object):
    """Enumeration of CodeTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CodeTypeSel instance for a given integer value."""
        _MAP = {
            0: CodeTypeSel.MELGEN(),
            1: CodeTypeSel.MELCOR(),
        }
        return _MAP.get(v, CodeTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def MELGEN():
        """Returns the CodeTypeSel value for 'MELGEN'."""
        return CodeTypeSel('MELGEN', 0)

    @staticmethod
    def MELCOR():
        """Returns the CodeTypeSel value for 'MELCOR'."""
        return CodeTypeSel('MELCOR', 1)


class ConcreteSel(object):
    """Enumeration of ConcreteSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ConcreteSel instance for a given integer value."""
        _MAP = {
            1: ConcreteSel.CORCON_Basaltic(),
            2: ConcreteSel.CORCON_Limestone(),
            3: ConcreteSel.CORCON_Generic(),
            4: ConcreteSel.CORCON_Savannah(),
            5: ConcreteSel.Basalt(),
            6: ConcreteSel.Limestone(),
            7: ConcreteSel.Clinch_River(),
        }
        return _MAP.get(v, ConcreteSel("unknown_{}".format(v), v))

    @staticmethod
    def CORCON_Basaltic():
        """Returns the ConcreteSel value for 'CORCON Basaltic'."""
        return ConcreteSel('CORCON_Basaltic', 1)

    @staticmethod
    def CORCON_Limestone():
        """Returns the ConcreteSel value for 'CORCON Limestone'."""
        return ConcreteSel('CORCON_Limestone', 2)

    @staticmethod
    def CORCON_Generic():
        """Returns the ConcreteSel value for 'CORCON Generic'."""
        return ConcreteSel('CORCON_Generic', 3)

    @staticmethod
    def CORCON_Savannah():
        """Returns the ConcreteSel value for 'CORCON Savannah'."""
        return ConcreteSel('CORCON_Savannah', 4)

    @staticmethod
    def Basalt():
        """Returns the ConcreteSel value for 'Basalt'."""
        return ConcreteSel('Basalt', 5)

    @staticmethod
    def Limestone():
        """Returns the ConcreteSel value for 'Limestone'."""
        return ConcreteSel('Limestone', 6)

    @staticmethod
    def Clinch_River():
        """Returns the ConcreteSel value for 'Clinch River'."""
        return ConcreteSel('Clinch_River', 7)


class ConcreteTypeSel(object):
    """Enumeration of ConcreteTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ConcreteTypeSel instance for a given integer value."""
        _MAP = {
            1: ConcreteTypeSel.Nonstandard_concrete(),
            2: ConcreteTypeSel.Standard_concrete(),
        }
        return _MAP.get(v, ConcreteTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Nonstandard_concrete():
        """Returns the ConcreteTypeSel value for 'Nonstandard concrete'."""
        return ConcreteTypeSel('Nonstandard_concrete', 1)

    @staticmethod
    def Standard_concrete():
        """Returns the ConcreteTypeSel value for 'Standard concrete'."""
        return ConcreteTypeSel('Standard_concrete', 2)


class CondoxSel(object):
    """Enumeration of CondoxSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CondoxSel instance for a given integer value."""
        _MAP = {
            0: CondoxSel.Use_internal_model(),
            1: CondoxSel.Use_table_function(),
            2: CondoxSel.Constant_conductivity(),
            3: CondoxSel.Multiplier_on_conductivity(),
        }
        return _MAP.get(v, CondoxSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_internal_model():
        """Returns the CondoxSel value for 'Use internal model'."""
        return CondoxSel('Use_internal_model', 0)

    @staticmethod
    def Use_table_function():
        """Returns the CondoxSel value for 'Use table function'."""
        return CondoxSel('Use_table_function', 1)

    @staticmethod
    def Constant_conductivity():
        """Returns the CondoxSel value for 'Constant conductivity'."""
        return CondoxSel('Constant_conductivity', 2)

    @staticmethod
    def Multiplier_on_conductivity():
        """Returns the CondoxSel value for 'Multiplier on conductivity'."""
        return CondoxSel('Multiplier_on_conductivity', 3)


class ConstCFSel(object):
    """Enumeration of ConstCFSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ConstCFSel instance for a given integer value."""
        _MAP = {
            0: ConstCFSel.Constant(),
            1: ConstCFSel.Control_Function(),
        }
        return _MAP.get(v, ConstCFSel("unknown_{}".format(v), v))

    @staticmethod
    def Constant():
        """Returns the ConstCFSel value for 'Constant'."""
        return ConstCFSel('Constant', 0)

    @staticmethod
    def Control_Function():
        """Returns the ConstCFSel value for 'Control Function'."""
        return ConstCFSel('Control_Function', 1)


class ControlArcSel(object):
    """Enumeration of ControlArcSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ControlArcSel instance for a given integer value."""
        _MAP = {
            0: ControlArcSel.Use_data_from_tabular_function(),
            1: ControlArcSel.Use_data_from_control_function(),
            2: ControlArcSel.Use_data_from_external_data_file(),
        }
        return _MAP.get(v, ControlArcSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_data_from_tabular_function():
        """Returns the ControlArcSel value for 'Use data from tabular function.'."""
        return ControlArcSel('Use_data_from_tabular_function', 0)

    @staticmethod
    def Use_data_from_control_function():
        """Returns the ControlArcSel value for 'Use data from control function.'."""
        return ControlArcSel('Use_data_from_control_function', 1)

    @staticmethod
    def Use_data_from_external_data_file():
        """Returns the ControlArcSel value for 'Use data from external data file.'."""
        return ControlArcSel('Use_data_from_external_data_file', 2)


class ControlIntSel(object):
    """Enumeration of ControlIntSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ControlIntSel instance for a given integer value."""
        _MAP = {
            0: ControlIntSel.Control_Function_IFLAGS_Type(),
            1: ControlIntSel.Integer_IFLAGS_Type(),
        }
        return _MAP.get(v, ControlIntSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function_IFLAGS_Type():
        """Returns the ControlIntSel value for 'Control Function IFLAGS Type'."""
        return ControlIntSel('Control_Function_IFLAGS_Type', 0)

    @staticmethod
    def Integer_IFLAGS_Type():
        """Returns the ControlIntSel value for 'Integer IFLAGS Type'."""
        return ControlIntSel('Integer_IFLAGS_Type', 1)


class CorHtrmdlSel(object):
    """Enumeration of CorHtrmdlSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CorHtrmdlSel instance for a given integer value."""
        _MAP = {
            1: CorHtrmdlSel.Constant_Radiate(),
            2: CorHtrmdlSel.Constant_Conduct(),
            3: CorHtrmdlSel.Control_Radiate(),
            4: CorHtrmdlSel.Control_Conduct(),
        }
        return _MAP.get(v, CorHtrmdlSel("unknown_{}".format(v), v))

    @staticmethod
    def Constant_Radiate():
        """Returns the CorHtrmdlSel value for 'Constant Radiate'."""
        return CorHtrmdlSel('Constant_Radiate', 1)

    @staticmethod
    def Constant_Conduct():
        """Returns the CorHtrmdlSel value for 'Constant Conduct'."""
        return CorHtrmdlSel('Constant_Conduct', 2)

    @staticmethod
    def Control_Radiate():
        """Returns the CorHtrmdlSel value for 'Control Radiate'."""
        return CorHtrmdlSel('Control_Radiate', 3)

    @staticmethod
    def Control_Conduct():
        """Returns the CorHtrmdlSel value for 'Control Conduct'."""
        return CorHtrmdlSel('Control_Conduct', 4)


class CorOxAirSel(object):
    """Enumeration of CorOxAirSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CorOxAirSel instance for a given integer value."""
        _MAP = {
            0: CorOxAirSel.Hofmann_Birchley(),
            1: CorOxAirSel.Hayse_Roberson_Leistikov_Berg(),
            2: CorOxAirSel.Powers(),
            3: CorOxAirSel.MELCOR(),
            4: CorOxAirSel.Mozart(),
            -1: CorOxAirSel.Default(),
        }
        return _MAP.get(v, CorOxAirSel("unknown_{}".format(v), v))

    @staticmethod
    def Hofmann_Birchley():
        """Returns the CorOxAirSel value for 'Hofmann-Birchley'."""
        return CorOxAirSel('Hofmann_Birchley', 0)

    @staticmethod
    def Hayse_Roberson_Leistikov_Berg():
        """Returns the CorOxAirSel value for 'Hayse-Roberson/Leistikov-Berg'."""
        return CorOxAirSel('Hayse_Roberson_Leistikov_Berg', 1)

    @staticmethod
    def Powers():
        """Returns the CorOxAirSel value for 'Powers'."""
        return CorOxAirSel('Powers', 2)

    @staticmethod
    def MELCOR():
        """Returns the CorOxAirSel value for 'MELCOR'."""
        return CorOxAirSel('MELCOR', 3)

    @staticmethod
    def Mozart():
        """Returns the CorOxAirSel value for 'Mozart'."""
        return CorOxAirSel('Mozart', 4)

    @staticmethod
    def Default():
        """Returns the CorOxAirSel value for 'Default'."""
        return CorOxAirSel('Default', -1)


class CorOxNobrkSel(object):
    """Enumeration of CorOxNobrkSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CorOxNobrkSel instance for a given integer value."""
        _MAP = {
            0: CorOxNobrkSel.Enable_in_Steam_and_Air(),
            1: CorOxNobrkSel.Enable_in_Air(),
            2: CorOxNobrkSel.Disable_in_Steam_and_Air(),
        }
        return _MAP.get(v, CorOxNobrkSel("unknown_{}".format(v), v))

    @staticmethod
    def Enable_in_Steam_and_Air():
        """Returns the CorOxNobrkSel value for 'Enable in Steam and Air'."""
        return CorOxNobrkSel('Enable_in_Steam_and_Air', 0)

    @staticmethod
    def Enable_in_Air():
        """Returns the CorOxNobrkSel value for 'Enable in Air'."""
        return CorOxNobrkSel('Enable_in_Air', 1)

    @staticmethod
    def Disable_in_Steam_and_Air():
        """Returns the CorOxNobrkSel value for 'Disable in Steam and Air'."""
        return CorOxNobrkSel('Disable_in_Steam_and_Air', 2)


class CorOxOxygenSel(object):
    """Enumeration of CorOxOxygenSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CorOxOxygenSel instance for a given integer value."""
        _MAP = {
            0: CorOxOxygenSel.Uetsuka_Hofmann(),
            -1: CorOxOxygenSel.Default(),
        }
        return _MAP.get(v, CorOxOxygenSel("unknown_{}".format(v), v))

    @staticmethod
    def Uetsuka_Hofmann():
        """Returns the CorOxOxygenSel value for 'Uetsuka-Hofmann'."""
        return CorOxOxygenSel('Uetsuka_Hofmann', 0)

    @staticmethod
    def Default():
        """Returns the CorOxOxygenSel value for 'Default'."""
        return CorOxOxygenSel('Default', -1)


class CorOxSteamSel(object):
    """Enumeration of CorOxSteamSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CorOxSteamSel instance for a given integer value."""
        _MAP = {
            0: CorOxSteamSel.Cathcart(),
            1: CorOxSteamSel.Leistikov_Schanz_Prater_Courtright(),
            2: CorOxSteamSel.Leistikov(),
            3: CorOxSteamSel.Urbanic_Heidrick(),
            4: CorOxSteamSel.Sokolov(),
            -1: CorOxSteamSel.Default(),
        }
        return _MAP.get(v, CorOxSteamSel("unknown_{}".format(v), v))

    @staticmethod
    def Cathcart():
        """Returns the CorOxSteamSel value for 'Cathcart'."""
        return CorOxSteamSel('Cathcart', 0)

    @staticmethod
    def Leistikov_Schanz_Prater_Courtright():
        """Returns the CorOxSteamSel value for 'Leistikov-Schanz/Prater-Courtright'."""
        return CorOxSteamSel('Leistikov_Schanz_Prater_Courtright', 1)

    @staticmethod
    def Leistikov():
        """Returns the CorOxSteamSel value for 'Leistikov'."""
        return CorOxSteamSel('Leistikov', 2)

    @staticmethod
    def Urbanic_Heidrick():
        """Returns the CorOxSteamSel value for 'Urbanic-Heidrick'."""
        return CorOxSteamSel('Urbanic_Heidrick', 3)

    @staticmethod
    def Sokolov():
        """Returns the CorOxSteamSel value for 'Sokolov'."""
        return CorOxSteamSel('Sokolov', 4)

    @staticmethod
    def Default():
        """Returns the CorOxSteamSel value for 'Default'."""
        return CorOxSteamSel('Default', -1)


class CoreBCMODSel(object):
    """Enumeration of CoreBCMODSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreBCMODSel instance for a given integer value."""
        _MAP = {
            0: CoreBCMODSel.Blade(),
            1: CoreBCMODSel.Rod(),
        }
        return _MAP.get(v, CoreBCMODSel("unknown_{}".format(v), v))

    @staticmethod
    def Blade():
        """Returns the CoreBCMODSel value for 'Blade'."""
        return CoreBCMODSel('Blade', 0)

    @staticmethod
    def Rod():
        """Returns the CoreBCMODSel value for 'Rod'."""
        return CoreBCMODSel('Rod', 1)


class CoreBCSASel(object):
    """Enumeration of CoreBCSASel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreBCSASel instance for a given integer value."""
        _MAP = {
            0: CoreBCSASel.Simple(),
            1: CoreBCSASel.Advanced(),
        }
        return _MAP.get(v, CoreBCSASel("unknown_{}".format(v), v))

    @staticmethod
    def Simple():
        """Returns the CoreBCSASel value for 'Simple'."""
        return CoreBCSASel('Simple', 0)

    @staticmethod
    def Advanced():
        """Returns the CoreBCSASel value for 'Advanced'."""
        return CoreBCSASel('Advanced', 1)


class CoreDebrisCompSel(object):
    """Enumeration of CoreDebrisCompSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreDebrisCompSel instance for a given integer value."""
        _MAP = {
            2: CoreDebrisCompSel.Cladding(),
            3: CoreDebrisCompSel.Canister(),
            4: CoreDebrisCompSel.Canister_Adjacent_to_Blade(),
            6: CoreDebrisCompSel.Particulate_Debris(),
            7: CoreDebrisCompSel.Supporting_Structure(),
            8: CoreDebrisCompSel.Non_Supporting_Structure(),
            9: CoreDebrisCompSel.Bypass_Debris(),
        }
        return _MAP.get(v, CoreDebrisCompSel("unknown_{}".format(v), v))

    @staticmethod
    def Cladding():
        """Returns the CoreDebrisCompSel value for 'Cladding'."""
        return CoreDebrisCompSel('Cladding', 2)

    @staticmethod
    def Canister():
        """Returns the CoreDebrisCompSel value for 'Canister'."""
        return CoreDebrisCompSel('Canister', 3)

    @staticmethod
    def Canister_Adjacent_to_Blade():
        """Returns the CoreDebrisCompSel value for 'Canister Adjacent to Blade'."""
        return CoreDebrisCompSel('Canister_Adjacent_to_Blade', 4)

    @staticmethod
    def Particulate_Debris():
        """Returns the CoreDebrisCompSel value for 'Particulate Debris'."""
        return CoreDebrisCompSel('Particulate_Debris', 6)

    @staticmethod
    def Supporting_Structure():
        """Returns the CoreDebrisCompSel value for 'Supporting Structure'."""
        return CoreDebrisCompSel('Supporting_Structure', 7)

    @staticmethod
    def Non_Supporting_Structure():
        """Returns the CoreDebrisCompSel value for 'Non-Supporting Structure'."""
        return CoreDebrisCompSel('Non_Supporting_Structure', 8)

    @staticmethod
    def Bypass_Debris():
        """Returns the CoreDebrisCompSel value for 'Bypass Debris'."""
        return CoreDebrisCompSel('Bypass_Debris', 9)


class CoreHeatRcptSel(object):
    """Enumeration of CoreHeatRcptSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreHeatRcptSel instance for a given integer value."""
        _MAP = {
            1: CoreHeatRcptSel.FU(),
            2: CoreHeatRcptSel.CL(),
            3: CoreHeatRcptSel.CN(),
            4: CoreHeatRcptSel.SH(),
            5: CoreHeatRcptSel.CB(),
            6: CoreHeatRcptSel.FM(),
            7: CoreHeatRcptSel.PD(),
            8: CoreHeatRcptSel.SS(),
            9: CoreHeatRcptSel.NS(),
            10: CoreHeatRcptSel.PB(),
            11: CoreHeatRcptSel.MP1(),
            12: CoreHeatRcptSel.MB1(),
            13: CoreHeatRcptSel.MP2(),
            14: CoreHeatRcptSel.MB2(),
            16: CoreHeatRcptSel.HR(),
            17: CoreHeatRcptSel.RK(),
        }
        return _MAP.get(v, CoreHeatRcptSel("unknown_{}".format(v), v))

    @staticmethod
    def FU():
        """Returns the CoreHeatRcptSel value for 'FU'."""
        return CoreHeatRcptSel('FU', 1)

    @staticmethod
    def CL():
        """Returns the CoreHeatRcptSel value for 'CL'."""
        return CoreHeatRcptSel('CL', 2)

    @staticmethod
    def CN():
        """Returns the CoreHeatRcptSel value for 'CN'."""
        return CoreHeatRcptSel('CN', 3)

    @staticmethod
    def SH():
        """Returns the CoreHeatRcptSel value for 'SH'."""
        return CoreHeatRcptSel('SH', 4)

    @staticmethod
    def CB():
        """Returns the CoreHeatRcptSel value for 'CB'."""
        return CoreHeatRcptSel('CB', 5)

    @staticmethod
    def FM():
        """Returns the CoreHeatRcptSel value for 'FM'."""
        return CoreHeatRcptSel('FM', 6)

    @staticmethod
    def PD():
        """Returns the CoreHeatRcptSel value for 'PD'."""
        return CoreHeatRcptSel('PD', 7)

    @staticmethod
    def SS():
        """Returns the CoreHeatRcptSel value for 'SS'."""
        return CoreHeatRcptSel('SS', 8)

    @staticmethod
    def NS():
        """Returns the CoreHeatRcptSel value for 'NS'."""
        return CoreHeatRcptSel('NS', 9)

    @staticmethod
    def PB():
        """Returns the CoreHeatRcptSel value for 'PB'."""
        return CoreHeatRcptSel('PB', 10)

    @staticmethod
    def MP1():
        """Returns the CoreHeatRcptSel value for 'MP1'."""
        return CoreHeatRcptSel('MP1', 11)

    @staticmethod
    def MB1():
        """Returns the CoreHeatRcptSel value for 'MB1'."""
        return CoreHeatRcptSel('MB1', 12)

    @staticmethod
    def MP2():
        """Returns the CoreHeatRcptSel value for 'MP2'."""
        return CoreHeatRcptSel('MP2', 13)

    @staticmethod
    def MB2():
        """Returns the CoreHeatRcptSel value for 'MB2'."""
        return CoreHeatRcptSel('MB2', 14)

    @staticmethod
    def HR():
        """Returns the CoreHeatRcptSel value for 'HR'."""
        return CoreHeatRcptSel('HR', 16)

    @staticmethod
    def RK():
        """Returns the CoreHeatRcptSel value for 'RK'."""
        return CoreHeatRcptSel('RK', 17)


class CoreHeatTransFormatSel(object):
    """Enumeration of CoreHeatTransFormatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreHeatTransFormatSel instance for a given integer value."""
        _MAP = {
            0: CoreHeatTransFormatSel.Individual_Cells(),
            1: CoreHeatTransFormatSel.Control_Function_Range(),
        }
        return _MAP.get(v, CoreHeatTransFormatSel("unknown_{}".format(v), v))

    @staticmethod
    def Individual_Cells():
        """Returns the CoreHeatTransFormatSel value for 'Individual Cells'."""
        return CoreHeatTransFormatSel('Individual_Cells', 0)

    @staticmethod
    def Control_Function_Range():
        """Returns the CoreHeatTransFormatSel value for 'Control Function Range'."""
        return CoreHeatTransFormatSel('Control_Function_Range', 1)


class CoreIaiconSel(object):
    """Enumeration of CoreIaiconSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIaiconSel instance for a given integer value."""
        _MAP = {
            0: CoreIaiconSel.Model_Inactive(),
            1: CoreIaiconSel.Candling_and_Conglomerate(),
            2: CoreIaiconSel.Candling_Only(),
        }
        return _MAP.get(v, CoreIaiconSel("unknown_{}".format(v), v))

    @staticmethod
    def Model_Inactive():
        """Returns the CoreIaiconSel value for 'Model Inactive'."""
        return CoreIaiconSel('Model_Inactive', 0)

    @staticmethod
    def Candling_and_Conglomerate():
        """Returns the CoreIaiconSel value for 'Candling and Conglomerate'."""
        return CoreIaiconSel('Candling_and_Conglomerate', 1)

    @staticmethod
    def Candling_Only():
        """Returns the CoreIaiconSel value for 'Candling Only'."""
        return CoreIaiconSel('Candling_Only', 2)


class CoreIcffisSel(object):
    """Enumeration of CoreIcffisSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIcffisSel instance for a given integer value."""
        _MAP = {
            0: CoreIcffisSel.No_Fission_Power(),
            1: CoreIcffisSel.Chexal_Layman_Correlation(),
            -1: CoreIcffisSel.Whole_Core_Fission_Power(),
            100: CoreIcffisSel.Chexal_Layman_Only_Intact(),
            -100: CoreIcffisSel.While_Core_Power_Intact(),
        }
        return _MAP.get(v, CoreIcffisSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Fission_Power():
        """Returns the CoreIcffisSel value for 'No Fission Power'."""
        return CoreIcffisSel('No_Fission_Power', 0)

    @staticmethod
    def Chexal_Layman_Correlation():
        """Returns the CoreIcffisSel value for 'Chexal-Layman Correlation'."""
        return CoreIcffisSel('Chexal_Layman_Correlation', 1)

    @staticmethod
    def Whole_Core_Fission_Power():
        """Returns the CoreIcffisSel value for 'Whole Core Fission Power'."""
        return CoreIcffisSel('Whole_Core_Fission_Power', -1)

    @staticmethod
    def Chexal_Layman_Only_Intact():
        """Returns the CoreIcffisSel value for 'Chexal-Layman Only Intact'."""
        return CoreIcffisSel('Chexal_Layman_Only_Intact', 100)

    @staticmethod
    def While_Core_Power_Intact():
        """Returns the CoreIcffisSel value for 'While Core Power Intact'."""
        return CoreIcffisSel('While_Core_Power_Intact', -100)


class CoreIdrpSel(object):
    """Enumeration of CoreIdrpSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIdrpSel instance for a given integer value."""
        _MAP = {
            0: CoreIdrpSel.Enable(),
            1: CoreIdrpSel.Disable_All(),
            2: CoreIdrpSel.Disable_Holdup(),
        }
        return _MAP.get(v, CoreIdrpSel("unknown_{}".format(v), v))

    @staticmethod
    def Enable():
        """Returns the CoreIdrpSel value for 'Enable'."""
        return CoreIdrpSel('Enable', 0)

    @staticmethod
    def Disable_All():
        """Returns the CoreIdrpSel value for 'Disable All'."""
        return CoreIdrpSel('Disable_All', 1)

    @staticmethod
    def Disable_Holdup():
        """Returns the CoreIdrpSel value for 'Disable Holdup'."""
        return CoreIdrpSel('Disable_Holdup', 2)


class CoreIdtdzSel(object):
    """Enumeration of CoreIdtdzSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIdtdzSel instance for a given integer value."""
        _MAP = {
            0: CoreIdtdzSel.Obtain_from_Hydraulic(),
            1: CoreIdtdzSel.Calculate_Values(),
        }
        return _MAP.get(v, CoreIdtdzSel("unknown_{}".format(v), v))

    @staticmethod
    def Obtain_from_Hydraulic():
        """Returns the CoreIdtdzSel value for 'Obtain from Hydraulic'."""
        return CoreIdtdzSel('Obtain_from_Hydraulic', 0)

    @staticmethod
    def Calculate_Values():
        """Returns the CoreIdtdzSel value for 'Calculate Values'."""
        return CoreIdtdzSel('Calculate_Values', 1)


class CoreIgeomrfSel(object):
    """Enumeration of CoreIgeomrfSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIgeomrfSel instance for a given integer value."""
        _MAP = {
            0: CoreIgeomrfSel.Flat_Plate(),
            1: CoreIgeomrfSel.Cylindrical(),
        }
        return _MAP.get(v, CoreIgeomrfSel("unknown_{}".format(v), v))

    @staticmethod
    def Flat_Plate():
        """Returns the CoreIgeomrfSel value for 'Flat Plate'."""
        return CoreIgeomrfSel('Flat_Plate', 0)

    @staticmethod
    def Cylindrical():
        """Returns the CoreIgeomrfSel value for 'Cylindrical'."""
        return CoreIgeomrfSel('Cylindrical', 1)


class CoreIhsdtSel(object):
    """Enumeration of CoreIhsdtSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIhsdtSel instance for a given integer value."""
        _MAP = {
            0: CoreIhsdtSel.dT_dz_Required(),
            1: CoreIhsdtSel.dT_dz_Optional(),
        }
        return _MAP.get(v, CoreIhsdtSel("unknown_{}".format(v), v))

    @staticmethod
    def dT_dz_Required():
        """Returns the CoreIhsdtSel value for 'dT/dz Required'."""
        return CoreIhsdtSel('dT_dz_Required', 0)

    @staticmethod
    def dT_dz_Optional():
        """Returns the CoreIhsdtSel value for 'dT/dz Optional'."""
        return CoreIhsdtSel('dT_dz_Optional', 1)


class CoreIlhtrnSel(object):
    """Enumeration of CoreIlhtrnSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIlhtrnSel instance for a given integer value."""
        _MAP = {
            0: CoreIlhtrnSel.Transition_at_Core(),
            1: CoreIlhtrnSel.Transition_on_Vessel(),
        }
        return _MAP.get(v, CoreIlhtrnSel("unknown_{}".format(v), v))

    @staticmethod
    def Transition_at_Core():
        """Returns the CoreIlhtrnSel value for 'Transition at Core'."""
        return CoreIlhtrnSel('Transition_at_Core', 0)

    @staticmethod
    def Transition_on_Vessel():
        """Returns the CoreIlhtrnSel value for 'Transition on Vessel'."""
        return CoreIlhtrnSel('Transition_on_Vessel', 1)


class CoreIlhtypSel(object):
    """Enumeration of CoreIlhtypSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIlhtypSel instance for a given integer value."""
        _MAP = {
            0: CoreIlhtypSel.v_0_Hemisphere(),
            1: CoreIlhtypSel.v_1_Flat(),
            2: CoreIlhtypSel.Spheroid(),
        }
        return _MAP.get(v, CoreIlhtypSel("unknown_{}".format(v), v))

    @staticmethod
    def v_0_Hemisphere():
        """Returns the CoreIlhtypSel value for '[0] Hemisphere'."""
        return CoreIlhtypSel('v_0_Hemisphere', 0)

    @staticmethod
    def v_1_Flat():
        """Returns the CoreIlhtypSel value for '[1] Flat'."""
        return CoreIlhtypSel('v_1_Flat', 1)

    @staticmethod
    def Spheroid():
        """Returns the CoreIlhtypSel value for 'Spheroid'."""
        return CoreIlhtypSel('Spheroid', 2)


class CoreIoldosSel(object):
    """Enumeration of CoreIoldosSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIoldosSel instance for a given integer value."""
        _MAP = {
            0: CoreIoldosSel.Other_Structures_Disabled(),
            1: CoreIoldosSel.Other_Structures_Enabled(),
        }
        return _MAP.get(v, CoreIoldosSel("unknown_{}".format(v), v))

    @staticmethod
    def Other_Structures_Disabled():
        """Returns the CoreIoldosSel value for 'Other Structures Disabled'."""
        return CoreIoldosSel('Other_Structures_Disabled', 0)

    @staticmethod
    def Other_Structures_Enabled():
        """Returns the CoreIoldosSel value for 'Other Structures Enabled'."""
        return CoreIoldosSel('Other_Structures_Enabled', 1)


class CoreIoxbSel(object):
    """Enumeration of CoreIoxbSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIoxbSel instance for a given integer value."""
        _MAP = {
            0: CoreIoxbSel.Off(),
            1: CoreIoxbSel.Clad_and_Canister(),
            2: CoreIoxbSel.All_Zircaloy(),
        }
        return _MAP.get(v, CoreIoxbSel("unknown_{}".format(v), v))

    @staticmethod
    def Off():
        """Returns the CoreIoxbSel value for 'Off'."""
        return CoreIoxbSel('Off', 0)

    @staticmethod
    def Clad_and_Canister():
        """Returns the CoreIoxbSel value for 'Clad and Canister'."""
        return CoreIoxbSel('Clad_and_Canister', 1)

    @staticmethod
    def All_Zircaloy():
        """Returns the CoreIoxbSel value for 'All Zircaloy'."""
        return CoreIoxbSel('All_Zircaloy', 2)


class CoreIoxdSel(object):
    """Enumeration of CoreIoxdSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIoxdSel instance for a given integer value."""
        _MAP = {
            0: CoreIoxdSel.Hierarchical_Option(),
            1: CoreIoxdSel.No_Oxidation(),
            2: CoreIoxdSel.Intact_Hierarchical(),
            3: CoreIoxdSel.Simultaneous_Option(),
            4: CoreIoxdSel.Intact_Simultaneous(),
        }
        return _MAP.get(v, CoreIoxdSel("unknown_{}".format(v), v))

    @staticmethod
    def Hierarchical_Option():
        """Returns the CoreIoxdSel value for 'Hierarchical Option'."""
        return CoreIoxdSel('Hierarchical_Option', 0)

    @staticmethod
    def No_Oxidation():
        """Returns the CoreIoxdSel value for 'No Oxidation'."""
        return CoreIoxdSel('No_Oxidation', 1)

    @staticmethod
    def Intact_Hierarchical():
        """Returns the CoreIoxdSel value for 'Intact Hierarchical'."""
        return CoreIoxdSel('Intact_Hierarchical', 2)

    @staticmethod
    def Simultaneous_Option():
        """Returns the CoreIoxdSel value for 'Simultaneous Option'."""
        return CoreIoxdSel('Simultaneous_Option', 3)

    @staticmethod
    def Intact_Simultaneous():
        """Returns the CoreIoxdSel value for 'Intact Simultaneous'."""
        return CoreIoxdSel('Intact_Simultaneous', 4)


class CoreIsrpSel(object):
    """Enumeration of CoreIsrpSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIsrpSel instance for a given integer value."""
        _MAP = {
            0: CoreIsrpSel.Enable(),
            1: CoreIsrpSel.Disable_Molten(),
            2: CoreIsrpSel.Disable_Particulate(),
            3: CoreIsrpSel.Disable_All(),
        }
        return _MAP.get(v, CoreIsrpSel("unknown_{}".format(v), v))

    @staticmethod
    def Enable():
        """Returns the CoreIsrpSel value for 'Enable'."""
        return CoreIsrpSel('Enable', 0)

    @staticmethod
    def Disable_Molten():
        """Returns the CoreIsrpSel value for 'Disable Molten'."""
        return CoreIsrpSel('Disable_Molten', 1)

    @staticmethod
    def Disable_Particulate():
        """Returns the CoreIsrpSel value for 'Disable Particulate'."""
        return CoreIsrpSel('Disable_Particulate', 2)

    @staticmethod
    def Disable_All():
        """Returns the CoreIsrpSel value for 'Disable All'."""
        return CoreIsrpSel('Disable_All', 3)


class CoreIssfaiSel(object):
    """Enumeration of CoreIssfaiSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIssfaiSel instance for a given integer value."""
        _MAP = {
            0: CoreIssfaiSel.Fail_Temperature(),
            1: CoreIssfaiSel.Fail_Control(),
        }
        return _MAP.get(v, CoreIssfaiSel("unknown_{}".format(v), v))

    @staticmethod
    def Fail_Temperature():
        """Returns the CoreIssfaiSel value for 'Fail Temperature'."""
        return CoreIssfaiSel('Fail_Temperature', 0)

    @staticmethod
    def Fail_Control():
        """Returns the CoreIssfaiSel value for 'Fail Control'."""
        return CoreIssfaiSel('Fail_Control', 1)


class CoreIssmodSel(object):
    """Enumeration of CoreIssmodSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIssmodSel instance for a given integer value."""
        _MAP = {
            0: CoreIssmodSel.Plate(),
            1: CoreIssmodSel.Plate_G(),
            2: CoreIssmodSel.Plate_B(),
            3: CoreIssmodSel.Column(),
            4: CoreIssmodSel.Column_End(),
            10: CoreIssmodSel.User_Defined(),
        }
        return _MAP.get(v, CoreIssmodSel("unknown_{}".format(v), v))

    @staticmethod
    def Plate():
        """Returns the CoreIssmodSel value for 'Plate'."""
        return CoreIssmodSel('Plate', 0)

    @staticmethod
    def Plate_G():
        """Returns the CoreIssmodSel value for 'Plate G'."""
        return CoreIssmodSel('Plate_G', 1)

    @staticmethod
    def Plate_B():
        """Returns the CoreIssmodSel value for 'Plate B'."""
        return CoreIssmodSel('Plate_B', 2)

    @staticmethod
    def Column():
        """Returns the CoreIssmodSel value for 'Column'."""
        return CoreIssmodSel('Column', 3)

    @staticmethod
    def Column_End():
        """Returns the CoreIssmodSel value for 'Column End'."""
        return CoreIssmodSel('Column_End', 4)

    @staticmethod
    def User_Defined():
        """Returns the CoreIssmodSel value for 'User Defined'."""
        return CoreIssmodSel('User_Defined', 10)


class CoreIsupOnesSel(object):
    """Enumeration of CoreIsupOnesSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIsupOnesSel instance for a given integer value."""
        _MAP = {
            0: CoreIsupOnesSel.text(),
            1: CoreIsupOnesSel.text(),
        }
        return _MAP.get(v, CoreIsupOnesSel("unknown_{}".format(v), v))

    @staticmethod
    def text():
        """Returns the CoreIsupOnesSel value for 'text'."""
        return CoreIsupOnesSel('text', 0)

    @staticmethod
    def text():
        """Returns the CoreIsupOnesSel value for 'text'."""
        return CoreIsupOnesSel('text', 1)


class CoreIsupTenSel(object):
    """Enumeration of CoreIsupTenSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreIsupTenSel instance for a given integer value."""
        _MAP = {
            0: CoreIsupTenSel.Does_not_Support_Debris(),
            1: CoreIsupTenSel.Supports_Debris(),
        }
        return _MAP.get(v, CoreIsupTenSel("unknown_{}".format(v), v))

    @staticmethod
    def Does_not_Support_Debris():
        """Returns the CoreIsupTenSel value for 'Does not Support Debris'."""
        return CoreIsupTenSel('Does_not_Support_Debris', 0)

    @staticmethod
    def Supports_Debris():
        """Returns the CoreIsupTenSel value for 'Supports Debris'."""
        return CoreIsupTenSel('Supports_Debris', 1)


class CoreItupSel(object):
    """Enumeration of CoreItupSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreItupSel instance for a given integer value."""
        _MAP = {
            0: CoreItupSel.Use_Next_Volume(),
            1000: CoreItupSel.Disable_Model(),
            2000: CoreItupSel.Use_IDTDZ_Zero(),
            1: CoreItupSel.Reference_Volume(),
            -1: CoreItupSel.Control_Function(),
        }
        return _MAP.get(v, CoreItupSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_Next_Volume():
        """Returns the CoreItupSel value for 'Use Next Volume'."""
        return CoreItupSel('Use_Next_Volume', 0)

    @staticmethod
    def Disable_Model():
        """Returns the CoreItupSel value for 'Disable Model'."""
        return CoreItupSel('Disable_Model', 1000)

    @staticmethod
    def Use_IDTDZ_Zero():
        """Returns the CoreItupSel value for 'Use IDTDZ Zero'."""
        return CoreItupSel('Use_IDTDZ_Zero', 2000)

    @staticmethod
    def Reference_Volume():
        """Returns the CoreItupSel value for 'Reference Volume'."""
        return CoreItupSel('Reference_Volume', 1)

    @staticmethod
    def Control_Function():
        """Returns the CoreItupSel value for 'Control Function'."""
        return CoreItupSel('Control_Function', -1)


class CoreLevelSupSel(object):
    """Enumeration of CoreLevelSupSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreLevelSupSel instance for a given integer value."""
        _MAP = {
            0: CoreLevelSupSel.Formers(),
            1: CoreLevelSupSel.Fixed(),
        }
        return _MAP.get(v, CoreLevelSupSel("unknown_{}".format(v), v))

    @staticmethod
    def Formers():
        """Returns the CoreLevelSupSel value for 'Formers'."""
        return CoreLevelSupSel('Formers', 0)

    @staticmethod
    def Fixed():
        """Returns the CoreLevelSupSel value for 'Fixed'."""
        return CoreLevelSupSel('Fixed', 1)


class CoreMaterialSel(object):
    """Enumeration of CoreMaterialSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreMaterialSel instance for a given integer value."""
        _MAP = {
            0: CoreMaterialSel.Zircaloy(),
            1: CoreMaterialSel.Zirconium_Dioxide(),
            2: CoreMaterialSel.Steel(),
            3: CoreMaterialSel.Steel_Oxide(),
            4: CoreMaterialSel.Control_Poison(),
            5: CoreMaterialSel.Inconel(),
            6: CoreMaterialSel.Graphite(),
            7: CoreMaterialSel.Iron_Chromium_Aluminum(),
            8: CoreMaterialSel.Iron_Chromium_Aluminum_Oxide(),
        }
        return _MAP.get(v, CoreMaterialSel("unknown_{}".format(v), v))

    @staticmethod
    def Zircaloy():
        """Returns the CoreMaterialSel value for 'Zircaloy'."""
        return CoreMaterialSel('Zircaloy', 0)

    @staticmethod
    def Zirconium_Dioxide():
        """Returns the CoreMaterialSel value for 'Zirconium Dioxide'."""
        return CoreMaterialSel('Zirconium_Dioxide', 1)

    @staticmethod
    def Steel():
        """Returns the CoreMaterialSel value for 'Steel'."""
        return CoreMaterialSel('Steel', 2)

    @staticmethod
    def Steel_Oxide():
        """Returns the CoreMaterialSel value for 'Steel Oxide'."""
        return CoreMaterialSel('Steel_Oxide', 3)

    @staticmethod
    def Control_Poison():
        """Returns the CoreMaterialSel value for 'Control Poison'."""
        return CoreMaterialSel('Control_Poison', 4)

    @staticmethod
    def Inconel():
        """Returns the CoreMaterialSel value for 'Inconel'."""
        return CoreMaterialSel('Inconel', 5)

    @staticmethod
    def Graphite():
        """Returns the CoreMaterialSel value for 'Graphite'."""
        return CoreMaterialSel('Graphite', 6)

    @staticmethod
    def Iron_Chromium_Aluminum():
        """Returns the CoreMaterialSel value for 'Iron Chromium Aluminum'."""
        return CoreMaterialSel('Iron_Chromium_Aluminum', 7)

    @staticmethod
    def Iron_Chromium_Aluminum_Oxide():
        """Returns the CoreMaterialSel value for 'Iron Chromium Aluminum Oxide'."""
        return CoreMaterialSel('Iron_Chromium_Aluminum_Oxide', 8)


class CoreMcrpSel(object):
    """Enumeration of CoreMcrpSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreMcrpSel instance for a given integer value."""
        _MAP = {
            0: CoreMcrpSel.B4C(),
            1: CoreMcrpSel.AG_IN_CD(),
        }
        return _MAP.get(v, CoreMcrpSel("unknown_{}".format(v), v))

    @staticmethod
    def B4C():
        """Returns the CoreMcrpSel value for 'B4C'."""
        return CoreMcrpSel('B4C', 0)

    @staticmethod
    def AG_IN_CD():
        """Returns the CoreMcrpSel value for 'AG-IN-CD'."""
        return CoreMcrpSel('AG_IN_CD', 1)


class CoreMetalSel(object):
    """Enumeration of CoreMetalSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreMetalSel instance for a given integer value."""
        _MAP = {
            0: CoreMetalSel.Steel(),
            1: CoreMetalSel.Zircaloy(),
        }
        return _MAP.get(v, CoreMetalSel("unknown_{}".format(v), v))

    @staticmethod
    def Steel():
        """Returns the CoreMetalSel value for 'Steel'."""
        return CoreMetalSel('Steel', 0)

    @staticmethod
    def Zircaloy():
        """Returns the CoreMetalSel value for 'Zircaloy'."""
        return CoreMetalSel('Zircaloy', 1)


class CoreSignalCompSel(object):
    """Enumeration of CoreSignalCompSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreSignalCompSel instance for a given integer value."""
        _MAP = {
            0: CoreSignalCompSel.FU_Fuel_Component(),
            1: CoreSignalCompSel.CL_Cladding(),
            2: CoreSignalCompSel.CN_Canister(),
            3: CoreSignalCompSel.CB_Canister_Blade_Side(),
            5: CoreSignalCompSel.SS_Supporting(),
            6: CoreSignalCompSel.NS_Non_Supporting(),
            7: CoreSignalCompSel.SH_Shroud(),
            8: CoreSignalCompSel.FM_Former(),
            9: CoreSignalCompSel.PB_Bypass_Debris(),
            10: CoreSignalCompSel.PD_Particulate_Debris(),
            11: CoreSignalCompSel.MP1_Molten_Pool_1(),
            12: CoreSignalCompSel.MB1_Molten_Pool_1_in_Bypass(),
            13: CoreSignalCompSel.MP2_Molten_Pool_2(),
            14: CoreSignalCompSel.MB2_Molten_Pool_2_in_Bypass(),
            15: CoreSignalCompSel.SVC_Channel_Fluid_Temp(),
            16: CoreSignalCompSel.SVB_Bypass_Fluid_Temp(),
            17: CoreSignalCompSel.RK_Spent_Fuel_Pool_Rack(),
            18: CoreSignalCompSel.RF_Reflector(),
            19: CoreSignalCompSel.HR_Heavy_Reflector(),
        }
        return _MAP.get(v, CoreSignalCompSel("unknown_{}".format(v), v))

    @staticmethod
    def FU_Fuel_Component():
        """Returns the CoreSignalCompSel value for '[FU] Fuel Component'."""
        return CoreSignalCompSel('FU_Fuel_Component', 0)

    @staticmethod
    def CL_Cladding():
        """Returns the CoreSignalCompSel value for '[CL] Cladding'."""
        return CoreSignalCompSel('CL_Cladding', 1)

    @staticmethod
    def CN_Canister():
        """Returns the CoreSignalCompSel value for '[CN] Canister'."""
        return CoreSignalCompSel('CN_Canister', 2)

    @staticmethod
    def CB_Canister_Blade_Side():
        """Returns the CoreSignalCompSel value for '[CB] Canister Blade Side'."""
        return CoreSignalCompSel('CB_Canister_Blade_Side', 3)

    @staticmethod
    def SS_Supporting():
        """Returns the CoreSignalCompSel value for '[SS] Supporting'."""
        return CoreSignalCompSel('SS_Supporting', 5)

    @staticmethod
    def NS_Non_Supporting():
        """Returns the CoreSignalCompSel value for '[NS] Non-Supporting'."""
        return CoreSignalCompSel('NS_Non_Supporting', 6)

    @staticmethod
    def SH_Shroud():
        """Returns the CoreSignalCompSel value for '[SH] Shroud'."""
        return CoreSignalCompSel('SH_Shroud', 7)

    @staticmethod
    def FM_Former():
        """Returns the CoreSignalCompSel value for '[FM] Former'."""
        return CoreSignalCompSel('FM_Former', 8)

    @staticmethod
    def PB_Bypass_Debris():
        """Returns the CoreSignalCompSel value for '[PB] Bypass Debris'."""
        return CoreSignalCompSel('PB_Bypass_Debris', 9)

    @staticmethod
    def PD_Particulate_Debris():
        """Returns the CoreSignalCompSel value for '[PD] Particulate Debris'."""
        return CoreSignalCompSel('PD_Particulate_Debris', 10)

    @staticmethod
    def MP1_Molten_Pool_1():
        """Returns the CoreSignalCompSel value for '[MP1] Molten Pool 1'."""
        return CoreSignalCompSel('MP1_Molten_Pool_1', 11)

    @staticmethod
    def MB1_Molten_Pool_1_in_Bypass():
        """Returns the CoreSignalCompSel value for '[MB1] Molten Pool 1 in Bypass'."""
        return CoreSignalCompSel('MB1_Molten_Pool_1_in_Bypass', 12)

    @staticmethod
    def MP2_Molten_Pool_2():
        """Returns the CoreSignalCompSel value for '[MP2] Molten Pool 2'."""
        return CoreSignalCompSel('MP2_Molten_Pool_2', 13)

    @staticmethod
    def MB2_Molten_Pool_2_in_Bypass():
        """Returns the CoreSignalCompSel value for '[MB2] Molten Pool 2 in Bypass'."""
        return CoreSignalCompSel('MB2_Molten_Pool_2_in_Bypass', 14)

    @staticmethod
    def SVC_Channel_Fluid_Temp():
        """Returns the CoreSignalCompSel value for '[SVC] Channel Fluid Temp'."""
        return CoreSignalCompSel('SVC_Channel_Fluid_Temp', 15)

    @staticmethod
    def SVB_Bypass_Fluid_Temp():
        """Returns the CoreSignalCompSel value for '[SVB] Bypass Fluid Temp.'."""
        return CoreSignalCompSel('SVB_Bypass_Fluid_Temp', 16)

    @staticmethod
    def RK_Spent_Fuel_Pool_Rack():
        """Returns the CoreSignalCompSel value for '[RK] Spent Fuel Pool Rack'."""
        return CoreSignalCompSel('RK_Spent_Fuel_Pool_Rack', 17)

    @staticmethod
    def RF_Reflector():
        """Returns the CoreSignalCompSel value for '[RF] Reflector'."""
        return CoreSignalCompSel('RF_Reflector', 18)

    @staticmethod
    def HR_Heavy_Reflector():
        """Returns the CoreSignalCompSel value for '[HR] Heavy Reflector'."""
        return CoreSignalCompSel('HR_Heavy_Reflector', 19)


class CoreSignalMatSel(object):
    """Enumeration of CoreSignalMatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreSignalMatSel instance for a given integer value."""
        _MAP = {
            0: CoreSignalMatSel.MUO2_Uranium_Oxide(),
            1: CoreSignalMatSel.MZR_Zircaloy(),
            2: CoreSignalMatSel.MSS_Stainless_Steel(),
            3: CoreSignalMatSel.MINC_Inconel_Steel(),
            4: CoreSignalMatSel.MZRO2_Zirconium_Oixde(),
            5: CoreSignalMatSel.MSSOX_Steel_Oxide(),
            6: CoreSignalMatSel.MCRP_Control_Poison(),
            7: CoreSignalMatSel.USRM1_4_User_Material(),
        }
        return _MAP.get(v, CoreSignalMatSel("unknown_{}".format(v), v))

    @staticmethod
    def MUO2_Uranium_Oxide():
        """Returns the CoreSignalMatSel value for '[MUO2] Uranium Oxide'."""
        return CoreSignalMatSel('MUO2_Uranium_Oxide', 0)

    @staticmethod
    def MZR_Zircaloy():
        """Returns the CoreSignalMatSel value for '[MZR] Zircaloy'."""
        return CoreSignalMatSel('MZR_Zircaloy', 1)

    @staticmethod
    def MSS_Stainless_Steel():
        """Returns the CoreSignalMatSel value for '[MSS] Stainless Steel'."""
        return CoreSignalMatSel('MSS_Stainless_Steel', 2)

    @staticmethod
    def MINC_Inconel_Steel():
        """Returns the CoreSignalMatSel value for '[MINC] Inconel Steel'."""
        return CoreSignalMatSel('MINC_Inconel_Steel', 3)

    @staticmethod
    def MZRO2_Zirconium_Oixde():
        """Returns the CoreSignalMatSel value for '[MZRO2] Zirconium Oixde'."""
        return CoreSignalMatSel('MZRO2_Zirconium_Oixde', 4)

    @staticmethod
    def MSSOX_Steel_Oxide():
        """Returns the CoreSignalMatSel value for '[MSSOX] Steel Oxide'."""
        return CoreSignalMatSel('MSSOX_Steel_Oxide', 5)

    @staticmethod
    def MCRP_Control_Poison():
        """Returns the CoreSignalMatSel value for '[MCRP] Control Poison'."""
        return CoreSignalMatSel('MCRP_Control_Poison', 6)

    @staticmethod
    def USRM1_4_User_Material():
        """Returns the CoreSignalMatSel value for '[USRM1-4] User Material'."""
        return CoreSignalMatSel('USRM1_4_User_Material', 7)


class CoreTmechSel(object):
    """Enumeration of CoreTmechSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CoreTmechSel instance for a given integer value."""
        _MAP = {
            1: CoreTmechSel.Molten_Mass(),
            2: CoreTmechSel.Existing_Mass(),
        }
        return _MAP.get(v, CoreTmechSel("unknown_{}".format(v), v))

    @staticmethod
    def Molten_Mass():
        """Returns the CoreTmechSel value for 'Molten Mass'."""
        return CoreTmechSel('Molten_Mass', 1)

    @staticmethod
    def Existing_Mass():
        """Returns the CoreTmechSel value for 'Existing Mass'."""
        return CoreTmechSel('Existing_Mass', 2)


class CourantCondSel(object):
    """Enumeration of CourantCondSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CourantCondSel instance for a given integer value."""
        _MAP = {
            0: CourantCondSel.Volumes_with_Mass_Sources(),
            1: CourantCondSel.Volumes_sans_Mass_Sources_RCS(),
        }
        return _MAP.get(v, CourantCondSel("unknown_{}".format(v), v))

    @staticmethod
    def Volumes_with_Mass_Sources():
        """Returns the CourantCondSel value for 'Volumes with Mass Sources'."""
        return CourantCondSel('Volumes_with_Mass_Sources', 0)

    @staticmethod
    def Volumes_sans_Mass_Sources_RCS():
        """Returns the CourantCondSel value for 'Volumes sans Mass Sources (RCS)'."""
        return CourantCondSel('Volumes_sans_Mass_Sources_RCS', 1)


class CreepSel(object):
    """Enumeration of CreepSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the CreepSel instance for a given integer value."""
        _MAP = {
            1: CreepSel.A_508_class_2_carbon_steel(),
            2: CreepSel.v_316_stainless_steel(),
            3: CreepSel.Inconel_600(),
            4: CreepSel.Default_COR_LH_Steel_SA533B1(),
            5: CreepSel.Default_COR_SS_Steel_SC1604(),
            6: CreepSel.User_Defined(),
        }
        return _MAP.get(v, CreepSel("unknown_{}".format(v), v))

    @staticmethod
    def A_508_class_2_carbon_steel():
        """Returns the CreepSel value for 'A-508, class 2 carbon steel'."""
        return CreepSel('A_508_class_2_carbon_steel', 1)

    @staticmethod
    def v_316_stainless_steel():
        """Returns the CreepSel value for '316 stainless steel'."""
        return CreepSel('v_316_stainless_steel', 2)

    @staticmethod
    def Inconel_600():
        """Returns the CreepSel value for 'Inconel 600'."""
        return CreepSel('Inconel_600', 3)

    @staticmethod
    def Default_COR_LH_Steel_SA533B1():
        """Returns the CreepSel value for 'Default COR LH Steel (SA533B1)'."""
        return CreepSel('Default_COR_LH_Steel_SA533B1', 4)

    @staticmethod
    def Default_COR_SS_Steel_SC1604():
        """Returns the CreepSel value for 'Default COR SS Steel (SC1604)'."""
        return CreepSel('Default_COR_SS_Steel_SC1604', 5)

    @staticmethod
    def User_Defined():
        """Returns the CreepSel value for 'User Defined'."""
        return CreepSel('User_Defined', 6)


class DBPhaseSel(object):
    """Enumeration of DBPhaseSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DBPhaseSel instance for a given integer value."""
        _MAP = {
            0: DBPhaseSel.Atmosphere(),
            1: DBPhaseSel.Pool(),
        }
        return _MAP.get(v, DBPhaseSel("unknown_{}".format(v), v))

    @staticmethod
    def Atmosphere():
        """Returns the DBPhaseSel value for 'Atmosphere'."""
        return DBPhaseSel('Atmosphere', 0)

    @staticmethod
    def Pool():
        """Returns the DBPhaseSel value for 'Pool'."""
        return DBPhaseSel('Pool', 1)


class DISOptSel(object):
    """Enumeration of DISOptSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DISOptSel instance for a given integer value."""
        _MAP = {
            0: DISOptSel.YES(),
            1: DISOptSel.NO(),
        }
        return _MAP.get(v, DISOptSel("unknown_{}".format(v), v))

    @staticmethod
    def YES():
        """Returns the DISOptSel value for 'YES'."""
        return DISOptSel('YES', 0)

    @staticmethod
    def NO():
        """Returns the DISOptSel value for 'NO'."""
        return DISOptSel('NO', 1)


class DecayHeatSel(object):
    """Enumeration of DecayHeatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DecayHeatSel instance for a given integer value."""
        _MAP = {
            -2: DecayHeatSel.Zero_Decay_Heat(),
            -1: DecayHeatSel.Calculated_Decay_Heat(),
            0: DecayHeatSel.Control_Function(),
        }
        return _MAP.get(v, DecayHeatSel("unknown_{}".format(v), v))

    @staticmethod
    def Zero_Decay_Heat():
        """Returns the DecayHeatSel value for 'Zero Decay Heat'."""
        return DecayHeatSel('Zero_Decay_Heat', -2)

    @staticmethod
    def Calculated_Decay_Heat():
        """Returns the DecayHeatSel value for 'Calculated Decay Heat'."""
        return DecayHeatSel('Calculated_Decay_Heat', -1)

    @staticmethod
    def Control_Function():
        """Returns the DecayHeatSel value for 'Control Function'."""
        return DecayHeatSel('Control_Function', 0)


class DecayTypeSel(object):
    """Enumeration of DecayTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DecayTypeSel instance for a given integer value."""
        _MAP = {
            1: DecayTypeSel.ORIGEN(),
            2: DecayTypeSel.ANS(),
            3: DecayTypeSel.Control_Function(),
            4: DecayTypeSel.Tabular_Function(),
        }
        return _MAP.get(v, DecayTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def ORIGEN():
        """Returns the DecayTypeSel value for 'ORIGEN'."""
        return DecayTypeSel('ORIGEN', 1)

    @staticmethod
    def ANS():
        """Returns the DecayTypeSel value for 'ANS'."""
        return DecayTypeSel('ANS', 2)

    @staticmethod
    def Control_Function():
        """Returns the DecayTypeSel value for 'Control Function'."""
        return DecayTypeSel('Control_Function', 3)

    @staticmethod
    def Tabular_Function():
        """Returns the DecayTypeSel value for 'Tabular Function'."""
        return DecayTypeSel('Tabular_Function', 4)


class DecontamFactSel(object):
    """Enumeration of DecontamFactSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DecontamFactSel instance for a given integer value."""
        _MAP = {
            0: DecontamFactSel.MACCS(),
            1: DecontamFactSel.DF(),
        }
        return _MAP.get(v, DecontamFactSel("unknown_{}".format(v), v))

    @staticmethod
    def MACCS():
        """Returns the DecontamFactSel value for 'MACCS'."""
        return DecontamFactSel('MACCS', 0)

    @staticmethod
    def DF():
        """Returns the DecontamFactSel value for 'DF'."""
        return DecontamFactSel('DF', 1)


class DefaultSel(object):
    """Enumeration of DefaultSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DefaultSel instance for a given integer value."""
        _MAP = {
            186: DefaultSel.v_1_8_6_Standards(),
            20: DefaultSel.v_2_x_Standards(),
        }
        return _MAP.get(v, DefaultSel("unknown_{}".format(v), v))

    @staticmethod
    def v_1_8_6_Standards():
        """Returns the DefaultSel value for '1.8.6 Standards'."""
        return DefaultSel('v_1_8_6_Standards', 186)

    @staticmethod
    def v_2_x_Standards():
        """Returns the DefaultSel value for '2.x Standards'."""
        return DefaultSel('v_2_x_Standards', 20)


class DirflSel(object):
    """Enumeration of DirflSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the DirflSel instance for a given integer value."""
        _MAP = {
            0: DirflSel.From(),
            1: DirflSel.To(),
        }
        return _MAP.get(v, DirflSel("unknown_{}".format(v), v))

    @staticmethod
    def From():
        """Returns the DirflSel value for 'From'."""
        return DirflSel('From', 0)

    @staticmethod
    def To():
        """Returns the DirflSel value for 'To'."""
        return DirflSel('To', 1)


class EdfModeSel(object):
    """Enumeration of EdfModeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the EdfModeSel instance for a given integer value."""
        _MAP = {
            0: EdfModeSel.Read(),
            1: EdfModeSel.Write(),
            2: EdfModeSel.Push(),
        }
        return _MAP.get(v, EdfModeSel("unknown_{}".format(v), v))

    @staticmethod
    def Read():
        """Returns the EdfModeSel value for 'Read'."""
        return EdfModeSel('Read', 0)

    @staticmethod
    def Write():
        """Returns the EdfModeSel value for 'Write'."""
        return EdfModeSel('Write', 1)

    @staticmethod
    def Push():
        """Returns the EdfModeSel value for 'Push'."""
        return EdfModeSel('Push', 2)


class EnableSel(object):
    """Enumeration of EnableSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the EnableSel instance for a given integer value."""
        _MAP = {
            0: EnableSel.Enable(),
            1: EnableSel.Disable(),
        }
        return _MAP.get(v, EnableSel("unknown_{}".format(v), v))

    @staticmethod
    def Enable():
        """Returns the EnableSel value for 'Enable'."""
        return EnableSel('Enable', 0)

    @staticmethod
    def Disable():
        """Returns the EnableSel value for 'Disable'."""
        return EnableSel('Disable', 1)


class ExCoefSel(object):
    """Enumeration of ExCoefSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ExCoefSel instance for a given integer value."""
        _MAP = {
            1: ExCoefSel.Adiabatic(),
            2: ExCoefSel.Isothermal(),
            3: ExCoefSel.User_Defined(),
        }
        return _MAP.get(v, ExCoefSel("unknown_{}".format(v), v))

    @staticmethod
    def Adiabatic():
        """Returns the ExCoefSel value for 'Adiabatic'."""
        return ExCoefSel('Adiabatic', 1)

    @staticmethod
    def Isothermal():
        """Returns the ExCoefSel value for 'Isothermal'."""
        return ExCoefSel('Isothermal', 2)

    @staticmethod
    def User_Defined():
        """Returns the ExCoefSel value for 'User-Defined'."""
        return ExCoefSel('User_Defined', 3)


class ExchTypeSel(object):
    """Enumeration of ExchTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ExchTypeSel instance for a given integer value."""
        _MAP = {
            0: ExchTypeSel.Counterflow(),
            1: ExchTypeSel.Parallel(),
        }
        return _MAP.get(v, ExchTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Counterflow():
        """Returns the ExchTypeSel value for 'Counterflow'."""
        return ExchTypeSel('Counterflow', 0)

    @staticmethod
    def Parallel():
        """Returns the ExchTypeSel value for 'Parallel'."""
        return ExchTypeSel('Parallel', 1)


class ExternalSourceSel(object):
    """Enumeration of ExternalSourceSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ExternalSourceSel instance for a given integer value."""
        _MAP = {
            0: ExternalSourceSel.Original_format(),
            1: ExternalSourceSel.New_format(),
        }
        return _MAP.get(v, ExternalSourceSel("unknown_{}".format(v), v))

    @staticmethod
    def Original_format():
        """Returns the ExternalSourceSel value for 'Original format'."""
        return ExternalSourceSel('Original_format', 0)

    @staticmethod
    def New_format():
        """Returns the ExternalSourceSel value for 'New format'."""
        return ExternalSourceSel('New_format', 1)


class FCModelSel(object):
    """Enumeration of FCModelSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FCModelSel instance for a given integer value."""
        _MAP = {
            0: FCModelSel.CONTAIN(),
            1: FCModelSel.MARCH(),
        }
        return _MAP.get(v, FCModelSel("unknown_{}".format(v), v))

    @staticmethod
    def CONTAIN():
        """Returns the FCModelSel value for 'CONTAIN'."""
        return FCModelSel('CONTAIN', 0)

    @staticmethod
    def MARCH():
        """Returns the FCModelSel value for 'MARCH'."""
        return FCModelSel('MARCH', 1)


class FDIDebrsrcSel(object):
    """Enumeration of FDIDebrsrcSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FDIDebrsrcSel instance for a given integer value."""
        _MAP = {
            -1: FDIDebrsrcSel.Transfer_Process(),
            1: FDIDebrsrcSel.Tabular_Function(),
        }
        return _MAP.get(v, FDIDebrsrcSel("unknown_{}".format(v), v))

    @staticmethod
    def Transfer_Process():
        """Returns the FDIDebrsrcSel value for 'Transfer Process'."""
        return FDIDebrsrcSel('Transfer_Process', -1)

    @staticmethod
    def Tabular_Function():
        """Returns the FDIDebrsrcSel value for 'Tabular Function'."""
        return FDIDebrsrcSel('Tabular_Function', 1)


class FLIbubSel(object):
    """Enumeration of FLIbubSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLIbubSel instance for a given integer value."""
        _MAP = {
            0: FLIbubSel.No_Bubble_Rise(),
            1: FLIbubSel.Aerosol_and_Iodine_Scrubbing(),
            2: FLIbubSel.All_Scrubbing(),
            -1: FLIbubSel.No_Scrubbing(),
            -2: FLIbubSel.Aerosol_Scrubbing(),
            -3: FLIbubSel.Iodine_Vapor_Scrubbing(),
        }
        return _MAP.get(v, FLIbubSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Bubble_Rise():
        """Returns the FLIbubSel value for 'No Bubble Rise'."""
        return FLIbubSel('No_Bubble_Rise', 0)

    @staticmethod
    def Aerosol_and_Iodine_Scrubbing():
        """Returns the FLIbubSel value for 'Aerosol and Iodine Scrubbing'."""
        return FLIbubSel('Aerosol_and_Iodine_Scrubbing', 1)

    @staticmethod
    def All_Scrubbing():
        """Returns the FLIbubSel value for 'All Scrubbing'."""
        return FLIbubSel('All_Scrubbing', 2)

    @staticmethod
    def No_Scrubbing():
        """Returns the FLIbubSel value for 'No Scrubbing'."""
        return FLIbubSel('No_Scrubbing', -1)

    @staticmethod
    def Aerosol_Scrubbing():
        """Returns the FLIbubSel value for 'Aerosol Scrubbing'."""
        return FLIbubSel('Aerosol_Scrubbing', -2)

    @staticmethod
    def Iodine_Vapor_Scrubbing():
        """Returns the FLIbubSel value for 'Iodine Vapor Scrubbing'."""
        return FLIbubSel('Iodine_Vapor_Scrubbing', -3)


class FLKactflSel(object):
    """Enumeration of FLKactflSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLKactflSel instance for a given integer value."""
        _MAP = {
            0: FLKactflSel.Active(),
            1: FLKactflSel.Inactive_Do_Not_Use(),
        }
        return _MAP.get(v, FLKactflSel("unknown_{}".format(v), v))

    @staticmethod
    def Active():
        """Returns the FLKactflSel value for 'Active'."""
        return FLKactflSel('Active', 0)

    @staticmethod
    def Inactive_Do_Not_Use():
        """Returns the FLKactflSel value for 'Inactive (Do Not Use)'."""
        return FLKactflSel('Inactive_Do_Not_Use', 1)


class FLKflgModeSel(object):
    """Enumeration of FLKflgModeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLKflgModeSel instance for a given integer value."""
        _MAP = {
            0: FLKflgModeSel.Both_Flows(),
            1: FLKflgModeSel.Forward_Only(),
            2: FLKflgModeSel.Reverse_Only(),
        }
        return _MAP.get(v, FLKflgModeSel("unknown_{}".format(v), v))

    @staticmethod
    def Both_Flows():
        """Returns the FLKflgModeSel value for 'Both Flows'."""
        return FLKflgModeSel('Both_Flows', 0)

    @staticmethod
    def Forward_Only():
        """Returns the FLKflgModeSel value for 'Forward Only'."""
        return FLKflgModeSel('Forward_Only', 1)

    @staticmethod
    def Reverse_Only():
        """Returns the FLKflgModeSel value for 'Reverse Only'."""
        return FLKflgModeSel('Reverse_Only', 2)


class FLKflgflSel(object):
    """Enumeration of FLKflgflSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLKflgflSel instance for a given integer value."""
        _MAP = {
            0: FLKflgflSel.Normal_Vertical_Path(),
            1: FLKflgflSel.Atmosphere_first_Vertical_Path(),
            2: FLKflgflSel.Pool_first_Vertical_Path(),
            3: FLKflgflSel.Normal_Horizontal_Path(),
            4: FLKflgflSel.Atmosphere_First_Horiz_Path(),
            5: FLKflgflSel.Pool_first_Horizontal_Path(),
            6: FLKflgflSel.Equal_Vertical_Flow(),
            7: FLKflgflSel.Equal_Horizontal_Flow(),
        }
        return _MAP.get(v, FLKflgflSel("unknown_{}".format(v), v))

    @staticmethod
    def Normal_Vertical_Path():
        """Returns the FLKflgflSel value for 'Normal Vertical Path'."""
        return FLKflgflSel('Normal_Vertical_Path', 0)

    @staticmethod
    def Atmosphere_first_Vertical_Path():
        """Returns the FLKflgflSel value for 'Atmosphere-first Vertical Path'."""
        return FLKflgflSel('Atmosphere_first_Vertical_Path', 1)

    @staticmethod
    def Pool_first_Vertical_Path():
        """Returns the FLKflgflSel value for 'Pool-first Vertical Path'."""
        return FLKflgflSel('Pool_first_Vertical_Path', 2)

    @staticmethod
    def Normal_Horizontal_Path():
        """Returns the FLKflgflSel value for 'Normal Horizontal Path'."""
        return FLKflgflSel('Normal_Horizontal_Path', 3)

    @staticmethod
    def Atmosphere_First_Horiz_Path():
        """Returns the FLKflgflSel value for 'Atmosphere-First Horiz. Path'."""
        return FLKflgflSel('Atmosphere_First_Horiz_Path', 4)

    @staticmethod
    def Pool_first_Horizontal_Path():
        """Returns the FLKflgflSel value for 'Pool-first Horizontal Path'."""
        return FLKflgflSel('Pool_first_Horizontal_Path', 5)

    @staticmethod
    def Equal_Vertical_Flow():
        """Returns the FLKflgflSel value for 'Equal Vertical Flow'."""
        return FLKflgflSel('Equal_Vertical_Flow', 6)

    @staticmethod
    def Equal_Horizontal_Flow():
        """Returns the FLKflgflSel value for 'Equal Horizontal Flow'."""
        return FLKflgflSel('Equal_Horizontal_Flow', 7)


class FLKflshSel(object):
    """Enumeration of FLKflshSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLKflshSel instance for a given integer value."""
        _MAP = {
            0: FLKflshSel.No_Flashing_Calculation(),
            1: FLKflshSel.Flashing_Model_Activated(),
        }
        return _MAP.get(v, FLKflshSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Flashing_Calculation():
        """Returns the FLKflshSel value for 'No Flashing Calculation'."""
        return FLKflshSel('No_Flashing_Calculation', 0)

    @staticmethod
    def Flashing_Model_Activated():
        """Returns the FLKflshSel value for 'Flashing Model Activated'."""
        return FLKflshSel('Flashing_Model_Activated', 1)


class FLMaccsFlowSel(object):
    """Enumeration of FLMaccsFlowSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLMaccsFlowSel instance for a given integer value."""
        _MAP = {
            0: FLMaccsFlowSel.Forward(),
            1: FLMaccsFlowSel.Reverse(),
        }
        return _MAP.get(v, FLMaccsFlowSel("unknown_{}".format(v), v))

    @staticmethod
    def Forward():
        """Returns the FLMaccsFlowSel value for 'Forward'."""
        return FLMaccsFlowSel('Forward', 0)

    @staticmethod
    def Reverse():
        """Returns the FLMaccsFlowSel value for 'Reverse'."""
        return FLMaccsFlowSel('Reverse', 1)


class FLNtflagSel(object):
    """Enumeration of FLNtflagSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FLNtflagSel instance for a given integer value."""
        _MAP = {
            1: FLNtflagSel.Tabular_Function(),
            2: FLNtflagSel.Control_Function(),
        }
        return _MAP.get(v, FLNtflagSel("unknown_{}".format(v), v))

    @staticmethod
    def Tabular_Function():
        """Returns the FLNtflagSel value for 'Tabular Function'."""
        return FLNtflagSel('Tabular_Function', 1)

    @staticmethod
    def Control_Function():
        """Returns the FLNtflagSel value for 'Control Function'."""
        return FLNtflagSel('Control_Function', 2)


class FilterCtypeSel(object):
    """Enumeration of FilterCtypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FilterCtypeSel instance for a given integer value."""
        _MAP = {
            0: FilterCtypeSel.Aerosol(),
            1: FilterCtypeSel.Fission_Product(),
        }
        return _MAP.get(v, FilterCtypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Aerosol():
        """Returns the FilterCtypeSel value for 'Aerosol'."""
        return FilterCtypeSel('Aerosol', 0)

    @staticmethod
    def Fission_Product():
        """Returns the FilterCtypeSel value for 'Fission Product'."""
        return FilterCtypeSel('Fission_Product', 1)


class FilterIrdcofSel(object):
    """Enumeration of FilterIrdcofSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FilterIrdcofSel instance for a given integer value."""
        _MAP = {
            0: FilterIrdcofSel.No_Desorption(),
            -2: FilterIrdcofSel.Use_Room_Correlation(),
            1: FilterIrdcofSel.Use_Tabular_Function(),
        }
        return _MAP.get(v, FilterIrdcofSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Desorption():
        """Returns the FilterIrdcofSel value for 'No Desorption'."""
        return FilterIrdcofSel('No_Desorption', 0)

    @staticmethod
    def Use_Room_Correlation():
        """Returns the FilterIrdcofSel value for 'Use Room Correlation'."""
        return FilterIrdcofSel('Use_Room_Correlation', -2)

    @staticmethod
    def Use_Tabular_Function():
        """Returns the FilterIrdcofSel value for 'Use Tabular Function'."""
        return FilterIrdcofSel('Use_Tabular_Function', 1)


class FilterIthcofSel(object):
    """Enumeration of FilterIthcofSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FilterIthcofSel instance for a given integer value."""
        _MAP = {
            0: FilterIthcofSel.No_Desorption(),
            -1: FilterIthcofSel.FISH6_Correlation(),
            -2: FilterIthcofSel.ROOM_Correlation(),
            1: FilterIthcofSel.Use_Tabular_Function(),
        }
        return _MAP.get(v, FilterIthcofSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Desorption():
        """Returns the FilterIthcofSel value for 'No Desorption'."""
        return FilterIthcofSel('No_Desorption', 0)

    @staticmethod
    def FISH6_Correlation():
        """Returns the FilterIthcofSel value for 'FISH6 Correlation'."""
        return FilterIthcofSel('FISH6_Correlation', -1)

    @staticmethod
    def ROOM_Correlation():
        """Returns the FilterIthcofSel value for 'ROOM Correlation'."""
        return FilterIthcofSel('ROOM_Correlation', -2)

    @staticmethod
    def Use_Tabular_Function():
        """Returns the FilterIthcofSel value for 'Use Tabular Function'."""
        return FilterIthcofSel('Use_Tabular_Function', 1)


class FlStateSel(object):
    """Enumeration of FlStateSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FlStateSel instance for a given integer value."""
        _MAP = {
            0: FlStateSel.Saturated(),
            1: FlStateSel.Subcooled(),
        }
        return _MAP.get(v, FlStateSel("unknown_{}".format(v), v))

    @staticmethod
    def Saturated():
        """Returns the FlStateSel value for 'Saturated'."""
        return FlStateSel('Saturated', 0)

    @staticmethod
    def Subcooled():
        """Returns the FlStateSel value for 'Subcooled'."""
        return FlStateSel('Subcooled', 1)


class FlowCalcSel(object):
    """Enumeration of FlowCalcSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FlowCalcSel instance for a given integer value."""
        _MAP = {
            0: FlowCalcSel.Calulate_Convection(),
            1: FlowCalcSel.Input_Convection(),
        }
        return _MAP.get(v, FlowCalcSel("unknown_{}".format(v), v))

    @staticmethod
    def Calulate_Convection():
        """Returns the FlowCalcSel value for 'Calulate Convection'."""
        return FlowCalcSel('Calulate_Convection', 0)

    @staticmethod
    def Input_Convection():
        """Returns the FlowCalcSel value for 'Input Convection'."""
        return FlowCalcSel('Input_Convection', 1)


class FogOptionSel(object):
    """Enumeration of FogOptionSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FogOptionSel instance for a given integer value."""
        _MAP = {
            0: FogOptionSel.Direct_Section_Distribution(),
            1: FogOptionSel.RN_Calculated_Distribution(),
        }
        return _MAP.get(v, FogOptionSel("unknown_{}".format(v), v))

    @staticmethod
    def Direct_Section_Distribution():
        """Returns the FogOptionSel value for 'Direct Section Distribution'."""
        return FogOptionSel('Direct_Section_Distribution', 0)

    @staticmethod
    def RN_Calculated_Distribution():
        """Returns the FogOptionSel value for 'RN Calculated Distribution'."""
        return FogOptionSel('RN_Calculated_Distribution', 1)


class FormulaFlagSel(object):
    """Enumeration of FormulaFlagSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FormulaFlagSel instance for a given integer value."""
        _MAP = {
            0: FormulaFlagSel.Connection(),
            1: FormulaFlagSel.Constant(),
        }
        return _MAP.get(v, FormulaFlagSel("unknown_{}".format(v), v))

    @staticmethod
    def Connection():
        """Returns the FormulaFlagSel value for 'Connection'."""
        return FormulaFlagSel('Connection', 0)

    @staticmethod
    def Constant():
        """Returns the FormulaFlagSel value for 'Constant'."""
        return FormulaFlagSel('Constant', 1)


class FricCoefSel(object):
    """Enumeration of FricCoefSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the FricCoefSel instance for a given integer value."""
        _MAP = {
            1: FricCoefSel.Calculated_by_Colebrook_White(),
            0: FricCoefSel.User_Defined(),
        }
        return _MAP.get(v, FricCoefSel("unknown_{}".format(v), v))

    @staticmethod
    def Calculated_by_Colebrook_White():
        """Returns the FricCoefSel value for 'Calculated by Colebrook-White'."""
        return FricCoefSel('Calculated_by_Colebrook_White', 1)

    @staticmethod
    def User_Defined():
        """Returns the FricCoefSel value for 'User-Defined'."""
        return FricCoefSel('User_Defined', 0)


class GasIsrchsSel(object):
    """Enumeration of GasIsrchsSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the GasIsrchsSel instance for a given integer value."""
        _MAP = {
            0: GasIsrchsSel.Left_Inside(),
            1: GasIsrchsSel.Right_Outside(),
        }
        return _MAP.get(v, GasIsrchsSel("unknown_{}".format(v), v))

    @staticmethod
    def Left_Inside():
        """Returns the GasIsrchsSel value for 'Left (Inside)'."""
        return GasIsrchsSel('Left_Inside', 0)

    @staticmethod
    def Right_Outside():
        """Returns the GasIsrchsSel value for 'Right (Outside)'."""
        return GasIsrchsSel('Right_Outside', 1)


class GasSrcTypeSel(object):
    """Enumeration of GasSrcTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the GasSrcTypeSel instance for a given integer value."""
        _MAP = {
            0: GasSrcTypeSel.Gas(),
            1: GasSrcTypeSel.Ice(),
            2: GasSrcTypeSel.Steel(),
        }
        return _MAP.get(v, GasSrcTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Gas():
        """Returns the GasSrcTypeSel value for 'Gas'."""
        return GasSrcTypeSel('Gas', 0)

    @staticmethod
    def Ice():
        """Returns the GasSrcTypeSel value for 'Ice'."""
        return GasSrcTypeSel('Ice', 1)

    @staticmethod
    def Steel():
        """Returns the GasSrcTypeSel value for 'Steel'."""
        return GasSrcTypeSel('Steel', 2)


class HPMESettleSel(object):
    """Enumeration of HPMESettleSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HPMESettleSel instance for a given integer value."""
        _MAP = {
            0: HPMESettleSel.Cavity_Settle_Area(),
            1: HPMESettleSel.Left_hand_side_of_heat_structure(),
            2: HPMESettleSel.Right_hand_side_of_heat_structure(),
        }
        return _MAP.get(v, HPMESettleSel("unknown_{}".format(v), v))

    @staticmethod
    def Cavity_Settle_Area():
        """Returns the HPMESettleSel value for 'Cavity Settle Area'."""
        return HPMESettleSel('Cavity_Settle_Area', 0)

    @staticmethod
    def Left_hand_side_of_heat_structure():
        """Returns the HPMESettleSel value for 'Left hand side of heat structure'."""
        return HPMESettleSel('Left_hand_side_of_heat_structure', 1)

    @staticmethod
    def Right_hand_side_of_heat_structure():
        """Returns the HPMESettleSel value for 'Right hand side of heat structure'."""
        return HPMESettleSel('Right_hand_side_of_heat_structure', 2)


class HPMESourceSel(object):
    """Enumeration of HPMESourceSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HPMESourceSel instance for a given integer value."""
        _MAP = {
            0: HPMESourceSel.Zircaloy(),
            1: HPMESourceSel.zirconium_oxide(),
            2: HPMESourceSel.uranium_dioxide(),
            3: HPMESourceSel.stainless_steel(),
            4: HPMESourceSel.stainless_steel_oxide(),
            5: HPMESourceSel.boron_carbide(),
            6: HPMESourceSel.silver_indium_cadmium(),
            7: HPMESourceSel.uranium_metal(),
            8: HPMESourceSel.aluminum(),
            9: HPMESourceSel.aluminum_oxide(),
            10: HPMESourceSel.cadmium(),
        }
        return _MAP.get(v, HPMESourceSel("unknown_{}".format(v), v))

    @staticmethod
    def Zircaloy():
        """Returns the HPMESourceSel value for 'Zircaloy'."""
        return HPMESourceSel('Zircaloy', 0)

    @staticmethod
    def zirconium_oxide():
        """Returns the HPMESourceSel value for 'zirconium-oxide'."""
        return HPMESourceSel('zirconium_oxide', 1)

    @staticmethod
    def uranium_dioxide():
        """Returns the HPMESourceSel value for 'uranium-dioxide'."""
        return HPMESourceSel('uranium_dioxide', 2)

    @staticmethod
    def stainless_steel():
        """Returns the HPMESourceSel value for 'stainless-steel'."""
        return HPMESourceSel('stainless_steel', 3)

    @staticmethod
    def stainless_steel_oxide():
        """Returns the HPMESourceSel value for 'stainless-steel-oxide'."""
        return HPMESourceSel('stainless_steel_oxide', 4)

    @staticmethod
    def boron_carbide():
        """Returns the HPMESourceSel value for 'boron carbide'."""
        return HPMESourceSel('boron_carbide', 5)

    @staticmethod
    def silver_indium_cadmium():
        """Returns the HPMESourceSel value for 'silver-indium-cadmium'."""
        return HPMESourceSel('silver_indium_cadmium', 6)

    @staticmethod
    def uranium_metal():
        """Returns the HPMESourceSel value for 'uranium-metal'."""
        return HPMESourceSel('uranium_metal', 7)

    @staticmethod
    def aluminum():
        """Returns the HPMESourceSel value for 'aluminum'."""
        return HPMESourceSel('aluminum', 8)

    @staticmethod
    def aluminum_oxide():
        """Returns the HPMESourceSel value for 'aluminum-oxide'."""
        return HPMESourceSel('aluminum_oxide', 9)

    @staticmethod
    def cadmium():
        """Returns the HPMESourceSel value for 'cadmium'."""
        return HPMESourceSel('cadmium', 10)


class HSIgeomSel(object):
    """Enumeration of HSIgeomSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HSIgeomSel instance for a given integer value."""
        _MAP = {
            1: HSIgeomSel.Rectangular(),
            2: HSIgeomSel.Cylindrical(),
            3: HSIgeomSel.Spherical(),
            4: HSIgeomSel.Bottom_Hemisphere(),
            5: HSIgeomSel.Top_Hemesphere(),
        }
        return _MAP.get(v, HSIgeomSel("unknown_{}".format(v), v))

    @staticmethod
    def Rectangular():
        """Returns the HSIgeomSel value for 'Rectangular'."""
        return HSIgeomSel('Rectangular', 1)

    @staticmethod
    def Cylindrical():
        """Returns the HSIgeomSel value for 'Cylindrical'."""
        return HSIgeomSel('Cylindrical', 2)

    @staticmethod
    def Spherical():
        """Returns the HSIgeomSel value for 'Spherical'."""
        return HSIgeomSel('Spherical', 3)

    @staticmethod
    def Bottom_Hemisphere():
        """Returns the HSIgeomSel value for 'Bottom Hemisphere'."""
        return HSIgeomSel('Bottom_Hemisphere', 4)

    @staticmethod
    def Top_Hemesphere():
        """Returns the HSIgeomSel value for 'Top Hemesphere'."""
        return HSIgeomSel('Top_Hemesphere', 5)


class HSIssSel(object):
    """Enumeration of HSIssSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HSIssSel instance for a given integer value."""
        _MAP = {
            0: HSIssSel.Input_Temperatures(),
            1: HSIssSel.Calculate_IC(),
        }
        return _MAP.get(v, HSIssSel("unknown_{}".format(v), v))

    @staticmethod
    def Input_Temperatures():
        """Returns the HSIssSel value for 'Input Temperatures'."""
        return HSIssSel('Input_Temperatures', 0)

    @staticmethod
    def Calculate_IC():
        """Returns the HSIssSel value for 'Calculate IC'."""
        return HSIssSel('Calculate_IC', 1)


class HSSideSel(object):
    """Enumeration of HSSideSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HSSideSel instance for a given integer value."""
        _MAP = {
            0: HSSideSel.Left_Hand_Side(),
            1: HSSideSel.Right_Hand_Side(),
        }
        return _MAP.get(v, HSSideSel("unknown_{}".format(v), v))

    @staticmethod
    def Left_Hand_Side():
        """Returns the HSSideSel value for 'Left Hand Side'."""
        return HSSideSel('Left_Hand_Side', 0)

    @staticmethod
    def Right_Hand_Side():
        """Returns the HSSideSel value for 'Right Hand Side'."""
        return HSSideSel('Right_Hand_Side', 1)


class HeatFlowSel(object):
    """Enumeration of HeatFlowSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HeatFlowSel instance for a given integer value."""
        _MAP = {
            0: HeatFlowSel.Internal_Flow(),
            1: HeatFlowSel.External_Flow(),
        }
        return _MAP.get(v, HeatFlowSel("unknown_{}".format(v), v))

    @staticmethod
    def Internal_Flow():
        """Returns the HeatFlowSel value for 'Internal Flow'."""
        return HeatFlowSel('Internal_Flow', 0)

    @staticmethod
    def External_Flow():
        """Returns the HeatFlowSel value for 'External Flow'."""
        return HeatFlowSel('External_Flow', 1)


class HeatIfrmatSel(object):
    """Enumeration of HeatIfrmatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HeatIfrmatSel instance for a given integer value."""
        _MAP = {
            1: HeatIfrmatSel.Node_Location(),
            2: HeatIfrmatSel.Node_Distance(),
        }
        return _MAP.get(v, HeatIfrmatSel("unknown_{}".format(v), v))

    @staticmethod
    def Node_Location():
        """Returns the HeatIfrmatSel value for 'Node Location'."""
        return HeatIfrmatSel('Node_Location', 1)

    @staticmethod
    def Node_Distance():
        """Returns the HeatIfrmatSel value for 'Node Distance'."""
        return HeatIfrmatSel('Node_Distance', 2)


class HeatMetalSel(object):
    """Enumeration of HeatMetalSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HeatMetalSel instance for a given integer value."""
        _MAP = {
            0: HeatMetalSel.Use_split_calculated_by_MELCOR(),
            1: HeatMetalSel.Metal_phase_heat_control(),
        }
        return _MAP.get(v, HeatMetalSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_split_calculated_by_MELCOR():
        """Returns the HeatMetalSel value for 'Use split calculated by MELCOR'."""
        return HeatMetalSel('Use_split_calculated_by_MELCOR', 0)

    @staticmethod
    def Metal_phase_heat_control():
        """Returns the HeatMetalSel value for 'Metal phase heat control'."""
        return HeatMetalSel('Metal_phase_heat_control', 1)


class HeatOutFlowSel(object):
    """Enumeration of HeatOutFlowSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HeatOutFlowSel instance for a given integer value."""
        _MAP = {
            0: HeatOutFlowSel.Internal_Flow(),
            1: HeatOutFlowSel.External_Flow(),
            2: HeatOutFlowSel.Ice_Condenser(),
        }
        return _MAP.get(v, HeatOutFlowSel("unknown_{}".format(v), v))

    @staticmethod
    def Internal_Flow():
        """Returns the HeatOutFlowSel value for 'Internal Flow'."""
        return HeatOutFlowSel('Internal_Flow', 0)

    @staticmethod
    def External_Flow():
        """Returns the HeatOutFlowSel value for 'External Flow'."""
        return HeatOutFlowSel('External_Flow', 1)

    @staticmethod
    def Ice_Condenser():
        """Returns the HeatOutFlowSel value for 'Ice Condenser'."""
        return HeatOutFlowSel('Ice_Condenser', 2)


class HtsideSel(object):
    """Enumeration of HtsideSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the HtsideSel instance for a given integer value."""
        _MAP = {
            2: HtsideSel.Activated(),
            1: HtsideSel.Adiabatic(),
        }
        return _MAP.get(v, HtsideSel("unknown_{}".format(v), v))

    @staticmethod
    def Activated():
        """Returns the HtsideSel value for 'Activated'."""
        return HtsideSel('Activated', 2)

    @staticmethod
    def Adiabatic():
        """Returns the HtsideSel value for 'Adiabatic'."""
        return HtsideSel('Adiabatic', 1)


class IbhtbSel(object):
    """Enumeration of IbhtbSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IbhtbSel instance for a given integer value."""
        _MAP = {
            0: IbhtbSel.Standard(),
            -1: IbhtbSel.Multiplier(),
            1: IbhtbSel.Sensitivity_Coefficients(),
        }
        return _MAP.get(v, IbhtbSel("unknown_{}".format(v), v))

    @staticmethod
    def Standard():
        """Returns the IbhtbSel value for 'Standard'."""
        return IbhtbSel('Standard', 0)

    @staticmethod
    def Multiplier():
        """Returns the IbhtbSel value for 'Multiplier'."""
        return IbhtbSel('Multiplier', -1)

    @staticmethod
    def Sensitivity_Coefficients():
        """Returns the IbhtbSel value for 'Sensitivity Coefficients'."""
        return IbhtbSel('Sensitivity_Coefficients', 1)


class IbubSel(object):
    """Enumeration of IbubSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IbubSel instance for a given integer value."""
        _MAP = {
            0: IbubSel.NOBUBBLERISE(),
            -1: IbubSel.NOSCRUBBINGRN(),
            -2: IbubSel.AEROSOLSCRUBBING(),
            -3: IbubSel.IODINESCRUBBING(),
        }
        return _MAP.get(v, IbubSel("unknown_{}".format(v), v))

    @staticmethod
    def NOBUBBLERISE():
        """Returns the IbubSel value for 'NOBUBBLERISE'."""
        return IbubSel('NOBUBBLERISE', 0)

    @staticmethod
    def NOSCRUBBINGRN():
        """Returns the IbubSel value for 'NOSCRUBBINGRN'."""
        return IbubSel('NOSCRUBBINGRN', -1)

    @staticmethod
    def AEROSOLSCRUBBING():
        """Returns the IbubSel value for 'AEROSOLSCRUBBING'."""
        return IbubSel('AEROSOLSCRUBBING', -2)

    @staticmethod
    def IODINESCRUBBING():
        """Returns the IbubSel value for 'IODINESCRUBBING'."""
        return IbubSel('IODINESCRUBBING', -3)


class IcflimSel(object):
    """Enumeration of IcflimSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IcflimSel instance for a given integer value."""
        _MAP = {
            0: IcflimSel.No_Boundary_Input(),
            1: IcflimSel.Lower_Bound_Only(),
            2: IcflimSel.Upper_Bound_Only(),
            3: IcflimSel.Both_Bounds(),
        }
        return _MAP.get(v, IcflimSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Boundary_Input():
        """Returns the IcflimSel value for 'No Boundary Input'."""
        return IcflimSel('No_Boundary_Input', 0)

    @staticmethod
    def Lower_Bound_Only():
        """Returns the IcflimSel value for 'Lower Bound Only'."""
        return IcflimSel('Lower_Bound_Only', 1)

    @staticmethod
    def Upper_Bound_Only():
        """Returns the IcflimSel value for 'Upper Bound Only'."""
        return IcflimSel('Upper_Bound_Only', 2)

    @staticmethod
    def Both_Bounds():
        """Returns the IcflimSel value for 'Both Bounds'."""
        return IcflimSel('Both_Bounds', 3)


class IchemSel(object):
    """Enumeration of IchemSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IchemSel instance for a given integer value."""
        _MAP = {
            1: IchemSel.Include(),
            0: IchemSel.Exclude(),
        }
        return _MAP.get(v, IchemSel("unknown_{}".format(v), v))

    @staticmethod
    def Include():
        """Returns the IchemSel value for 'Include'."""
        return IchemSel('Include', 1)

    @staticmethod
    def Exclude():
        """Returns the IchemSel value for 'Exclude'."""
        return IchemSel('Exclude', 0)


class IchtSel(object):
    """Enumeration of IchtSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IchtSel instance for a given integer value."""
        _MAP = {
            0: IchtSel.MOD3(),
            -1: IchtSel.VALUE(),
            2: IchtSel.MOD2(),
        }
        return _MAP.get(v, IchtSel("unknown_{}".format(v), v))

    @staticmethod
    def MOD3():
        """Returns the IchtSel value for 'MOD3'."""
        return IchtSel('MOD3', 0)

    @staticmethod
    def VALUE():
        """Returns the IchtSel value for 'VALUE'."""
        return IchtSel('VALUE', -1)

    @staticmethod
    def MOD2():
        """Returns the IchtSel value for 'MOD2'."""
        return IchtSel('MOD2', 2)


class IcokSel(object):
    """Enumeration of IcokSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IcokSel instance for a given integer value."""
        _MAP = {
            1: IcokSel.Enable(),
            0: IcokSel.Suppress(),
        }
        return _MAP.get(v, IcokSel("unknown_{}".format(v), v))

    @staticmethod
    def Enable():
        """Returns the IcokSel value for 'Enable'."""
        return IcokSel('Enable', 1)

    @staticmethod
    def Suppress():
        """Returns the IcokSel value for 'Suppress'."""
        return IcokSel('Suppress', 0)


class IcvactSel(object):
    """Enumeration of IcvactSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IcvactSel instance for a given integer value."""
        _MAP = {
            0: IcvactSel.Active(),
            1: IcvactSel.Inactive(),
            -1: IcvactSel.Constant(),
            -2: IcvactSel.Time_Dep(),
            -3: IcvactSel.Constant_Active(),
        }
        return _MAP.get(v, IcvactSel("unknown_{}".format(v), v))

    @staticmethod
    def Active():
        """Returns the IcvactSel value for 'Active'."""
        return IcvactSel('Active', 0)

    @staticmethod
    def Inactive():
        """Returns the IcvactSel value for 'Inactive'."""
        return IcvactSel('Inactive', 1)

    @staticmethod
    def Constant():
        """Returns the IcvactSel value for 'Constant'."""
        return IcvactSel('Constant', -1)

    @staticmethod
    def Time_Dep():
        """Returns the IcvactSel value for 'Time-Dep'."""
        return IcvactSel('Time_Dep', -2)

    @staticmethod
    def Constant_Active():
        """Returns the IcvactSel value for 'Constant/Active'."""
        return IcvactSel('Constant_Active', -3)


class IcvffSel(object):
    """Enumeration of IcvffSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IcvffSel instance for a given integer value."""
        _MAP = {
            0: IcvffSel.Not_Defined(),
            1: IcvffSel.Horizontal_Flow(),
            2: IcvffSel.Vertical_flow(),
        }
        return _MAP.get(v, IcvffSel("unknown_{}".format(v), v))

    @staticmethod
    def Not_Defined():
        """Returns the IcvffSel value for 'Not Defined'."""
        return IcvffSel('Not_Defined', 0)

    @staticmethod
    def Horizontal_Flow():
        """Returns the IcvffSel value for 'Horizontal Flow'."""
        return IcvffSel('Horizontal_Flow', 1)

    @staticmethod
    def Vertical_flow():
        """Returns the IcvffSel value for 'Vertical flow'."""
        return IcvffSel('Vertical_flow', 2)


class IcvthrSel(object):
    """Enumeration of IcvthrSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IcvthrSel instance for a given integer value."""
        _MAP = {
            1: IcvthrSel.Equilibrium(),
            2: IcvthrSel.Non_Equilibrium(),
        }
        return _MAP.get(v, IcvthrSel("unknown_{}".format(v), v))

    @staticmethod
    def Equilibrium():
        """Returns the IcvthrSel value for 'Equilibrium'."""
        return IcvthrSel('Equilibrium', 1)

    @staticmethod
    def Non_Equilibrium():
        """Returns the IcvthrSel value for 'Non-Equilibrium'."""
        return IcvthrSel('Non_Equilibrium', 2)


class IdealSel(object):
    """Enumeration of IdealSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IdealSel instance for a given integer value."""
        _MAP = {
            1: IdealSel.Ideal(),
            -1: IdealSel.Differ(),
        }
        return _MAP.get(v, IdealSel("unknown_{}".format(v), v))

    @staticmethod
    def Ideal():
        """Returns the IdealSel value for 'Ideal'."""
        return IdealSel('Ideal', 1)

    @staticmethod
    def Differ():
        """Returns the IdealSel value for 'Differ'."""
        return IdealSel('Differ', -1)


class IfilmSel(object):
    """Enumeration of IfilmSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IfilmSel instance for a given integer value."""
        _MAP = {
            0: IfilmSel.Slag(),
            1: IfilmSel.Gas(),
        }
        return _MAP.get(v, IfilmSel("unknown_{}".format(v), v))

    @staticmethod
    def Slag():
        """Returns the IfilmSel value for 'Slag'."""
        return IfilmSel('Slag', 0)

    @staticmethod
    def Gas():
        """Returns the IfilmSel value for 'Gas'."""
        return IfilmSel('Gas', 1)


class IfsflgSel(object):
    """Enumeration of IfsflgSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IfsflgSel instance for a given integer value."""
        _MAP = {
            0: IfsflgSel.Control_Function_IFSFLG_type(),
            1: IfsflgSel.Integer_IFSFLG_type(),
        }
        return _MAP.get(v, IfsflgSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function_IFSFLG_type():
        """Returns the IfsflgSel value for 'Control Function IFSFLG type'."""
        return IfsflgSel('Control_Function_IFSFLG_type', 0)

    @staticmethod
    def Integer_IFSFLG_type():
        """Returns the IfsflgSel value for 'Integer IFSFLG type'."""
        return IfsflgSel('Integer_IFSFLG_type', 1)


class IgntrSel(object):
    """Enumeration of IgntrSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IgntrSel instance for a given integer value."""
        _MAP = {
            0: IgntrSel.igniter_not_active_in_control_volume(),
            1: IgntrSel.igniter_is_active_in_control_volume(),
            86: IgntrSel.burning_prohibited_in_control_volume(),
        }
        return _MAP.get(v, IgntrSel("unknown_{}".format(v), v))

    @staticmethod
    def igniter_not_active_in_control_volume():
        """Returns the IgntrSel value for 'igniter not active in control volume'."""
        return IgntrSel('igniter_not_active_in_control_volume', 0)

    @staticmethod
    def igniter_is_active_in_control_volume():
        """Returns the IgntrSel value for 'igniter is active in control volume'."""
        return IgntrSel('igniter_is_active_in_control_volume', 1)

    @staticmethod
    def burning_prohibited_in_control_volume():
        """Returns the IgntrSel value for 'burning prohibited in control volume'."""
        return IgntrSel('burning_prohibited_in_control_volume', 86)


class IgntrTypeSel(object):
    """Enumeration of IgntrTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IgntrTypeSel instance for a given integer value."""
        _MAP = {
            0: IgntrTypeSel.Use_Control_Function(),
            1: IgntrTypeSel.Use_Integer_Value(),
        }
        return _MAP.get(v, IgntrTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_Control_Function():
        """Returns the IgntrTypeSel value for 'Use Control Function'."""
        return IgntrTypeSel('Use_Control_Function', 0)

    @staticmethod
    def Use_Integer_Value():
        """Returns the IgntrTypeSel value for 'Use Integer Value'."""
        return IgntrTypeSel('Use_Integer_Value', 1)


class ImixSel(object):
    """Enumeration of ImixSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ImixSel instance for a given integer value."""
        _MAP = {
            0: ImixSel.Suppress_Mixing(),
            1: ImixSel.Calculate_Mixing(),
            -1: ImixSel.Enforce_Mixing(),
        }
        return _MAP.get(v, ImixSel("unknown_{}".format(v), v))

    @staticmethod
    def Suppress_Mixing():
        """Returns the ImixSel value for 'Suppress Mixing'."""
        return ImixSel('Suppress_Mixing', 0)

    @staticmethod
    def Calculate_Mixing():
        """Returns the ImixSel value for 'Calculate Mixing'."""
        return ImixSel('Calculate_Mixing', 1)

    @staticmethod
    def Enforce_Mixing():
        """Returns the ImixSel value for 'Enforce Mixing'."""
        return ImixSel('Enforce_Mixing', -1)


class InTransTypeSel(object):
    """Enumeration of InTransTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the InTransTypeSel instance for a given integer value."""
        _MAP = {
            0: InTransTypeSel.HS(),
            1: InTransTypeSel.FDI(),
            2: InTransTypeSel.RNFDI(),
            3: InTransTypeSel.COR(),
            4: InTransTypeSel.RNCOR(),
            5: InTransTypeSel.EDF(),
            6: InTransTypeSel.Simple(),
        }
        return _MAP.get(v, InTransTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def HS():
        """Returns the InTransTypeSel value for 'HS'."""
        return InTransTypeSel('HS', 0)

    @staticmethod
    def FDI():
        """Returns the InTransTypeSel value for 'FDI'."""
        return InTransTypeSel('FDI', 1)

    @staticmethod
    def RNFDI():
        """Returns the InTransTypeSel value for 'RNFDI'."""
        return InTransTypeSel('RNFDI', 2)

    @staticmethod
    def COR():
        """Returns the InTransTypeSel value for 'COR'."""
        return InTransTypeSel('COR', 3)

    @staticmethod
    def RNCOR():
        """Returns the InTransTypeSel value for 'RNCOR'."""
        return InTransTypeSel('RNCOR', 4)

    @staticmethod
    def EDF():
        """Returns the InTransTypeSel value for 'EDF'."""
        return InTransTypeSel('EDF', 5)

    @staticmethod
    def Simple():
        """Returns the InTransTypeSel value for 'Simple'."""
        return InTransTypeSel('Simple', 6)


class InitMassModeSel(object):
    """Enumeration of InitMassModeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the InitMassModeSel instance for a given integer value."""
        _MAP = {
            0: InitMassModeSel.Fractional_Value(),
            1: InitMassModeSel.Actual_Value(),
        }
        return _MAP.get(v, InitMassModeSel("unknown_{}".format(v), v))

    @staticmethod
    def Fractional_Value():
        """Returns the InitMassModeSel value for 'Fractional Value'."""
        return InitMassModeSel('Fractional_Value', 0)

    @staticmethod
    def Actual_Value():
        """Returns the InitMassModeSel value for 'Actual Value'."""
        return InitMassModeSel('Actual_Value', 1)


class IodIodflgSel(object):
    """Enumeration of IodIodflgSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IodIodflgSel instance for a given integer value."""
        _MAP = {
            0: IodIodflgSel.Activate_Only_With_Iodine(),
            1: IodIodflgSel.Activate_Without_Iodine(),
        }
        return _MAP.get(v, IodIodflgSel("unknown_{}".format(v), v))

    @staticmethod
    def Activate_Only_With_Iodine():
        """Returns the IodIodflgSel value for 'Activate Only With Iodine'."""
        return IodIodflgSel('Activate_Only_With_Iodine', 0)

    @staticmethod
    def Activate_Without_Iodine():
        """Returns the IodIodflgSel value for 'Activate Without Iodine'."""
        return IodIodflgSel('Activate_Without_Iodine', 1)


class IodineDosidSel(object):
    """Enumeration of IodineDosidSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IodineDosidSel instance for a given integer value."""
        _MAP = {
            0: IodineDosidSel.Atmospheric(),
            1: IodineDosidSel.Pool(),
            2: IodineDosidSel.Wall(),
            3: IodineDosidSel.Cable(),
        }
        return _MAP.get(v, IodineDosidSel("unknown_{}".format(v), v))

    @staticmethod
    def Atmospheric():
        """Returns the IodineDosidSel value for 'Atmospheric'."""
        return IodineDosidSel('Atmospheric', 0)

    @staticmethod
    def Pool():
        """Returns the IodineDosidSel value for 'Pool'."""
        return IodineDosidSel('Pool', 1)

    @staticmethod
    def Wall():
        """Returns the IodineDosidSel value for 'Wall'."""
        return IodineDosidSel('Wall', 2)

    @staticmethod
    def Cable():
        """Returns the IodineDosidSel value for 'Cable'."""
        return IodineDosidSel('Cable', 3)


class IodineDossrcSel(object):
    """Enumeration of IodineDossrcSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IodineDossrcSel instance for a given integer value."""
        _MAP = {
            0: IodineDossrcSel.Dose_Rate_Off(),
            1: IodineDossrcSel.Decay_Heat(),
            2: IodineDossrcSel.Source_Location(),
        }
        return _MAP.get(v, IodineDossrcSel("unknown_{}".format(v), v))

    @staticmethod
    def Dose_Rate_Off():
        """Returns the IodineDossrcSel value for 'Dose Rate Off'."""
        return IodineDossrcSel('Dose_Rate_Off', 0)

    @staticmethod
    def Decay_Heat():
        """Returns the IodineDossrcSel value for 'Decay Heat'."""
        return IodineDossrcSel('Decay_Heat', 1)

    @staticmethod
    def Source_Location():
        """Returns the IodineDossrcSel value for 'Source Location'."""
        return IodineDossrcSel('Source_Location', 2)


class IodineIrcoptSel(object):
    """Enumeration of IodineIrcoptSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IodineIrcoptSel instance for a given integer value."""
        _MAP = {
            0: IodineIrcoptSel.INSPECT_Powers(),
            1: IodineIrcoptSel.INSPECT(),
            2: IodineIrcoptSel.Boyd_Carter_and_Dixon(),
            3: IodineIrcoptSel.Minimum_Set(),
        }
        return _MAP.get(v, IodineIrcoptSel("unknown_{}".format(v), v))

    @staticmethod
    def INSPECT_Powers():
        """Returns the IodineIrcoptSel value for 'INSPECT-Powers'."""
        return IodineIrcoptSel('INSPECT_Powers', 0)

    @staticmethod
    def INSPECT():
        """Returns the IodineIrcoptSel value for 'INSPECT'."""
        return IodineIrcoptSel('INSPECT', 1)

    @staticmethod
    def Boyd_Carter_and_Dixon():
        """Returns the IodineIrcoptSel value for 'Boyd, Carter and Dixon'."""
        return IodineIrcoptSel('Boyd_Carter_and_Dixon', 2)

    @staticmethod
    def Minimum_Set():
        """Returns the IodineIrcoptSel value for 'Minimum Set'."""
        return IodineIrcoptSel('Minimum_Set', 3)


class IpdhcfTypeSel(object):
    """Enumeration of IpdhcfTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IpdhcfTypeSel instance for a given integer value."""
        _MAP = {
            0: IpdhcfTypeSel.Zero_DCH(),
            1: IpdhcfTypeSel.Calculate_From_DCH_RN(),
            -1: IpdhcfTypeSel.Control_Function(),
        }
        return _MAP.get(v, IpdhcfTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Zero_DCH():
        """Returns the IpdhcfTypeSel value for 'Zero DCH'."""
        return IpdhcfTypeSel('Zero_DCH', 0)

    @staticmethod
    def Calculate_From_DCH_RN():
        """Returns the IpdhcfTypeSel value for 'Calculate From DCH & RN'."""
        return IpdhcfTypeSel('Calculate_From_DCH_RN', 1)

    @staticmethod
    def Control_Function():
        """Returns the IpdhcfTypeSel value for 'Control Function'."""
        return IpdhcfTypeSel('Control_Function', -1)


class IpfswSel(object):
    """Enumeration of IpfswSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IpfswSel instance for a given integer value."""
        _MAP = {
            0: IpfswSel.Pool_fog_allowed(),
            1: IpfswSel.No_pool_fog_allowed(),
            2: IpfswSel.Pool_no_fog(),
        }
        return _MAP.get(v, IpfswSel("unknown_{}".format(v), v))

    @staticmethod
    def Pool_fog_allowed():
        """Returns the IpfswSel value for 'Pool, fog allowed'."""
        return IpfswSel('Pool_fog_allowed', 0)

    @staticmethod
    def No_pool_fog_allowed():
        """Returns the IpfswSel value for 'No pool, fog allowed'."""
        return IpfswSel('No_pool_fog_allowed', 1)

    @staticmethod
    def Pool_no_fog():
        """Returns the IpfswSel value for 'Pool, no fog'."""
        return IpfswSel('Pool_no_fog', 2)


class IpoxcfTypeSel(object):
    """Enumeration of IpoxcfTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the IpoxcfTypeSel instance for a given integer value."""
        _MAP = {
            0: IpoxcfTypeSel.Use_split_provided_by_MELCOR(),
            -1: IpoxcfTypeSel.Use_Control_Function(),
        }
        return _MAP.get(v, IpoxcfTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_split_provided_by_MELCOR():
        """Returns the IpoxcfTypeSel value for 'Use split provided by MELCOR'."""
        return IpoxcfTypeSel('Use_split_provided_by_MELCOR', 0)

    @staticmethod
    def Use_Control_Function():
        """Returns the IpoxcfTypeSel value for 'Use Control Function'."""
        return IpoxcfTypeSel('Use_Control_Function', -1)


class ItypthSel(object):
    """Enumeration of ItypthSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ItypthSel instance for a given integer value."""
        _MAP = {
            1: ItypthSel.Masses_and_Energies(),
            2: ItypthSel.P_T_and_Mass_frac(),
            3: ItypthSel.Pool_and_Atmosphere(),
        }
        return _MAP.get(v, ItypthSel("unknown_{}".format(v), v))

    @staticmethod
    def Masses_and_Energies():
        """Returns the ItypthSel value for 'Masses and Energies'."""
        return ItypthSel('Masses_and_Energies', 1)

    @staticmethod
    def P_T_and_Mass_frac():
        """Returns the ItypthSel value for 'P, T,and Mass frac'."""
        return ItypthSel('P_T_and_Mass_frac', 2)

    @staticmethod
    def Pool_and_Atmosphere():
        """Returns the ItypthSel value for 'Pool and Atmosphere'."""
        return ItypthSel('Pool_and_Atmosphere', 3)


class JetPresSel(object):
    """Enumeration of JetPresSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the JetPresSel instance for a given integer value."""
        _MAP = {
            0: JetPresSel.Control_Function(),
            1: JetPresSel.Constant_Pressure(),
        }
        return _MAP.get(v, JetPresSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function():
        """Returns the JetPresSel value for 'Control Function'."""
        return JetPresSel('Control_Function', 0)

    @staticmethod
    def Constant_Pressure():
        """Returns the JetPresSel value for 'Constant Pressure'."""
        return JetPresSel('Constant_Pressure', 1)


class LayerActionSel(object):
    """Enumeration of LayerActionSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the LayerActionSel instance for a given integer value."""
        _MAP = {
            0: LayerActionSel.TEMP_Define_a_Layer(),
            1: LayerActionSel.DELETE_Delete_a_Layer(),
        }
        return _MAP.get(v, LayerActionSel("unknown_{}".format(v), v))

    @staticmethod
    def TEMP_Define_a_Layer():
        """Returns the LayerActionSel value for 'TEMP - Define a Layer'."""
        return LayerActionSel('TEMP_Define_a_Layer', 0)

    @staticmethod
    def DELETE_Delete_a_Layer():
        """Returns the LayerActionSel value for 'DELETE - Delete a Layer'."""
        return LayerActionSel('DELETE_Delete_a_Layer', 1)


class LevelInsupSel(object):
    """Enumeration of LevelInsupSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the LevelInsupSel instance for a given integer value."""
        _MAP = {
            0: LevelInsupSel.Use_Default(),
            1: LevelInsupSel.Below(),
            2: LevelInsupSel.Above(),
            3: LevelInsupSel.Fixed(),
            4: LevelInsupSel.Blade(),
            5: LevelInsupSel.Rod(),
        }
        return _MAP.get(v, LevelInsupSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_Default():
        """Returns the LevelInsupSel value for 'Use Default'."""
        return LevelInsupSel('Use_Default', 0)

    @staticmethod
    def Below():
        """Returns the LevelInsupSel value for 'Below'."""
        return LevelInsupSel('Below', 1)

    @staticmethod
    def Above():
        """Returns the LevelInsupSel value for 'Above'."""
        return LevelInsupSel('Above', 2)

    @staticmethod
    def Fixed():
        """Returns the LevelInsupSel value for 'Fixed'."""
        return LevelInsupSel('Fixed', 3)

    @staticmethod
    def Blade():
        """Returns the LevelInsupSel value for 'Blade'."""
        return LevelInsupSel('Blade', 4)

    @staticmethod
    def Rod():
        """Returns the LevelInsupSel value for 'Rod'."""
        return LevelInsupSel('Rod', 5)


class MCUndefSel(object):
    """Enumeration of MCUndefSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MCUndefSel instance for a given integer value."""
        _MAP = {
            0: MCUndefSel.Real(),
            1: MCUndefSel.Off(),
            2: MCUndefSel.Default(),
        }
        return _MAP.get(v, MCUndefSel("unknown_{}".format(v), v))

    @staticmethod
    def Real():
        """Returns the MCUndefSel value for 'Real'."""
        return MCUndefSel('Real', 0)

    @staticmethod
    def Off():
        """Returns the MCUndefSel value for 'Off'."""
        return MCUndefSel('Off', 1)

    @staticmethod
    def Default():
        """Returns the MCUndefSel value for 'Default'."""
        return MCUndefSel('Default', 2)


class MPOptionSel(object):
    """Enumeration of MPOptionSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MPOptionSel instance for a given integer value."""
        _MAP = {
            0: MPOptionSel.Default(),
            1: MPOptionSel.Specified(),
        }
        return _MAP.get(v, MPOptionSel("unknown_{}".format(v), v))

    @staticmethod
    def Default():
        """Returns the MPOptionSel value for 'Default'."""
        return MPOptionSel('Default', 0)

    @staticmethod
    def Specified():
        """Returns the MPOptionSel value for 'Specified'."""
        return MPOptionSel('Specified', 1)


class MaterialPropSel(object):
    """Enumeration of MaterialPropSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MaterialPropSel instance for a given integer value."""
        _MAP = {
            0: MaterialPropSel.CV0(),
            1: MaterialPropSel.CV1(),
            2: MaterialPropSel.CV2(),
            3: MaterialPropSel.CV3(),
            4: MaterialPropSel.CVSQRT(),
            5: MaterialPropSel.CVM1(),
            6: MaterialPropSel.CVM2(),
            7: MaterialPropSel.TLOW(),
            8: MaterialPropSel.TUP(),
            9: MaterialPropSel.WM(),
            10: MaterialPropSel.EF(),
            11: MaterialPropSel.SZ(),
        }
        return _MAP.get(v, MaterialPropSel("unknown_{}".format(v), v))

    @staticmethod
    def CV0():
        """Returns the MaterialPropSel value for 'CV0'."""
        return MaterialPropSel('CV0', 0)

    @staticmethod
    def CV1():
        """Returns the MaterialPropSel value for 'CV1'."""
        return MaterialPropSel('CV1', 1)

    @staticmethod
    def CV2():
        """Returns the MaterialPropSel value for 'CV2'."""
        return MaterialPropSel('CV2', 2)

    @staticmethod
    def CV3():
        """Returns the MaterialPropSel value for 'CV3'."""
        return MaterialPropSel('CV3', 3)

    @staticmethod
    def CVSQRT():
        """Returns the MaterialPropSel value for 'CVSQRT'."""
        return MaterialPropSel('CVSQRT', 4)

    @staticmethod
    def CVM1():
        """Returns the MaterialPropSel value for 'CVM1'."""
        return MaterialPropSel('CVM1', 5)

    @staticmethod
    def CVM2():
        """Returns the MaterialPropSel value for 'CVM2'."""
        return MaterialPropSel('CVM2', 6)

    @staticmethod
    def TLOW():
        """Returns the MaterialPropSel value for 'TLOW'."""
        return MaterialPropSel('TLOW', 7)

    @staticmethod
    def TUP():
        """Returns the MaterialPropSel value for 'TUP'."""
        return MaterialPropSel('TUP', 8)

    @staticmethod
    def WM():
        """Returns the MaterialPropSel value for 'WM'."""
        return MaterialPropSel('WM', 9)

    @staticmethod
    def EF():
        """Returns the MaterialPropSel value for 'EF'."""
        return MaterialPropSel('EF', 10)

    @staticmethod
    def SZ():
        """Returns the MaterialPropSel value for 'SZ'."""
        return MaterialPropSel('SZ', 11)


class MatrixSel(object):
    """Enumeration of MatrixSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MatrixSel instance for a given integer value."""
        _MAP = {
            0: MatrixSel.Default_Matrix_DEF_1(),
            1: MatrixSel.User_Defined_Matrix(),
        }
        return _MAP.get(v, MatrixSel("unknown_{}".format(v), v))

    @staticmethod
    def Default_Matrix_DEF_1():
        """Returns the MatrixSel value for 'Default Matrix:  DEF.1'."""
        return MatrixSel('Default_Matrix_DEF_1', 0)

    @staticmethod
    def User_Defined_Matrix():
        """Returns the MatrixSel value for 'User Defined Matrix'."""
        return MatrixSel('User_Defined_Matrix', 1)


class MechanModelSel(object):
    """Enumeration of MechanModelSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MechanModelSel instance for a given integer value."""
        _MAP = {
            0: MechanModelSel.PRESSURE(),
            1: MechanModelSel.DELTA_H(),
        }
        return _MAP.get(v, MechanModelSel("unknown_{}".format(v), v))

    @staticmethod
    def PRESSURE():
        """Returns the MechanModelSel value for 'PRESSURE'."""
        return MechanModelSel('PRESSURE', 0)

    @staticmethod
    def DELTA_H():
        """Returns the MechanModelSel value for 'DELTA_H'."""
        return MechanModelSel('DELTA_H', 1)


class MpSwitchSel(object):
    """Enumeration of MpSwitchSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MpSwitchSel instance for a given integer value."""
        _MAP = {
            0: MpSwitchSel.Chapman_Enskog(),
            1: MpSwitchSel.Control_Function(),
            2: MpSwitchSel.Tabular_Function(),
        }
        return _MAP.get(v, MpSwitchSel("unknown_{}".format(v), v))

    @staticmethod
    def Chapman_Enskog():
        """Returns the MpSwitchSel value for 'Chapman-Enskog'."""
        return MpSwitchSel('Chapman_Enskog', 0)

    @staticmethod
    def Control_Function():
        """Returns the MpSwitchSel value for 'Control Function'."""
        return MpSwitchSel('Control_Function', 1)

    @staticmethod
    def Tabular_Function():
        """Returns the MpSwitchSel value for 'Tabular Function'."""
        return MpSwitchSel('Tabular_Function', 2)


class MsgFilSel(object):
    """Enumeration of MsgFilSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the MsgFilSel instance for a given integer value."""
        _MAP = {
            0: MsgFilSel.Disable_Messages(),
            1: MsgFilSel.Write_To_STDOUT_File(),
            2: MsgFilSel.Write_If_Timestep_Completed(),
        }
        return _MAP.get(v, MsgFilSel("unknown_{}".format(v), v))

    @staticmethod
    def Disable_Messages():
        """Returns the MsgFilSel value for 'Disable Messages'."""
        return MsgFilSel('Disable_Messages', 0)

    @staticmethod
    def Write_To_STDOUT_File():
        """Returns the MsgFilSel value for 'Write To STDOUT File'."""
        return MsgFilSel('Write_To_STDOUT_File', 1)

    @staticmethod
    def Write_If_Timestep_Completed():
        """Returns the MsgFilSel value for 'Write If Timestep Completed'."""
        return MsgFilSel('Write_If_Timestep_Completed', 2)


class NLConstCFSel(object):
    """Enumeration of NLConstCFSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NLConstCFSel instance for a given integer value."""
        _MAP = {
            0: NLConstCFSel.Constant(),
            1: NLConstCFSel.Control_Function(),
        }
        return _MAP.get(v, NLConstCFSel("unknown_{}".format(v), v))

    @staticmethod
    def Constant():
        """Returns the NLConstCFSel value for 'Constant'."""
        return NLConstCFSel('Constant', 0)

    @staticmethod
    def Control_Function():
        """Returns the NLConstCFSel value for 'Control Function'."""
        return NLConstCFSel('Control_Function', 1)


class NLEnableSel(object):
    """Enumeration of NLEnableSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NLEnableSel instance for a given integer value."""
        _MAP = {
            0: NLEnableSel.Enable(),
            1: NLEnableSel.Disable(),
        }
        return _MAP.get(v, NLEnableSel("unknown_{}".format(v), v))

    @staticmethod
    def Enable():
        """Returns the NLEnableSel value for 'Enable'."""
        return NLEnableSel('Enable', 0)

    @staticmethod
    def Disable():
        """Returns the NLEnableSel value for 'Disable'."""
        return NLEnableSel('Disable', 1)


class NLYNSel(object):
    """Enumeration of NLYNSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NLYNSel instance for a given integer value."""
        _MAP = {
            0: NLYNSel.No(),
            1: NLYNSel.Yes(),
        }
        return _MAP.get(v, NLYNSel("unknown_{}".format(v), v))

    @staticmethod
    def No():
        """Returns the NLYNSel value for 'No'."""
        return NLYNSel('No', 0)

    @staticmethod
    def Yes():
        """Returns the NLYNSel value for 'Yes'."""
        return NLYNSel('Yes', 1)


class NLYesNoSel(object):
    """Enumeration of NLYesNoSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NLYesNoSel instance for a given integer value."""
        _MAP = {
            0: NLYesNoSel.Steady_State_Initialization(),
            1: NLYesNoSel.No_Steady_State_Calc(),
        }
        return _MAP.get(v, NLYesNoSel("unknown_{}".format(v), v))

    @staticmethod
    def Steady_State_Initialization():
        """Returns the NLYesNoSel value for 'Steady State Initialization'."""
        return NLYesNoSel('Steady_State_Initialization', 0)

    @staticmethod
    def No_Steady_State_Calc():
        """Returns the NLYesNoSel value for 'No Steady State Calc.'."""
        return NLYesNoSel('No_Steady_State_Calc', 1)


class NetworkWaterTypeSel(object):
    """Enumeration of NetworkWaterTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NetworkWaterTypeSel instance for a given integer value."""
        _MAP = {
            0: NetworkWaterTypeSel.NONE(),
            1: NetworkWaterTypeSel.Control_Function(),
            2: NetworkWaterTypeSel.Tabular_Function(),
        }
        return _MAP.get(v, NetworkWaterTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def NONE():
        """Returns the NetworkWaterTypeSel value for 'NONE'."""
        return NetworkWaterTypeSel('NONE', 0)

    @staticmethod
    def Control_Function():
        """Returns the NetworkWaterTypeSel value for 'Control Function'."""
        return NetworkWaterTypeSel('Control_Function', 1)

    @staticmethod
    def Tabular_Function():
        """Returns the NetworkWaterTypeSel value for 'Tabular Function'."""
        return NetworkWaterTypeSel('Tabular_Function', 2)


class NewOldSel(object):
    """Enumeration of NewOldSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NewOldSel instance for a given integer value."""
        _MAP = {
            0: NewOldSel.Old(),
            1: NewOldSel.New(),
        }
        return _MAP.get(v, NewOldSel("unknown_{}".format(v), v))

    @staticmethod
    def Old():
        """Returns the NewOldSel value for 'Old'."""
        return NewOldSel('Old', 0)

    @staticmethod
    def New():
        """Returns the NewOldSel value for 'New'."""
        return NewOldSel('New', 1)


class NfdtpiTypeSel(object):
    """Enumeration of NfdtpiTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NfdtpiTypeSel instance for a given integer value."""
        _MAP = {
            1: NfdtpiTypeSel.Tabular_Function(),
            2: NfdtpiTypeSel.External_Data_File(),
        }
        return _MAP.get(v, NfdtpiTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Tabular_Function():
        """Returns the NfdtpiTypeSel value for 'Tabular Function'."""
        return NfdtpiTypeSel('Tabular_Function', 1)

    @staticmethod
    def External_Data_File():
        """Returns the NfdtpiTypeSel value for 'External Data File'."""
        return NfdtpiTypeSel('External_Data_File', 2)


class NfdtpoTypeSel(object):
    """Enumeration of NfdtpoTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NfdtpoTypeSel instance for a given integer value."""
        _MAP = {
            0: NfdtpoTypeSel.Out_Transfer_Process(),
            1: NfdtpoTypeSel.Number_of_source_materials(),
        }
        return _MAP.get(v, NfdtpoTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Out_Transfer_Process():
        """Returns the NfdtpoTypeSel value for 'Out Transfer Process'."""
        return NfdtpoTypeSel('Out_Transfer_Process', 0)

    @staticmethod
    def Number_of_source_materials():
        """Returns the NfdtpoTypeSel value for 'Number of source materials'."""
        return NfdtpoTypeSel('Number_of_source_materials', 1)


class NinpTypeSel(object):
    """Enumeration of NinpTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NinpTypeSel instance for a given integer value."""
        _MAP = {
            0: NinpTypeSel.Ninp_Core_Cell(),
            1: NinpTypeSel.Ninp_Fraction(),
        }
        return _MAP.get(v, NinpTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Ninp_Core_Cell():
        """Returns the NinpTypeSel value for 'Ninp Core Cell'."""
        return NinpTypeSel('Ninp_Core_Cell', 0)

    @staticmethod
    def Ninp_Fraction():
        """Returns the NinpTypeSel value for 'Ninp Fraction'."""
        return NinpTypeSel('Ninp_Fraction', 1)


class NovcTypeSel(object):
    """Enumeration of NovcTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NovcTypeSel instance for a given integer value."""
        _MAP = {
            0: NovcTypeSel.Stop_calculation_if_rupture_occurs(),
            1: NovcTypeSel.Continue_calculation_if_rupture_occurs(),
            2: NovcTypeSel.Use_cavity_to_retrieve_rupture_overflow(),
        }
        return _MAP.get(v, NovcTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Stop_calculation_if_rupture_occurs():
        """Returns the NovcTypeSel value for 'Stop calculation if rupture occurs'."""
        return NovcTypeSel('Stop_calculation_if_rupture_occurs', 0)

    @staticmethod
    def Continue_calculation_if_rupture_occurs():
        """Returns the NovcTypeSel value for 'Continue calculation if rupture occurs'."""
        return NovcTypeSel('Continue_calculation_if_rupture_occurs', 1)

    @staticmethod
    def Use_cavity_to_retrieve_rupture_overflow():
        """Returns the NovcTypeSel value for 'Use cavity to retrieve rupture overflow'."""
        return NovcTypeSel('Use_cavity_to_retrieve_rupture_overflow', 2)


class NovcValSel(object):
    """Enumeration of NovcValSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NovcValSel instance for a given integer value."""
        _MAP = {
            0: NovcValSel.Stop_calculation(),
            1: NovcValSel.Continue_calculation(),
        }
        return _MAP.get(v, NovcValSel("unknown_{}".format(v), v))

    @staticmethod
    def Stop_calculation():
        """Returns the NovcValSel value for 'Stop calculation'."""
        return NovcValSel('Stop_calculation', 0)

    @staticmethod
    def Continue_calculation():
        """Returns the NovcValSel value for 'Continue calculation'."""
        return NovcValSel('Continue_calculation', 1)


class NtfbdSel(object):
    """Enumeration of NtfbdSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NtfbdSel instance for a given integer value."""
        _MAP = {
            0: NtfbdSel.Keep_Constant(),
            1: NtfbdSel.Extrapolate(),
            2: NtfbdSel.Fail(),
        }
        return _MAP.get(v, NtfbdSel("unknown_{}".format(v), v))

    @staticmethod
    def Keep_Constant():
        """Returns the NtfbdSel value for 'Keep Constant'."""
        return NtfbdSel('Keep_Constant', 0)

    @staticmethod
    def Extrapolate():
        """Returns the NtfbdSel value for 'Extrapolate'."""
        return NtfbdSel('Extrapolate', 1)

    @staticmethod
    def Fail():
        """Returns the NtfbdSel value for 'Fail'."""
        return NtfbdSel('Fail', 2)


class NunitsSel(object):
    """Enumeration of NunitsSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the NunitsSel instance for a given integer value."""
        _MAP = {
            0: NunitsSel.S_I(),
            1: NunitsSel.British(),
        }
        return _MAP.get(v, NunitsSel("unknown_{}".format(v), v))

    @staticmethod
    def S_I():
        """Returns the NunitsSel value for 'S.I.'."""
        return NunitsSel('S_I', 0)

    @staticmethod
    def British():
        """Returns the NunitsSel value for 'British'."""
        return NunitsSel('British', 1)


class OffOnSel(object):
    """Enumeration of OffOnSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the OffOnSel instance for a given integer value."""
        _MAP = {
            0: OffOnSel.Off(),
            1: OffOnSel.On(),
        }
        return _MAP.get(v, OffOnSel("unknown_{}".format(v), v))

    @staticmethod
    def Off():
        """Returns the OffOnSel value for 'Off'."""
        return OffOnSel('Off', 0)

    @staticmethod
    def On():
        """Returns the OffOnSel value for 'On'."""
        return OffOnSel('On', 1)


class OptionalOffOnSel(object):
    """Enumeration of OptionalOffOnSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the OptionalOffOnSel instance for a given integer value."""
        _MAP = {
            0: OptionalOffOnSel.Off(),
            1: OptionalOffOnSel.On(),
        }
        return _MAP.get(v, OptionalOffOnSel("unknown_{}".format(v), v))

    @staticmethod
    def Off():
        """Returns the OptionalOffOnSel value for 'Off'."""
        return OptionalOffOnSel('Off', 0)

    @staticmethod
    def On():
        """Returns the OptionalOffOnSel value for 'On'."""
        return OptionalOffOnSel('On', 1)


class OptionalYesNoSel(object):
    """Enumeration of OptionalYesNoSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the OptionalYesNoSel instance for a given integer value."""
        _MAP = {
            0: OptionalYesNoSel.Yes(),
            1: OptionalYesNoSel.No(),
        }
        return _MAP.get(v, OptionalYesNoSel("unknown_{}".format(v), v))

    @staticmethod
    def Yes():
        """Returns the OptionalYesNoSel value for 'Yes'."""
        return OptionalYesNoSel('Yes', 0)

    @staticmethod
    def No():
        """Returns the OptionalYesNoSel value for 'No'."""
        return OptionalYesNoSel('No', 1)


class OxidStructSel(object):
    """Enumeration of OxidStructSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the OxidStructSel instance for a given integer value."""
        _MAP = {
            0: OxidStructSel.No_Control_Function(),
            1: OxidStructSel.Reference_Cell_CF_if_available(),
            2: OxidStructSel.Specify_Control_Function(),
        }
        return _MAP.get(v, OxidStructSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Control_Function():
        """Returns the OxidStructSel value for 'No Control Function'."""
        return OxidStructSel('No_Control_Function', 0)

    @staticmethod
    def Reference_Cell_CF_if_available():
        """Returns the OxidStructSel value for 'Reference Cell CF ( if available )'."""
        return OxidStructSel('Reference_Cell_CF_if_available', 1)

    @staticmethod
    def Specify_Control_Function():
        """Returns the OxidStructSel value for 'Specify Control Function'."""
        return OxidStructSel('Specify_Control_Function', 2)


class OxidePhaseSel(object):
    """Enumeration of OxidePhaseSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the OxidePhaseSel instance for a given integer value."""
        _MAP = {
            0: OxidePhaseSel.Use_split_calculated_by_MELCOR(),
            1: OxidePhaseSel.Total_decay_heat_control_function(),
        }
        return _MAP.get(v, OxidePhaseSel("unknown_{}".format(v), v))

    @staticmethod
    def Use_split_calculated_by_MELCOR():
        """Returns the OxidePhaseSel value for 'Use split calculated by MELCOR'."""
        return OxidePhaseSel('Use_split_calculated_by_MELCOR', 0)

    @staticmethod
    def Total_decay_heat_control_function():
        """Returns the OxidePhaseSel value for 'Total decay heat control function'."""
        return OxidePhaseSel('Total_decay_heat_control_function', 1)


class PNTOptSel(object):
    """Enumeration of PNTOptSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the PNTOptSel instance for a given integer value."""
        _MAP = {
            0: PNTOptSel.SIMP(),
            1: PNTOptSel.EXP(),
        }
        return _MAP.get(v, PNTOptSel("unknown_{}".format(v), v))

    @staticmethod
    def SIMP():
        """Returns the PNTOptSel value for 'SIMP'."""
        return PNTOptSel('SIMP', 0)

    @staticmethod
    def EXP():
        """Returns the PNTOptSel value for 'EXP'."""
        return PNTOptSel('EXP', 1)


class PlotEditSel(object):
    """Enumeration of PlotEditSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the PlotEditSel instance for a given integer value."""
        _MAP = {
            0: PlotEditSel.Control_Function(),
            -1: PlotEditSel.Start_and_End(),
            -2: PlotEditSel.No_Plot_Edits(),
        }
        return _MAP.get(v, PlotEditSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function():
        """Returns the PlotEditSel value for 'Control Function'."""
        return PlotEditSel('Control_Function', 0)

    @staticmethod
    def Start_and_End():
        """Returns the PlotEditSel value for 'Start and End'."""
        return PlotEditSel('Start_and_End', -1)

    @staticmethod
    def No_Plot_Edits():
        """Returns the PlotEditSel value for 'No Plot Edits'."""
        return PlotEditSel('No_Plot_Edits', -2)


class PoolTypeSel(object):
    """Enumeration of PoolTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the PoolTypeSel instance for a given integer value."""
        _MAP = {
            0: PoolTypeSel.Define_Initial_Mass(),
            1: PoolTypeSel.Define_Pool_Volume(),
            2: PoolTypeSel.Define_Pool_Elevation(),
        }
        return _MAP.get(v, PoolTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Define_Initial_Mass():
        """Returns the PoolTypeSel value for 'Define Initial Mass'."""
        return PoolTypeSel('Define_Initial_Mass', 0)

    @staticmethod
    def Define_Pool_Volume():
        """Returns the PoolTypeSel value for 'Define Pool Volume'."""
        return PoolTypeSel('Define_Pool_Volume', 1)

    @staticmethod
    def Define_Pool_Elevation():
        """Returns the PoolTypeSel value for 'Define Pool Elevation'."""
        return PoolTypeSel('Define_Pool_Elevation', 2)


class PostionTransportSel(object):
    """Enumeration of PostionTransportSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the PostionTransportSel instance for a given integer value."""
        _MAP = {
            1: PostionTransportSel.Poison_Flag_Value_1(),
            2: PostionTransportSel.Poison_Flag_Value_2(),
        }
        return _MAP.get(v, PostionTransportSel("unknown_{}".format(v), v))

    @staticmethod
    def Poison_Flag_Value_1():
        """Returns the PostionTransportSel value for 'Poison Flag Value - 1'."""
        return PostionTransportSel('Poison_Flag_Value_1', 1)

    @staticmethod
    def Poison_Flag_Value_2():
        """Returns the PostionTransportSel value for 'Poison Flag Value - 2'."""
        return PostionTransportSel('Poison_Flag_Value_2', 2)


class PumpPhaseSel(object):
    """Enumeration of PumpPhaseSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the PumpPhaseSel instance for a given integer value."""
        _MAP = {
            0: PumpPhaseSel.Single_Phase(),
            1: PumpPhaseSel.Two_Phase(),
        }
        return _MAP.get(v, PumpPhaseSel("unknown_{}".format(v), v))

    @staticmethod
    def Single_Phase():
        """Returns the PumpPhaseSel value for 'Single Phase'."""
        return PumpPhaseSel('Single_Phase', 0)

    @staticmethod
    def Two_Phase():
        """Returns the PumpPhaseSel value for 'Two Phase'."""
        return PumpPhaseSel('Two_Phase', 1)


class PumpSpeedCompSel(object):
    """Enumeration of PumpSpeedCompSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the PumpSpeedCompSel instance for a given integer value."""
        _MAP = {
            0: PumpSpeedCompSel.CFTF_ONLY(),
            1: PumpSpeedCompSel.CFTF_TIE(),
            2: PumpSpeedCompSel.TIE(),
        }
        return _MAP.get(v, PumpSpeedCompSel("unknown_{}".format(v), v))

    @staticmethod
    def CFTF_ONLY():
        """Returns the PumpSpeedCompSel value for 'CFTF-ONLY'."""
        return PumpSpeedCompSel('CFTF_ONLY', 0)

    @staticmethod
    def CFTF_TIE():
        """Returns the PumpSpeedCompSel value for 'CFTF-TIE'."""
        return PumpSpeedCompSel('CFTF_TIE', 1)

    @staticmethod
    def TIE():
        """Returns the PumpSpeedCompSel value for 'TIE'."""
        return PumpSpeedCompSel('TIE', 2)


class RNActiveSel(object):
    """Enumeration of RNActiveSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNActiveSel instance for a given integer value."""
        _MAP = {
            0: RNActiveSel.RN_package_Active(),
            1: RNActiveSel.RN_package_Inactive(),
        }
        return _MAP.get(v, RNActiveSel("unknown_{}".format(v), v))

    @staticmethod
    def RN_package_Active():
        """Returns the RNActiveSel value for 'RN package Active'."""
        return RNActiveSel('RN_package_Active', 0)

    @staticmethod
    def RN_package_Inactive():
        """Returns the RNActiveSel value for 'RN package Inactive'."""
        return RNActiveSel('RN_package_Inactive', 1)


class RNCladdingSel(object):
    """Enumeration of RNCladdingSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNCladdingSel instance for a given integer value."""
        _MAP = {
            -1: RNCladdingSel.Reference_Cell(),
            1: RNCladdingSel.Material_Class(),
        }
        return _MAP.get(v, RNCladdingSel("unknown_{}".format(v), v))

    @staticmethod
    def Reference_Cell():
        """Returns the RNCladdingSel value for 'Reference Cell'."""
        return RNCladdingSel('Reference_Cell', -1)

    @staticmethod
    def Material_Class():
        """Returns the RNCladdingSel value for 'Material Class'."""
        return RNCladdingSel('Material_Class', 1)


class RNClassTypeSel(object):
    """Enumeration of RNClassTypeSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNClassTypeSel instance for a given integer value."""
        _MAP = {
            0: RNClassTypeSel.Default(),
            1: RNClassTypeSel.Custom(),
        }
        return _MAP.get(v, RNClassTypeSel("unknown_{}".format(v), v))

    @staticmethod
    def Default():
        """Returns the RNClassTypeSel value for 'Default'."""
        return RNClassTypeSel('Default', 0)

    @staticmethod
    def Custom():
        """Returns the RNClassTypeSel value for 'Custom'."""
        return RNClassTypeSel('Custom', 1)


class RNCoatSel(object):
    """Enumeration of RNCoatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNCoatSel instance for a given integer value."""
        _MAP = {
            0: RNCoatSel.No_Coating(),
            1: RNCoatSel.Painted_Surface(),
            2: RNCoatSel.Steel_Surface(),
            3: RNCoatSel.Concrete_Surface(),
        }
        return _MAP.get(v, RNCoatSel("unknown_{}".format(v), v))

    @staticmethod
    def No_Coating():
        """Returns the RNCoatSel value for 'No Coating'."""
        return RNCoatSel('No_Coating', 0)

    @staticmethod
    def Painted_Surface():
        """Returns the RNCoatSel value for 'Painted Surface'."""
        return RNCoatSel('Painted_Surface', 1)

    @staticmethod
    def Steel_Surface():
        """Returns the RNCoatSel value for 'Steel Surface'."""
        return RNCoatSel('Steel_Surface', 2)

    @staticmethod
    def Concrete_Surface():
        """Returns the RNCoatSel value for 'Concrete Surface'."""
        return RNCoatSel('Concrete_Surface', 3)


class RNFpplsSel(object):
    """Enumeration of RNFpplsSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNFpplsSel instance for a given integer value."""
        _MAP = {
            0: RNFpplsSel.From_Volume(),
            1: RNFpplsSel.To_Volume(),
            2: RNFpplsSel.Cavity_Pool(),
        }
        return _MAP.get(v, RNFpplsSel("unknown_{}".format(v), v))

    @staticmethod
    def From_Volume():
        """Returns the RNFpplsSel value for 'From Volume'."""
        return RNFpplsSel('From_Volume', 0)

    @staticmethod
    def To_Volume():
        """Returns the RNFpplsSel value for 'To Volume'."""
        return RNFpplsSel('To_Volume', 1)

    @staticmethod
    def Cavity_Pool():
        """Returns the RNFpplsSel value for 'Cavity Pool'."""
        return RNFpplsSel('Cavity_Pool', 2)


class RNIcoeffSel(object):
    """Enumeration of RNIcoeffSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNIcoeffSel instance for a given integer value."""
        _MAP = {
            -1: RNIcoeffSel.User_Defined_Coefficients(),
            0: RNIcoeffSel.Calculate_Coefficients(),
            1: RNIcoeffSel.Calculate_and_Write(),
        }
        return _MAP.get(v, RNIcoeffSel("unknown_{}".format(v), v))

    @staticmethod
    def User_Defined_Coefficients():
        """Returns the RNIcoeffSel value for 'User Defined Coefficients'."""
        return RNIcoeffSel('User_Defined_Coefficients', -1)

    @staticmethod
    def Calculate_Coefficients():
        """Returns the RNIcoeffSel value for 'Calculate Coefficients'."""
        return RNIcoeffSel('Calculate_Coefficients', 0)

    @staticmethod
    def Calculate_and_Write():
        """Returns the RNIcoeffSel value for 'Calculate and Write'."""
        return RNIcoeffSel('Calculate_and_Write', 1)


class RNIcondSel(object):
    """Enumeration of RNIcondSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNIcondSel instance for a given integer value."""
        _MAP = {
            0: RNIcondSel.All_Aerosols(),
            1: RNIcondSel.Water_Only(),
        }
        return _MAP.get(v, RNIcondSel("unknown_{}".format(v), v))

    @staticmethod
    def All_Aerosols():
        """Returns the RNIcondSel value for 'All Aerosols'."""
        return RNIcondSel('All_Aerosols', 0)

    @staticmethod
    def Water_Only():
        """Returns the RNIcondSel value for 'Water Only'."""
        return RNIcondSel('Water_Only', 1)


class RNIdistSel(object):
    """Enumeration of RNIdistSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNIdistSel instance for a given integer value."""
        _MAP = {
            1: RNIdistSel.Uniform_Source(),
            2: RNIdistSel.Log_Normal_Distribution(),
        }
        return _MAP.get(v, RNIdistSel("unknown_{}".format(v), v))

    @staticmethod
    def Uniform_Source():
        """Returns the RNIdistSel value for 'Uniform Source'."""
        return RNIdistSel('Uniform_Source', 1)

    @staticmethod
    def Log_Normal_Distribution():
        """Returns the RNIdistSel value for 'Log-Normal Distribution'."""
        return RNIdistSel('Log_Normal_Distribution', 2)


class RNIdistpSel(object):
    """Enumeration of RNIdistpSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNIdistpSel instance for a given integer value."""
        _MAP = {
            1: RNIdistpSel.Uniform_Source(),
            2: RNIdistpSel.Log_Normal_Distribution(),
            3: RNIdistpSel.Sectional_Distribution(),
        }
        return _MAP.get(v, RNIdistpSel("unknown_{}".format(v), v))

    @staticmethod
    def Uniform_Source():
        """Returns the RNIdistpSel value for 'Uniform Source'."""
        return RNIdistpSel('Uniform_Source', 1)

    @staticmethod
    def Log_Normal_Distribution():
        """Returns the RNIdistpSel value for 'Log-Normal Distribution'."""
        return RNIdistpSel('Log_Normal_Distribution', 2)

    @staticmethod
    def Sectional_Distribution():
        """Returns the RNIdistpSel value for 'Sectional Distribution'."""
        return RNIdistpSel('Sectional_Distribution', 3)


class RNIphsSel(object):
    """Enumeration of RNIphsSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNIphsSel instance for a given integer value."""
        _MAP = {
            1: RNIphsSel.Liquid(),
            2: RNIphsSel.Vapor(),
        }
        return _MAP.get(v, RNIphsSel("unknown_{}".format(v), v))

    @staticmethod
    def Liquid():
        """Returns the RNIphsSel value for 'Liquid'."""
        return RNIphsSel('Liquid', 1)

    @staticmethod
    def Vapor():
        """Returns the RNIphsSel value for 'Vapor'."""
        return RNIphsSel('Vapor', 2)


class RNItypSel(object):
    """Enumeration of RNItypSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNItypSel instance for a given integer value."""
        _MAP = {
            0: RNItypSel.Ceiling(),
            1: RNItypSel.Vertical_Wall(),
            2: RNItypSel.Floor(),
            3: RNItypSel.Inactive(),
        }
        return _MAP.get(v, RNItypSel("unknown_{}".format(v), v))

    @staticmethod
    def Ceiling():
        """Returns the RNItypSel value for 'Ceiling'."""
        return RNItypSel('Ceiling', 0)

    @staticmethod
    def Vertical_Wall():
        """Returns the RNItypSel value for 'Vertical Wall'."""
        return RNItypSel('Vertical_Wall', 1)

    @staticmethod
    def Floor():
        """Returns the RNItypSel value for 'Floor'."""
        return RNItypSel('Floor', 2)

    @staticmethod
    def Inactive():
        """Returns the RNItypSel value for 'Inactive'."""
        return RNItypSel('Inactive', 3)


class RNMassKeySel(object):
    """Enumeration of RNMassKeySel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNMassKeySel instance for a given integer value."""
        _MAP = {
            0: RNMassKeySel.Total_Mass(),
            1: RNMassKeySel.Radioactive_Mass(),
        }
        return _MAP.get(v, RNMassKeySel("unknown_{}".format(v), v))

    @staticmethod
    def Total_Mass():
        """Returns the RNMassKeySel value for 'Total Mass'."""
        return RNMassKeySel('Total_Mass', 0)

    @staticmethod
    def Radioactive_Mass():
        """Returns the RNMassKeySel value for 'Radioactive Mass'."""
        return RNMassKeySel('Radioactive_Mass', 1)


class RNMventSel(object):
    """Enumeration of RNMventSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNMventSel instance for a given integer value."""
        _MAP = {
            1: RNMventSel.Multi_Hole(),
            2: RNMventSel.Downcomer(),
            3: RNMventSel.Horizontal(),
        }
        return _MAP.get(v, RNMventSel("unknown_{}".format(v), v))

    @staticmethod
    def Multi_Hole():
        """Returns the RNMventSel value for 'Multi-Hole'."""
        return RNMventSel('Multi_Hole', 1)

    @staticmethod
    def Downcomer():
        """Returns the RNMventSel value for 'Downcomer'."""
        return RNMventSel('Downcomer', 2)

    @staticmethod
    def Horizontal():
        """Returns the RNMventSel value for 'Horizontal'."""
        return RNMventSel('Horizontal', 3)


class RNNinpFlagSel(object):
    """Enumeration of RNNinpFlagSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNNinpFlagSel instance for a given integer value."""
        _MAP = {
            -1: RNNinpFlagSel.Reference_Cell(),
            0: RNNinpFlagSel.Total_Mass(),
            1: RNNinpFlagSel.Material_Class(),
        }
        return _MAP.get(v, RNNinpFlagSel("unknown_{}".format(v), v))

    @staticmethod
    def Reference_Cell():
        """Returns the RNNinpFlagSel value for 'Reference Cell'."""
        return RNNinpFlagSel('Reference_Cell', -1)

    @staticmethod
    def Total_Mass():
        """Returns the RNNinpFlagSel value for 'Total Mass'."""
        return RNNinpFlagSel('Total_Mass', 0)

    @staticmethod
    def Material_Class():
        """Returns the RNNinpFlagSel value for 'Material Class'."""
        return RNNinpFlagSel('Material_Class', 1)


class RNOptionSel(object):
    """Enumeration of RNOptionSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNOptionSel instance for a given integer value."""
        _MAP = {
            0: RNOptionSel.Cavity(),
            1: RNOptionSel.Core_Cell(),
        }
        return _MAP.get(v, RNOptionSel("unknown_{}".format(v), v))

    @staticmethod
    def Cavity():
        """Returns the RNOptionSel value for 'Cavity'."""
        return RNOptionSel('Cavity', 0)

    @staticmethod
    def Core_Cell():
        """Returns the RNOptionSel value for 'Core Cell'."""
        return RNOptionSel('Core_Cell', 1)


class RNScrubSel(object):
    """Enumeration of RNScrubSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNScrubSel instance for a given integer value."""
        _MAP = {
            0: RNScrubSel.RN_scrubbing_of_aerosols_and_iodine_vapor_is_active(),
            -1: RNScrubSel.all_RN_scrubbing_is_inactive(),
            -2: RNScrubSel.RN_scrubbing_of_aerosols_only_is_active(),
            -3: RNScrubSel.RN_scrubbing_of_iodine_vapor_only_is_active(),
        }
        return _MAP.get(v, RNScrubSel("unknown_{}".format(v), v))

    @staticmethod
    def RN_scrubbing_of_aerosols_and_iodine_vapor_is_active():
        """Returns the RNScrubSel value for 'RN scrubbing of aerosols and iodine vapor is active'."""
        return RNScrubSel('RN_scrubbing_of_aerosols_and_iodine_vapor_is_active', 0)

    @staticmethod
    def all_RN_scrubbing_is_inactive():
        """Returns the RNScrubSel value for 'all RN scrubbing is inactive'."""
        return RNScrubSel('all_RN_scrubbing_is_inactive', -1)

    @staticmethod
    def RN_scrubbing_of_aerosols_only_is_active():
        """Returns the RNScrubSel value for 'RN scrubbing of aerosols only is active'."""
        return RNScrubSel('RN_scrubbing_of_aerosols_only_is_active', -2)

    @staticmethod
    def RN_scrubbing_of_iodine_vapor_only_is_active():
        """Returns the RNScrubSel value for 'RN scrubbing of iodine vapor only is active'."""
        return RNScrubSel('RN_scrubbing_of_iodine_vapor_only_is_active', -3)


class RNVarParamSel(object):
    """Enumeration of RNVarParamSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RNVarParamSel instance for a given integer value."""
        _MAP = {
            1: RNVarParamSel.Total_Mass(),
            2: RNVarParamSel.Radioactive_Mass(),
        }
        return _MAP.get(v, RNVarParamSel("unknown_{}".format(v), v))

    @staticmethod
    def Total_Mass():
        """Returns the RNVarParamSel value for 'Total Mass'."""
        return RNVarParamSel('Total_Mass', 1)

    @staticmethod
    def Radioactive_Mass():
        """Returns the RNVarParamSel value for 'Radioactive Mass'."""
        return RNVarParamSel('Radioactive_Mass', 2)


class ReactIstatSel(object):
    """Enumeration of ReactIstatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ReactIstatSel instance for a given integer value."""
        _MAP = {
            0: ReactIstatSel.Heat_Structure(),
            1: ReactIstatSel.Aerosol_Vapor(),
            2: ReactIstatSel.Liquid_Pool(),
        }
        return _MAP.get(v, ReactIstatSel("unknown_{}".format(v), v))

    @staticmethod
    def Heat_Structure():
        """Returns the ReactIstatSel value for 'Heat Structure'."""
        return ReactIstatSel('Heat_Structure', 0)

    @staticmethod
    def Aerosol_Vapor():
        """Returns the ReactIstatSel value for 'Aerosol Vapor'."""
        return ReactIstatSel('Aerosol_Vapor', 1)

    @staticmethod
    def Liquid_Pool():
        """Returns the ReactIstatSel value for 'Liquid Pool'."""
        return ReactIstatSel('Liquid_Pool', 2)


class ReadWriteEnabledSel(object):
    """Enumeration of ReadWriteEnabledSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ReadWriteEnabledSel instance for a given integer value."""
        _MAP = {
            0: ReadWriteEnabledSel.Disable_read_write(),
            1: ReadWriteEnabledSel.Enable_read_write(),
        }
        return _MAP.get(v, ReadWriteEnabledSel("unknown_{}".format(v), v))

    @staticmethod
    def Disable_read_write():
        """Returns the ReadWriteEnabledSel value for 'Disable read/write'."""
        return ReadWriteEnabledSel('Disable_read_write', 0)

    @staticmethod
    def Enable_read_write():
        """Returns the ReadWriteEnabledSel value for 'Enable read/write'."""
        return ReadWriteEnabledSel('Enable_read_write', 1)


class ReadWriteSel(object):
    """Enumeration of ReadWriteSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ReadWriteSel instance for a given integer value."""
        _MAP = {
            0: ReadWriteSel.Read(),
            1: ReadWriteSel.Write(),
        }
        return _MAP.get(v, ReadWriteSel("unknown_{}".format(v), v))

    @staticmethod
    def Read():
        """Returns the ReadWriteSel value for 'Read'."""
        return ReadWriteSel('Read', 0)

    @staticmethod
    def Write():
        """Returns the ReadWriteSel value for 'Write'."""
        return ReadWriteSel('Write', 1)


class RuptureSel(object):
    """Enumeration of RuptureSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the RuptureSel instance for a given integer value."""
        _MAP = {
            0: RuptureSel.Disabled(),
            1: RuptureSel.Axial(),
            2: RuptureSel.Radial(),
            3: RuptureSel.Control_Function(),
        }
        return _MAP.get(v, RuptureSel("unknown_{}".format(v), v))

    @staticmethod
    def Disabled():
        """Returns the RuptureSel value for 'Disabled'."""
        return RuptureSel('Disabled', 0)

    @staticmethod
    def Axial():
        """Returns the RuptureSel value for 'Axial'."""
        return RuptureSel('Axial', 1)

    @staticmethod
    def Radial():
        """Returns the RuptureSel value for 'Radial'."""
        return RuptureSel('Radial', 2)

    @staticmethod
    def Control_Function():
        """Returns the RuptureSel value for 'Control Function'."""
        return RuptureSel('Control_Function', 3)


class ShapeplSel(object):
    """Enumeration of ShapeplSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the ShapeplSel instance for a given integer value."""
        _MAP = {
            0: ShapeplSel.Exclude(),
            1: ShapeplSel.Include(),
        }
        return _MAP.get(v, ShapeplSel("unknown_{}".format(v), v))

    @staticmethod
    def Exclude():
        """Returns the ShapeplSel value for 'Exclude'."""
        return ShapeplSel('Exclude', 0)

    @staticmethod
    def Include():
        """Returns the ShapeplSel value for 'Include'."""
        return ShapeplSel('Include', 1)


class SourceFogSel(object):
    """Enumeration of SourceFogSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SourceFogSel instance for a given integer value."""
        _MAP = {
            0: SourceFogSel.Distribute_Directly(),
            1: SourceFogSel.Calculate_Distribution(),
        }
        return _MAP.get(v, SourceFogSel("unknown_{}".format(v), v))

    @staticmethod
    def Distribute_Directly():
        """Returns the SourceFogSel value for 'Distribute Directly'."""
        return SourceFogSel('Distribute_Directly', 0)

    @staticmethod
    def Calculate_Distribution():
        """Returns the SourceFogSel value for 'Calculate Distribution'."""
        return SourceFogSel('Calculate_Distribution', 1)


class SourceIesflgSel(object):
    """Enumeration of SourceIesflgSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SourceIesflgSel instance for a given integer value."""
        _MAP = {
            0: SourceIesflgSel.Cumulative_Source(),
            2: SourceIesflgSel.Source_Rate(),
            4: SourceIesflgSel.Source_per_Mass(),
            6: SourceIesflgSel.Source_per_Volume(),
            8: SourceIesflgSel.Material_Enthalpy(),
        }
        return _MAP.get(v, SourceIesflgSel("unknown_{}".format(v), v))

    @staticmethod
    def Cumulative_Source():
        """Returns the SourceIesflgSel value for 'Cumulative Source'."""
        return SourceIesflgSel('Cumulative_Source', 0)

    @staticmethod
    def Source_Rate():
        """Returns the SourceIesflgSel value for 'Source Rate'."""
        return SourceIesflgSel('Source_Rate', 2)

    @staticmethod
    def Source_per_Mass():
        """Returns the SourceIesflgSel value for 'Source per Mass'."""
        return SourceIesflgSel('Source_per_Mass', 4)

    @staticmethod
    def Source_per_Volume():
        """Returns the SourceIesflgSel value for 'Source per Volume'."""
        return SourceIesflgSel('Source_per_Volume', 6)

    @staticmethod
    def Material_Enthalpy():
        """Returns the SourceIesflgSel value for 'Material Enthalpy'."""
        return SourceIesflgSel('Material_Enthalpy', 8)


class SourceIsautoptSel(object):
    """Enumeration of SourceIsautoptSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SourceIsautoptSel instance for a given integer value."""
        _MAP = {
            0: SourceIsautoptSel.Control_Function(),
            1: SourceIsautoptSel.Constant(),
            2: SourceIsautoptSel.Sensitivity_Coefficient(),
        }
        return _MAP.get(v, SourceIsautoptSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function():
        """Returns the SourceIsautoptSel value for 'Control Function'."""
        return SourceIsautoptSel('Control_Function', 0)

    @staticmethod
    def Constant():
        """Returns the SourceIsautoptSel value for 'Constant'."""
        return SourceIsautoptSel('Constant', 1)

    @staticmethod
    def Sensitivity_Coefficient():
        """Returns the SourceIsautoptSel value for 'Sensitivity Coefficient'."""
        return SourceIsautoptSel('Sensitivity_Coefficient', 2)


class SourceTyp2Sel(object):
    """Enumeration of SourceTyp2Sel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SourceTyp2Sel instance for a given integer value."""
        _MAP = {
            0: SourceTyp2Sel.Atmosphere_Energy(),
            1: SourceTyp2Sel.Pool_Energy(),
            2: SourceTyp2Sel.Mass(),
            3: SourceTyp2Sel.File(),
            4: SourceTyp2Sel.Water_Energy(),
            5: SourceTyp2Sel.Water_Enthalpy(),
        }
        return _MAP.get(v, SourceTyp2Sel("unknown_{}".format(v), v))

    @staticmethod
    def Atmosphere_Energy():
        """Returns the SourceTyp2Sel value for 'Atmosphere Energy'."""
        return SourceTyp2Sel('Atmosphere_Energy', 0)

    @staticmethod
    def Pool_Energy():
        """Returns the SourceTyp2Sel value for 'Pool Energy'."""
        return SourceTyp2Sel('Pool_Energy', 1)

    @staticmethod
    def Mass():
        """Returns the SourceTyp2Sel value for 'Mass'."""
        return SourceTyp2Sel('Mass', 2)

    @staticmethod
    def File():
        """Returns the SourceTyp2Sel value for 'File'."""
        return SourceTyp2Sel('File', 3)

    @staticmethod
    def Water_Energy():
        """Returns the SourceTyp2Sel value for 'Water Energy'."""
        return SourceTyp2Sel('Water_Energy', 4)

    @staticmethod
    def Water_Enthalpy():
        """Returns the SourceTyp2Sel value for 'Water Enthalpy'."""
        return SourceTyp2Sel('Water_Enthalpy', 5)


class SprayKeydtSel(object):
    """Enumeration of SprayKeydtSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SprayKeydtSel instance for a given integer value."""
        _MAP = {
            -1: SprayKeydtSel.Out_Transfer_Process(),
            0: SprayKeydtSel.Constant(),
            1: SprayKeydtSel.Control_Function(),
        }
        return _MAP.get(v, SprayKeydtSel("unknown_{}".format(v), v))

    @staticmethod
    def Out_Transfer_Process():
        """Returns the SprayKeydtSel value for 'Out Transfer Process'."""
        return SprayKeydtSel('Out_Transfer_Process', -1)

    @staticmethod
    def Constant():
        """Returns the SprayKeydtSel value for 'Constant'."""
        return SprayKeydtSel('Constant', 0)

    @staticmethod
    def Control_Function():
        """Returns the SprayKeydtSel value for 'Control Function'."""
        return SprayKeydtSel('Control_Function', 1)


class SsMetaSel(object):
    """Enumeration of SsMetaSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SsMetaSel instance for a given integer value."""
        _MAP = {
            0: SsMetaSel.Steel(),
            1: SsMetaSel.Zirc(),
        }
        return _MAP.get(v, SsMetaSel("unknown_{}".format(v), v))

    @staticmethod
    def Steel():
        """Returns the SsMetaSel value for 'Steel'."""
        return SsMetaSel('Steel', 0)

    @staticmethod
    def Zirc():
        """Returns the SsMetaSel value for 'Zirc'."""
        return SsMetaSel('Zirc', 1)


class StandardConSel(object):
    """Enumeration of StandardConSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the StandardConSel instance for a given integer value."""
        _MAP = {
            0: StandardConSel.basaltic_concrete(),
            1: StandardConSel.limestone_common_sand_concrete(),
            2: StandardConSel.Clinch_River_Breeder_Reactor_concrete(),
        }
        return _MAP.get(v, StandardConSel("unknown_{}".format(v), v))

    @staticmethod
    def basaltic_concrete():
        """Returns the StandardConSel value for 'basaltic concrete'."""
        return StandardConSel('basaltic_concrete', 0)

    @staticmethod
    def limestone_common_sand_concrete():
        """Returns the StandardConSel value for 'limestone/common sand concrete'."""
        return StandardConSel('limestone_common_sand_concrete', 1)

    @staticmethod
    def Clinch_River_Breeder_Reactor_concrete():
        """Returns the StandardConSel value for 'Clinch River Breeder Reactor concrete'."""
        return StandardConSel('Clinch_River_Breeder_Reactor_concrete', 2)


class SurgeLineControlSel(object):
    """Enumeration of SurgeLineControlSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SurgeLineControlSel instance for a given integer value."""
        _MAP = {
            -1: SurgeLineControlSel.Control_Function(),
            1: SurgeLineControlSel.Tabular_Function(),
            0: SurgeLineControlSel.Constant(),
        }
        return _MAP.get(v, SurgeLineControlSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function():
        """Returns the SurgeLineControlSel value for 'Control Function'."""
        return SurgeLineControlSel('Control_Function', -1)

    @staticmethod
    def Tabular_Function():
        """Returns the SurgeLineControlSel value for 'Tabular Function'."""
        return SurgeLineControlSel('Tabular_Function', 1)

    @staticmethod
    def Constant():
        """Returns the SurgeLineControlSel value for 'Constant'."""
        return SurgeLineControlSel('Constant', 0)


class SurgelineFormLossSel(object):
    """Enumeration of SurgelineFormLossSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the SurgelineFormLossSel instance for a given integer value."""
        _MAP = {
            -1: SurgelineFormLossSel.Control_Function(),
            0: SurgelineFormLossSel.Constant(),
        }
        return _MAP.get(v, SurgelineFormLossSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function():
        """Returns the SurgelineFormLossSel value for 'Control Function'."""
        return SurgelineFormLossSel('Control_Function', -1)

    @staticmethod
    def Constant():
        """Returns the SurgelineFormLossSel value for 'Constant'."""
        return SurgelineFormLossSel('Constant', 0)


class TFLenSel(object):
    """Enumeration of TFLenSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the TFLenSel instance for a given integer value."""
        _MAP = {
            0: TFLenSel.Tabular_Function(),
            1: TFLenSel.Explicit(),
        }
        return _MAP.get(v, TFLenSel("unknown_{}".format(v), v))

    @staticmethod
    def Tabular_Function():
        """Returns the TFLenSel value for 'Tabular Function'."""
        return TFLenSel('Tabular_Function', 0)

    @staticmethod
    def Explicit():
        """Returns the TFLenSel value for 'Explicit'."""
        return TFLenSel('Explicit', 1)


class TableControlArcSel(object):
    """Enumeration of TableControlArcSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the TableControlArcSel instance for a given integer value."""
        _MAP = {
            0: TableControlArcSel.Control_Function(),
            1: TableControlArcSel.Tabular_Function(),
        }
        return _MAP.get(v, TableControlArcSel("unknown_{}".format(v), v))

    @staticmethod
    def Control_Function():
        """Returns the TableControlArcSel value for 'Control Function'."""
        return TableControlArcSel('Control_Function', 0)

    @staticmethod
    def Tabular_Function():
        """Returns the TableControlArcSel value for 'Tabular Function'."""
        return TableControlArcSel('Tabular_Function', 1)


class TransIstatSel(object):
    """Enumeration of TransIstatSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the TransIstatSel instance for a given integer value."""
        _MAP = {
            0: TransIstatSel.All_States(),
            1: TransIstatSel.Aerosols_on_Heat(),
            2: TransIstatSel.Vapors_on_Heat(),
            3: TransIstatSel.Vapor_Aerosols(),
            4: TransIstatSel.Liquid_Aerosols(),
            5: TransIstatSel.Gaseous_Vapors(),
            6: TransIstatSel.Liquid_Vapors(),
        }
        return _MAP.get(v, TransIstatSel("unknown_{}".format(v), v))

    @staticmethod
    def All_States():
        """Returns the TransIstatSel value for 'All States'."""
        return TransIstatSel('All_States', 0)

    @staticmethod
    def Aerosols_on_Heat():
        """Returns the TransIstatSel value for 'Aerosols on Heat'."""
        return TransIstatSel('Aerosols_on_Heat', 1)

    @staticmethod
    def Vapors_on_Heat():
        """Returns the TransIstatSel value for 'Vapors on Heat'."""
        return TransIstatSel('Vapors_on_Heat', 2)

    @staticmethod
    def Vapor_Aerosols():
        """Returns the TransIstatSel value for 'Vapor Aerosols'."""
        return TransIstatSel('Vapor_Aerosols', 3)

    @staticmethod
    def Liquid_Aerosols():
        """Returns the TransIstatSel value for 'Liquid Aerosols'."""
        return TransIstatSel('Liquid_Aerosols', 4)

    @staticmethod
    def Gaseous_Vapors():
        """Returns the TransIstatSel value for 'Gaseous Vapors'."""
        return TransIstatSel('Gaseous_Vapors', 5)

    @staticmethod
    def Liquid_Vapors():
        """Returns the TransIstatSel value for 'Liquid Vapors'."""
        return TransIstatSel('Liquid_Vapors', 6)


class TransItsttwSel(object):
    """Enumeration of TransItsttwSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the TransItsttwSel instance for a given integer value."""
        _MAP = {
            0: TransItsttwSel.Continue_in_Water(),
            1: TransItsttwSel.Halt_in_Wet_Source(),
            2: TransItsttwSel.Halt_in_Wet_Target(),
            3: TransItsttwSel.Halt_if_Ether_Wet(),
            4: TransItsttwSel.Halt_if_Both_Wet(),
        }
        return _MAP.get(v, TransItsttwSel("unknown_{}".format(v), v))

    @staticmethod
    def Continue_in_Water():
        """Returns the TransItsttwSel value for 'Continue in Water'."""
        return TransItsttwSel('Continue_in_Water', 0)

    @staticmethod
    def Halt_in_Wet_Source():
        """Returns the TransItsttwSel value for 'Halt in Wet Source'."""
        return TransItsttwSel('Halt_in_Wet_Source', 1)

    @staticmethod
    def Halt_in_Wet_Target():
        """Returns the TransItsttwSel value for 'Halt in Wet Target'."""
        return TransItsttwSel('Halt_in_Wet_Target', 2)

    @staticmethod
    def Halt_if_Ether_Wet():
        """Returns the TransItsttwSel value for 'Halt if Ether Wet'."""
        return TransItsttwSel('Halt_if_Ether_Wet', 3)

    @staticmethod
    def Halt_if_Both_Wet():
        """Returns the TransItsttwSel value for 'Halt if Both Wet'."""
        return TransItsttwSel('Halt_if_Both_Wet', 4)


class TransferDryoutSel(object):
    """Enumeration of TransferDryoutSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the TransferDryoutSel instance for a given integer value."""
        _MAP = {
            0: TransferDryoutSel.Inactive_during_dryout(),
            1: TransferDryoutSel.Stop_calculation_on_dryout(),
        }
        return _MAP.get(v, TransferDryoutSel("unknown_{}".format(v), v))

    @staticmethod
    def Inactive_during_dryout():
        """Returns the TransferDryoutSel value for 'Inactive during dryout'."""
        return TransferDryoutSel('Inactive_during_dryout', 0)

    @staticmethod
    def Stop_calculation_on_dryout():
        """Returns the TransferDryoutSel value for 'Stop calculation on dryout'."""
        return TransferDryoutSel('Stop_calculation_on_dryout', 1)


class VKeySel(object):
    """Enumeration of VKeySel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the VKeySel instance for a given integer value."""
        _MAP = {
            0: VKeySel.Pool(),
            1: VKeySel.Atmosphere(),
            2: VKeySel.All(),
        }
        return _MAP.get(v, VKeySel("unknown_{}".format(v), v))

    @staticmethod
    def Pool():
        """Returns the VKeySel value for 'Pool'."""
        return VKeySel('Pool', 0)

    @staticmethod
    def Atmosphere():
        """Returns the VKeySel value for 'Atmosphere'."""
        return VKeySel('Atmosphere', 1)

    @staticmethod
    def All():
        """Returns the VKeySel value for 'All'."""
        return VKeySel('All', 2)


class VapStateSel(object):
    """Enumeration of VapStateSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the VapStateSel instance for a given integer value."""
        _MAP = {
            0: VapStateSel.Saturated(),
            1: VapStateSel.Superheated(),
        }
        return _MAP.get(v, VapStateSel("unknown_{}".format(v), v))

    @staticmethod
    def Saturated():
        """Returns the VapStateSel value for 'Saturated'."""
        return VapStateSel('Saturated', 0)

    @staticmethod
    def Superheated():
        """Returns the VapStateSel value for 'Superheated'."""
        return VapStateSel('Superheated', 1)


class WaterDiameterSel(object):
    """Enumeration of WaterDiameterSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the WaterDiameterSel instance for a given integer value."""
        _MAP = {
            0: WaterDiameterSel.Constant_Diameter(),
            1: WaterDiameterSel.Control_Function(),
        }
        return _MAP.get(v, WaterDiameterSel("unknown_{}".format(v), v))

    @staticmethod
    def Constant_Diameter():
        """Returns the WaterDiameterSel value for 'Constant Diameter'."""
        return WaterDiameterSel('Constant_Diameter', 0)

    @staticmethod
    def Control_Function():
        """Returns the WaterDiameterSel value for 'Control Function'."""
        return WaterDiameterSel('Control_Function', 1)


class YesNoSel(object):
    """Enumeration of YesNoSel values."""

    def __init__(self, name, value):
        object.__init__(self)
        self._name = name
        self._value = value

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self._name == other._name and self._value == other._value

    def __repr__(self):
        return "{}.{}".format(type(self).__name__, self._name)

    @property
    def value(self):
        return self._value

    @staticmethod
    def _for_value(v):
        """Return the YesNoSel instance for a given integer value."""
        _MAP = {
            0: YesNoSel.Yes(),
            1: YesNoSel.No(),
        }
        return _MAP.get(v, YesNoSel("unknown_{}".format(v), v))

    @staticmethod
    def Yes():
        """Returns the YesNoSel value for 'Yes'."""
        return YesNoSel('Yes', 0)

    @staticmethod
    def No():
        """Returns the YesNoSel value for 'No'."""
        return YesNoSel('No', 1)

