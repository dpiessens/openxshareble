
import uuid

class Attrs:
    DeviceInfo = uuid.UUID('0000180a-0000-1000-8000-00805f9b34fb')
    # iOS uses FEBC?           
    Advertisement = uuid.UUID('0000febc-0000-1000-8000-00805f9b34fb')
    CGMService = uuid.UUID('f8083532-849e-531c-c594-30f1f86a4ea5')
    
    # DeviceInfoCharacteristicUUID, Read, DexcomUN
    ManufacturerNameString = uuid.UUID('00002a29-0000-1000-8000-00805f9b34fb')

    # CGMServiceCharacteristicUUID
    Communication = uuid.UUID('f8083533-849e-531c-c594-30f1f86a4ea5')
    Control = uuid.UUID('f8083534-849e-531c-c594-30f1f86a4ea5')
    Authentication = uuid.UUID('f8083535-849e-531c-c594-30f1f86a4ea5')
    ProbablyBackfill = uuid.UUID('f8083536-849e-531c-c594-30f1f86a4ea5')

    # CharacteristicDescriptorUUID
    CharacteristicUpdateNotification = uuid.UUID('00002902-0000-1000-8000-00805f9b34fb')

