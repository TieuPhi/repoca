import device_management
Router_4100 = device_management.Device("SBD-12345678","3.3.3.3", "tieuphi", "0903", "5.5.5.5")
print(Router_4100.generate_preconfigure())
Router_4100.export_config()
