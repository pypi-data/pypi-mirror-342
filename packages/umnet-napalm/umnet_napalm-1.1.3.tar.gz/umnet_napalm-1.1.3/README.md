# umnet-napalm
This is a project that augments the [NAPALM](https://napalm.readthedocs.io/en/latest/) library in ways that are relevant to our interests.
More specifically, new [getter functions](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix) have been implemented to pull
data from routers and parse it into a vender agnostic format.

The following platforms all have their own `umnet-napalm` drivers. Most of these inherit from other libraries.
* `ASA` does not inherit - the NAPALM community ASA driver uses the web API which is currently impractical for us.
* `IOS` inherits `napalm.ios.IOSDriver`
* `IOSXRNetconf` inherits `napalm.iosxr_netconf.IOSXRNETCONFDriver`
* `Junos` inherits `napalm.junos.JunOSDriver`
* `NXOS` inherits `napalm.nxos_ssh.NXOSSSHDriver`
* `PANOS` inherits `napalm_panos.panos.PANOSDriver`

See the `umnet_napalm` [Abstract Base Class](https://github.com/umich-its-networking/umnet-napalm/blob/main/umnet_napalm/abstract_base.py) definition to see what commands are supported across all platforms. For platforms that inherit from core NAPALM drivers, refer to the [getter matrix](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix). For PANOS see [napalm-panos repo](https://github.com/napalm-automation-community/napalm-panos)

## Using umnet-napalm
tbd
