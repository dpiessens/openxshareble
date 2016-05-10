
import uuid

class Attrs:
    DeviceInfo = uuid.UUID("0000180A-0000-1000-8000-00805F9B34FB");
    # iOS uses FEBC?
    Advertisement = uuid.UUID("0000FEBC-0000-1000-8000-00805F9B34FB");
    CGMService = uuid.UUID("F8083532-849E-531C-C594-30F1F86A4EA5");
    ServiceB = uuid.UUID("F8084532-849E-531C-C594-30F1F86A4EA5");

    # DeviceInfoCharacteristicUUID, Read, DexcomUN
    ManufacturerNameString = uuid.UUID("00002A29-0000-1000-8000-00805F9B34FB");

    # CGMServiceCharacteristicUUID
    Communication = uuid.UUID("F8083533-849E-531C-C594-30F1F86A4EA5");
    Control = uuid.UUID("F8083534-849E-531C-C594-30F1F86A4EA5");
    Authentication = uuid.UUID("F8083535-849E-531C-C594-30F1F86A4EA5");
    ProbablyBackfill = uuid.UUID("F8083536-849E-531C-C594-30F1F86A4EA5");

    # ServiceBCharacteristicUUID
    CharacteristicE = uuid.UUID("F8084533-849E-531C-C594-30F1F86A4EA5");
    CharacteristicF = uuid.UUID("F8084534-849E-531C-C594-30F1F86A4EA5");

    # CharacteristicDescriptorUUID
    CharacteristicUpdateNotification = uuid.UUID("00002902-0000-1000-8000-00805F9B34FB")

