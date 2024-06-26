commands_list = [
    {"PID": "00", "Name": "PIDS_A", "Description": "Supported PIDs [01-20]", "Response Value": "BitArray"},
    {"PID": "01", "Name": "STATUS", "Description": "Status since DTCs cleared", "Response Value": "special"},
    {"PID": "02", "Name": "FREEZE_DTC", "Description": "DTC that triggered the freeze frame", "Response Value": "special"},
    {"PID": "03", "Name": "FUEL_STATUS", "Description": "Fuel System Status", "Response Value": "(string, string)"},
    {"PID": "04", "Name": "ENGINE_LOAD", "Description": "Calculated Engine Load", "Response Value": "Unit.percent"},
    {"PID": "05", "Name": "COOLANT_TEMP", "Description": "Engine Coolant Temperature", "Response Value": "Unit.celsius"},
    {"PID": "06", "Name": "SHORT_FUEL_TRIM_1", "Description": "Short Term Fuel Trim - Bank 1", "Response Value": "Unit.percent"},
    {"PID": "07", "Name": "LONG_FUEL_TRIM_1", "Description": "Long Term Fuel Trim - Bank 1", "Response Value": "Unit.percent"},
    {"PID": "08", "Name": "SHORT_FUEL_TRIM_2", "Description": "Short Term Fuel Trim - Bank 2", "Response Value": "Unit.percent"},
    {"PID": "09", "Name": "LONG_FUEL_TRIM_2", "Description": "Long Term Fuel Trim - Bank 2", "Response Value": "Unit.percent"},
    {"PID": "0A", "Name": "FUEL_PRESSURE", "Description": "Fuel Pressure", "Response Value": "Unit.kilopascal"},
    {"PID": "0B", "Name": "INTAKE_PRESSURE", "Description": "Intake Manifold Pressure", "Response Value": "Unit.kilopascal"},
    {"PID": "0C", "Name": "RPM", "Description": "Engine RPM", "Response Value": "Unit.rpm"},
    {"PID": "0D", "Name": "SPEED", "Description": "Vehicle Speed", "Response Value": "Unit.kph"},
    {"PID": "0E", "Name": "TIMING_ADVANCE", "Description": "Timing Advance", "Response Value": "Unit.degree"},
    {"PID": "0F", "Name": "INTAKE_TEMP", "Description": "Intake Air Temp", "Response Value": "Unit.celsius"},
    {"PID": "10", "Name": "MAF", "Description": "Air Flow Rate (MAF)", "Response Value": "Unit.grams_per_second"},
    {"PID": "11", "Name": "THROTTLE_POS", "Description": "Throttle Position", "Response Value": "Unit.percent"},
    {"PID": "12", "Name": "AIR_STATUS", "Description": "Secondary Air Status", "Response Value": "string"},
    {"PID": "13", "Name": "O2_SENSORS", "Description": "O2 Sensors Present", "Response Value": "special"},
    {"PID": "14", "Name": "O2_B1S1", "Description": "O2: Bank 1 - Sensor 1 Voltage", "Response Value": "Unit.volt"},
    {"PID": "15", "Name": "O2_B1S2", "Description": "O2: Bank 1 - Sensor 2 Voltage", "Response Value": "Unit.volt"},
    {"PID": "16", "Name": "O2_B1S3", "Description": "O2: Bank 1 - Sensor 3 Voltage", "Response Value": "Unit.volt"},
    {"PID": "17", "Name": "O2_B1S4", "Description": "O2: Bank 1 - Sensor 4 Voltage", "Response Value": "Unit.volt"},
    {"PID": "18", "Name": "O2_B2S1", "Description": "O2: Bank 2 - Sensor 1 Voltage", "Response Value": "Unit.volt"},
    {"PID": "19", "Name": "O2_B2S2", "Description": "O2: Bank 2 - Sensor 2 Voltage", "Response Value": "Unit.volt"},
    {"PID": "1A", "Name": "O2_B2S3", "Description": "O2: Bank 2 - Sensor 3 Voltage", "Response Value": "Unit.volt"},
    {"PID": "1B", "Name": "O2_B2S4", "Description": "O2: Bank 2 - Sensor 4 Voltage", "Response Value": "Unit.volt"},
    {"PID": "1C", "Name": "OBD_COMPLIANCE", "Description": "OBD Standards Compliance", "Response Value": "string"},
    {"PID": "1D", "Name": "O2_SENSORS_ALT", "Description": "O2 Sensors Present (alternate)", "Response Value": "special"},
    {"PID": "1E", "Name": "AUX_INPUT_STATUS", "Description": "Auxiliary input status (power take off)", "Response Value": "boolean"},
    {"PID": "1F", "Name": "RUN_TIME", "Description": "Engine Run Time", "Response Value": "Unit.second"},
    {"PID": "20", "Name": "PIDS_B", "Description": "Supported PIDs [21-40]", "Response Value": "BitArray"},{"PID": "20", "Name": "PIDS_B", "Description": "Supported PIDs [21-40]", "Response Value": "BitArray"},
    {"PID": "21", "Name": "DISTANCE_W_MIL", "Description": "Distance Traveled with MIL on", "Response Value": "Unit.kilometer"},
    {"PID": "22", "Name": "FUEL_RAIL_PRESSURE_VAC", "Description": "Fuel Rail Pressure (relative to vacuum)", "Response Value": "Unit.kilopascal"},
    {"PID": "23", "Name": "FUEL_RAIL_PRESSURE_DIRECT", "Description": "Fuel Rail Pressure (direct inject)", "Response Value": "Unit.kilopascal"},
    {"PID": "24", "Name": "O2_S1_WR_VOLTAGE", "Description": "O2 Sensor 1 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "25", "Name": "O2_S2_WR_VOLTAGE", "Description": "O2 Sensor 2 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "26", "Name": "O2_S3_WR_VOLTAGE", "Description": "O2 Sensor 3 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "27", "Name": "O2_S4_WR_VOLTAGE", "Description": "O2 Sensor 4 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "28", "Name": "O2_S5_WR_VOLTAGE", "Description": "O2 Sensor 5 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "29", "Name": "O2_S6_WR_VOLTAGE", "Description": "O2 Sensor 6 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "2A", "Name": "O2_S7_WR_VOLTAGE", "Description": "O2 Sensor 7 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "2B", "Name": "O2_S8_WR_VOLTAGE", "Description": "O2 Sensor 8 WR Lambda Voltage", "Response Value": "Unit.volt"},
    {"PID": "2C", "Name": "COMMANDED_EGR", "Description": "Commanded EGR", "Response Value": "Unit.percent"},
    {"PID": "2D", "Name": "EGR_ERROR", "Description": "EGR Error", "Response Value": "Unit.percent"},
    {"PID": "2E", "Name": "EVAPORATIVE_PURGE", "Description": "Commanded Evaporative Purge", "Response Value": "Unit.percent"},
    {"PID": "2F", "Name": "FUEL_LEVEL", "Description": "Fuel Level Input", "Response Value": "Unit.percent"},
    {"PID": "30", "Name": "WARMUPS_SINCE_DTC_CLEAR", "Description": "Number of warm-ups since codes cleared", "Response Value": "Unit.count"},
    {"PID": "31", "Name": "DISTANCE_SINCE_DTC_CLEAR", "Description": "Distance traveled since codes cleared", "Response Value": "Unit.kilometer"},
    {"PID": "32", "Name": "EVAP_VAPOR_PRESSURE", "Description": "Evaporative system vapor pressure", "Response Value": "Unit.pascal"},
    {"PID": "33", "Name": "BAROMETRIC_PRESSURE", "Description": "Barometric Pressure", "Response Value": "Unit.kilopascal"},
    {"PID": "34", "Name": "O2_S1_WR_CURRENT", "Description": "O2 Sensor 1 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "35", "Name": "O2_S2_WR_CURRENT", "Description": "O2 Sensor 2 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "36", "Name": "O2_S3_WR_CURRENT", "Description": "O2 Sensor 3 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "37", "Name": "O2_S4_WR_CURRENT", "Description": "O2 Sensor 4 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "38", "Name": "O2_S5_WR_CURRENT", "Description": "O2 Sensor 5 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "39", "Name": "O2_S6_WR_CURRENT", "Description": "O2 Sensor 6 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "3A", "Name": "O2_S7_WR_CURRENT", "Description": "O2 Sensor 7 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "3B", "Name": "O2_S8_WR_CURRENT", "Description": "O2 Sensor 8 WR Lambda Current", "Response Value": "Unit.milliampere"},
    {"PID": "3C", "Name": "CATALYST_TEMP_B1S1", "Description": "Catalyst Temperature: Bank 1 - Sensor 1", "Response Value": "Unit.celsius"},
    {"PID": "3D", "Name": "CATALYST_TEMP_B2S1", "Description": "Catalyst Temperature: Bank 2 - Sensor 1", "Response Value": "Unit.celsius"},
    {"PID": "3E", "Name": "CATALYST_TEMP_B1S2", "Description": "Catalyst Temperature: Bank 1 - Sensor 2", "Response Value": "Unit.celsius"},
    {"PID": "3F", "Name": "CATALYST_TEMP_B2S2", "Description": "Catalyst Temperature: Bank 2 - Sensor 2", "Response Value": "Unit.celsius"},
    {"PID": "40", "Name": "PIDS_C", "Description": "Supported PIDs [41-60]", "Response Value": "BitArray"},
    {"PID": "41", "Name": "STATUS_DRIVE_CYCLE", "Description": "Monitor status this drive cycle", "Response Value": "special"},
    {"PID": "42", "Name": "CONTROL_MODULE_VOLTAGE", "Description": "Control module voltage", "Response Value": "Unit.volt"},
    {"PID": "43", "Name": "ABSOLUTE_LOAD", "Description": "Absolute load value", "Response Value": "Unit.percent"},
    {"PID": "44", "Name": "COMMANDED_EQUIV_RATIO", "Description": "Commanded equivalence ratio", "Response Value": "Unit.ratio"},
    {"PID": "45", "Name": "RELATIVE_THROTTLE_POS", "Description": "Relative throttle position", "Response Value": "Unit.percent"},
    {"PID": "46", "Name": "AMBIANT_AIR_TEMP", "Description": "Ambient air temperature", "Response Value": "Unit.celsius"},
    {"PID": "47", "Name": "THROTTLE_POS_B", "Description": "Absolute throttle position B", "Response Value": "Unit.percent"},
    {"PID": "48", "Name": "THROTTLE_POS_C", "Description": "Absolute throttle position C", "Response Value": "Unit.percent"},
    {"PID": "49", "Name": "ACCELERATOR_POS_D", "Description": "Accelerator pedal position D", "Response Value": "Unit.percent"},
    {"PID": "4A", "Name": "ACCELERATOR_POS_E", "Description": "Accelerator pedal position E", "Response Value": "Unit.percent"},
    {"PID": "4B", "Name": "ACCELERATOR_POS_F", "Description": "Accelerator pedal position F", "Response Value": "Unit.percent"},
    {"PID": "4C", "Name": "THROTTLE_ACTUATOR", "Description": "Commanded throttle actuator", "Response Value": "Unit.percent"},
    {"PID": "4D", "Name": "RUN_TIME_MIL", "Description": "Time run with MIL on", "Response Value": "Unit.minute"},
    {"PID": "4E", "Name": "TIME_SINCE_DTC_CLEARED", "Description": "Time since trouble codes cleared", "Response Value": "Unit.minute"},
    {"PID": "4F", "Name": "unsupported", "Description": "unsupported", "Response Value": "unsupported"},
    {"PID": "50", "Name": "MAX_MAF", "Description": "Maximum value for mass air flow sensor", "Response Value": "Unit.grams_per_second"},
    {"PID": "51", "Name": "FUEL_TYPE", "Description": "Fuel Type", "Response Value": "string"},
    {"PID": "52", "Name": "ETHANOL_PERCENT", "Description": "Ethanol Fuel Percent", "Response Value": "Unit.percent"},
    {"PID": "53", "Name": "EVAP_VAPOR_PRESSURE_ABS", "Description": "Absolute Evap system Vapor Pressure", "Response Value": "Unit.kilopascal"},
    {"PID": "54", "Name": "EVAP_VAPOR_PRESSURE_ALT", "Description": "Evap system vapor pressure", "Response Value": "Unit.pascal"},
    {"PID": "55", "Name": "SHORT_O2_TRIM_B1", "Description": "Short term secondary O2 trim - Bank 1", "Response Value": "Unit.percent"},
    {"PID": "56", "Name": "LONG_O2_TRIM_B1", "Description": "Long term secondary O2 trim - Bank 1", "Response Value": "Unit.percent"},
    {"PID": "57", "Name": "SHORT_O2_TRIM_B2", "Description": "Short term secondary O2 trim - Bank 2", "Response Value": "Unit.percent"},
    {"PID": "58", "Name": "LONG_O2_TRIM_B2", "Description": "Long term secondary O2 trim - Bank 2", "Response Value": "Unit.percent"},
    {"PID": "59", "Name": "FUEL_RAIL_PRESSURE_ABS", "Description": "Fuel rail pressure (absolute)", "Response Value": "Unit.kilopascal"},
    {"PID": "5A", "Name": "RELATIVE_ACCEL_POS", "Description": "Relative accelerator pedal position", "Response Value": "Unit.percent"},
    {"PID": "5B", "Name": "HYBRID_BATTERY_REMAINING", "Description": "Hybrid battery pack remaining life", "Response Value": "Unit.percent"},
    {"PID": "5C", "Name": "OIL_TEMP", "Description": "Engine oil temperature", "Response Value": "Unit.celsius"},
    {"PID": "5D", "Name": "FUEL_INJECT_TIMING", "Description": "Fuel injection timing", "Response Value": "Unit.degree"},
    {"PID": "5E", "Name": "FUEL_RATE", "Description": "Engine fuel rate", "Response Value": "Unit.liters_per_hour"}
]