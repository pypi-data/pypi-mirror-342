from dependency.core import provider, providers
from example.plugin.hardware.factory import HardwareFactory, HardwareFactoryComponent
from example.plugin.hardware.factory.interfaces import Hardware
from example.plugin.hardware.factory.products.productB import HardwareB
from example.plugin.hardware.factory.products.productC import HardwareC
from example.plugin.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugin.hardware.observer.interfaces import EventHardwareCreated

@provider(
    component=HardwareFactoryComponent,
    imports=[
        HardwareObserverComponent
    ],
    dependents=[
        HardwareB,
        HardwareC
    ],
    provider = providers.Singleton
)
class HardwareFactoryCreatorB(HardwareFactory):
    def __init__(self, config: dict):
        self.__observer: HardwareObserver = HardwareObserverComponent()
        print("FactoryCreatorB initialized")

    def createProduct(self, product: str) -> Hardware:
        match product:
            case "B":
                self.__observer.update(
                    context=EventHardwareCreated(product="B"))
                return HardwareB()
            case "C":
                self.__observer.update(
                    context=EventHardwareCreated(product="C"))
                return HardwareC()
            case _:
                raise ValueError(f"Unknown product type: {product}")