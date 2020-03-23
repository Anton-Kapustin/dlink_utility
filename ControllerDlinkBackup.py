import re


class ControllerDlinkBackup:

    def __init__(self, controller_main):
        self.controller_main = controller_main

    # ------------------------------------------------------------------------------------------------------------------
    #                                               DLINK BACKUP
    # ------------------------------------------------------------------------------------------------------------------
    def make_dlink_backup(self, ip_address, args):
        response = ''
        ip_dst_for_backup = args['ip_dst_for_backup']
        path_work_directory = args['path_work_directory']
        list_read_expect = [b'Success', b'success', b'successful', b'fail', b'Fail']
        is_authorised_with_dlink = self.controller_main.authorisation(ip_address)
        if is_authorised_with_dlink:
            model = self.controller_main.get_dlink_model()
            cmd = self.make_cmd_for_backup_for_different_dlink_switches(model, ip_address, ip_dst_for_backup)
            if cmd:
                path_for_backup = self.controller_main.delete_last_object_in_path(path_work_directory) + 'backup/dlink'
                self.controller_main.check_folder_exists(path_for_backup)
                path_for_backup += '/' + ip_address
                self.controller_main.check_folder_exists(path_for_backup)
                # print(path_for_backup)
                if self.controller_main.network_send_data(cmd):
                    response = self.controller_main.network_receive_data_until(list_read_expect)
                    # print(response)
                backup_result = self.controller_main.check_string_contain_item_from_list(response, list_read_expect)
                if path_work_directory and backup_result:
                    if self.controller_main.is_web_smart_model(model):
                        string_to_write = ip_address + ' ' + model + ' WEB SMART backup ' + backup_result
                    else:
                        string_to_write = ip_address + ' ' + model + ' backup ' + backup_result
                    print(string_to_write)
                    self.controller_main.write_to_log_file(path_work_directory, string_to_write, 'a+')
                self.controller_main.network_close_connection()

        # sys.exit(0)
        # return result

    def make_cmd_for_backup_for_different_dlink_switches(self, dlink_model, ip_address, ip_dst_for_backup):
        dlink_model = re.sub('[/]', '', dlink_model)
        backup_name = ip_address + '\\' + ip_address + '_' + dlink_model + '_' + \
                      self.controller_main.get_date_in_string()
        cmd = ''
        if dlink_model:
            if '3200' in dlink_model or '3000' in dlink_model or '1510' in dlink_model or '3120' in dlink_model:
                cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + 'dest_file ' + backup_name + '.cfg\n'
            elif '1210' in dlink_model and 'ME' in dlink_model:
                cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + backup_name + '.cfg\n'
            elif '1210' in dlink_model and 'ME' not in dlink_model:
                # print("WEB SMART")
                cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + backup_name + '\n'
        return cmd
    # ------------------------------------------------------------------------------------------------------------------
