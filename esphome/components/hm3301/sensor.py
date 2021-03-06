import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import CONF_ID, CONF_PM_2_5, CONF_PM_10_0, CONF_PM_1_0, \
    UNIT_MICROGRAMS_PER_CUBIC_METER, ICON_CHEMICAL_WEAPON

DEPENDENCIES = ['i2c']

hm3301_ns = cg.esphome_ns.namespace('hm3301')
HM3301Component = hm3301_ns.class_('HM3301Component', cg.PollingComponent, i2c.I2CDevice)
AQICalculatorType = hm3301_ns.enum('AQICalculatorType')

CONF_AQI = 'aqi'
CONF_CALCULATION_TYPE = 'calculation_type'
UNIT_INDEX = 'index'

AQI_CALCULATION_TYPE = {
    'CAQI': AQICalculatorType.CAQI_TYPE,
    'AQI': AQICalculatorType.AQI_TYPE
}


def validate(config):
    if CONF_AQI in config and CONF_PM_2_5 not in config:
        raise cv.Invalid("AQI sensor requires PM 2.5")
    if CONF_AQI in config and CONF_PM_10_0 not in config:
        raise cv.Invalid("AQI sensor requires PM 10 sensors")
    return config


CONFIG_SCHEMA = cv.All(cv.Schema({
    cv.GenerateID(): cv.declare_id(HM3301Component),

    cv.Optional(CONF_PM_1_0):
        sensor.sensor_schema(UNIT_MICROGRAMS_PER_CUBIC_METER, ICON_CHEMICAL_WEAPON, 0),
    cv.Optional(CONF_PM_2_5):
        sensor.sensor_schema(UNIT_MICROGRAMS_PER_CUBIC_METER, ICON_CHEMICAL_WEAPON, 0),
    cv.Optional(CONF_PM_10_0):
        sensor.sensor_schema(UNIT_MICROGRAMS_PER_CUBIC_METER, ICON_CHEMICAL_WEAPON, 0),
    cv.Optional(CONF_AQI):
        sensor.sensor_schema(UNIT_INDEX, ICON_CHEMICAL_WEAPON, 0).extend({
            cv.Required(CONF_CALCULATION_TYPE): cv.enum(AQI_CALCULATION_TYPE, upper=True),
        })
}).extend(cv.polling_component_schema('60s')).extend(i2c.i2c_device_schema(0x40)), validate)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)

    if CONF_PM_1_0 in config:
        sens = yield sensor.new_sensor(config[CONF_PM_1_0])
        cg.add(var.set_pm_1_0_sensor(sens))

    if CONF_PM_2_5 in config:
        sens = yield sensor.new_sensor(config[CONF_PM_2_5])
        cg.add(var.set_pm_2_5_sensor(sens))

    if CONF_PM_10_0 in config:
        sens = yield sensor.new_sensor(config[CONF_PM_10_0])
        cg.add(var.set_pm_10_0_sensor(sens))

    if CONF_AQI in config:
        sens = yield sensor.new_sensor(config[CONF_AQI])
        cg.add(var.set_aqi_sensor(sens))
        cg.add(var.set_aqi_calculation_type(config[CONF_AQI][CONF_CALCULATION_TYPE]))

    # https://platformio.org/lib/show/6306/Grove%20-%20Laser%20PM2.5%20Sensor%20HM3301
    cg.add_library('6306', '1.0.3')
