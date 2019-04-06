#
# Common INI file handling class
#
from __future__ import print_function
import sys

if sys.version[0] == '2':
    from ConfigParser import ConfigParser, NoSectionError
else:
    from configparser import ConfigParser, NoSectionError


class BaseIniFile(object):

    SECTION_TYPE_SIMPLE = 0
    SECTION_TPYE_STRUCT = 1
    KEY_SEC_NAME = 'section_names'
    KEY_SEC_META = 'section_metas'
    KEY_TYPE = 'type'
    KEY_ITEMS = 'items'
    KEY_SIZE = 'size'

    def __init__(self, config_file_name, config_data):
        # read ini file
        self.config_file_name = config_file_name
        self.section_names = config_data.get(BaseIniFile.KEY_SEC_NAME)
        self.section_metas = config_data.get(BaseIniFile.KEY_SEC_META)
        self.config = ConfigParser()
        self.config.optionxform = str
        self.config.read(config_file_name)
        # read in sections from file and compare with set ones
        # add missing ones, happens normally only on first call and file creation
        sections_in_file = self.config.sections()
        for section_id, section_name in self.section_names.items():
            if section_name not in sections_in_file:
                self.config.add_section(section_name)

    def save_config(self, config_file_name=None):
        # watch out, write expects file open as text file - not binary!!
        tmp_config_file_name = self.config_file_name
        if config_file_name is not None:
            tmp_config_file_name = config_file_name
        with open(tmp_config_file_name, 'w') as configfile:
            try:
                self.config.write(configfile)
            except:
                print('Unexpected error:', str(sys.exc_info()))

    def print_out_config(self):
        for section_name in self.config.sections():
            print('Section:', section_name)
            print('  Options:', self.config.options(section_name))
            for name, value in self.config.items(section_name):
                print('  %s = %s' % (name, value))
            print()

    def get_section_values(self, section_id):
        valueList = list()
        try:
            for name, value in self.config.items(self.section_names[section_id]):
                valueList.append(value)
        except NoSectionError:
            print('Section %s does not exists', self.section_names[section_id])
        except:
            print('Unexpected error:', sys.exc_info()[0])
        return valueList

    def get_full_section(self, section_id):
        try:
            if self.section_metas[section_id][BaseIniFile.KEY_TYPE] == BaseIniFile.SECTION_TPYE_STRUCT:
                section_list = dict()
                for option_name, option_value in self.config.items(self.section_names[section_id]):
                    if option_name in self.section_metas[section_id][BaseIniFile.KEY_ITEMS]:
                        section_list[option_name] = option_value
            else:
                section_list = list()
                for option_name, option_value in self.config.items(self.section_names[section_id]):
                    section_list.append(option_value)
                pass
        except NoSectionError:
            print('Section %s does not exists', self.section_names[section_id])
        except:
            print('Unexpected error:', sys.exc_info()[0])
        return section_list

    def update_section(self, section_id, new_section_data):
        option_counter = 0
        if self.section_metas[section_id][BaseIniFile.KEY_TYPE] == self.SECTION_TPYE_STRUCT:
            for option_name in new_section_data:
                    try:
                        self.config.set(self.section_names[section_id], option_name, new_section_data[option_name])
                    except NoSectionError:
                        print('Section %s does not exists', self.section_names[section_id])
                    except:
                        print('Unexpected error:', sys.exc_info()[0])
        else:
            section_size = self.section_metas[section_id][BaseIniFile.KEY_SIZE]
            for data_value in new_section_data:
                self.config.set(self.section_names[section_id], str(option_counter), data_value)
                option_counter += 1
                if option_counter >= section_size:
                    break
                pass


if __name__ == "__main__":

    class TestBaseIniFile(BaseIniFile):
        TCC_CONFIGURATION = 0
        TCC_LAYOUT = 1
        TCC_MCG_FW_DIR_HIST = 2
        TCC_MCG_FW_VERS_HIST = 3
        TCC_MCG_CFG_DIR_HIST = 4
        TCC_MCG_CFG_VERS_HIST = 5
        TCC_MCG_PACK_DIR_HIST = 6
        TCC_PRODBASE_VERS_HIST = 7
        TCC_INST_DST_HIST = 8
        TCC_PACK_BRNCH_HIST = 9
        TCC_PACK_TAG_HIST = 10
        TCC_INST_SRC_HIST = 11
        TCC_INST_DST_HIST = 12
        TCC_INST_DIR_HIST = 13
        CONFIG_DATA = {
            'section_names': {
                TCC_CONFIGURATION: 'Configuration',
                TCC_LAYOUT: 'Layout',
                TCC_MCG_FW_DIR_HIST: 'McgFwDirHistory',
                TCC_MCG_FW_VERS_HIST: 'McgFwVersionHistory',
                TCC_MCG_CFG_DIR_HIST: 'McgCfgDirHistory',
                TCC_MCG_CFG_VERS_HIST: 'McgCfgVersionHistory',
                TCC_MCG_PACK_DIR_HIST: 'McgPackDirHistory',
                TCC_PRODBASE_VERS_HIST: 'ProdBaseVersionHistory',
                TCC_PACK_BRNCH_HIST: 'CreateMcgPackBranchHistory',
                TCC_PACK_TAG_HIST: 'CreateMcgPackTagHistory',
                TCC_INST_SRC_HIST: 'CopyToInstallSrcHistory',
                TCC_INST_DST_HIST: 'CopyToInstallDstHistory',
                TCC_INST_DIR_HIST: 'InstallDirHistory'
            },
            'section_metas': {
                TCC_LAYOUT: {'type': BaseIniFile.SECTION_TPYE_STRUCT, 'size': 1},
                TCC_MCG_FW_DIR_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_MCG_FW_VERS_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_MCG_CFG_DIR_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_MCG_CFG_VERS_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_MCG_PACK_DIR_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_PRODBASE_VERS_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_PACK_BRNCH_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_PACK_TAG_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_INST_SRC_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_INST_DST_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10},
                TCC_INST_DIR_HIST: {'type': BaseIniFile.SECTION_TYPE_SIMPLE, 'size': 10}
            }
        }

        def __init__(self, ini_file_name):
            super().__init__(ini_file_name, TestBaseIniFile.CONFIG_DATA)

    testConfig = TestBaseIniFile('toolscollector.ini')
    testConfig.print_out_config()
    layout = dict()
    layout['PosX'] = str(124)
    layout['PosY'] = str(424)
    layout['Height'] = str(242)
    layout['Width'] = str(5333)
    layout['geometry'] = str(b'AdnQywACAAAAAAG6AAAAtwAABcQAAANYAAABugAAALcAAAXEAAADWAAAAAAAAAAAB4A=')
    layout['state'] = str(b'AAAA/wAAAAD9AAAAAAAABAsAAAJ7AAAABAAAAAQAAAAIAAAACPwAAAABAAAAAgAAAAEAAAAWAG0AYQBpAG4AVABvAG8AbABCAGEAcgEAAAAA/////wAAAAAAAAAA')
    testConfig.update_section(TestBaseIniFile.TCC_LAYOUT, layout)

    sectionID = TestBaseIniFile.TCC_MCG_FW_VERS_HIST

    sectionTouples = testConfig.get_full_section(sectionID)
    print('Listing values of section %s' % TestBaseIniFile.CONFIG_DATA['section_names'][sectionID])
    for option, value in sectionTouples:
        print("%s=%s" % (option, value))

    sectionValues = testConfig.get_section_values(sectionID)
    print('Listing values of section %s' % TestBaseIniFile.CONFIG_DATA['section_names'][sectionID])
    for value in sectionValues:
        print("value %s" % value)

    # create test elements
    sectionValues.insert(0, '3.22.0.x')
    sectionValues.insert(0, '5.22.0.x')
    sectionValues.insert(0, '4.22.0.x')
    sectionValues.insert(0, '2.22.0.x')
    sectionValues.insert(0, '2.21.0.x')
    sectionValues.insert(0, '2.20.0.x')

    testConfig.update_section(sectionID, sectionValues)

    testConfig.save_config()
