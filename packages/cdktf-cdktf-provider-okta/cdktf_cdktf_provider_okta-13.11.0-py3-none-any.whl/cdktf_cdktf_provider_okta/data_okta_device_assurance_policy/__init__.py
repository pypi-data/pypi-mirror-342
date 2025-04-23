r'''
# `data_okta_device_assurance_policy`

Refer to the Terraform Registry for docs: [`data_okta_device_assurance_policy`](https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataOktaDeviceAssurancePolicy(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy okta_device_assurance_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        third_party_signal_provider: typing.Optional[typing.Union["DataOktaDeviceAssurancePolicyThirdPartySignalProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy okta_device_assurance_policy} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: ID of the user type to retrieve, conflicts with ``name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#id DataOktaDeviceAssurancePolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Name of user type to retrieve, conflicts with ``id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#name DataOktaDeviceAssurancePolicy#name}
        :param secure_hardware_present: Indicates if the device contains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#secure_hardware_present DataOktaDeviceAssurancePolicy#secure_hardware_present}
        :param third_party_signal_provider: Indicates if the device contains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#third_party_signal_provider DataOktaDeviceAssurancePolicy#third_party_signal_provider}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3abb5b7a942ac7114f3a37018de45309c6edd37c571ce00e3ac05c7b15b026)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOktaDeviceAssurancePolicyConfig(
            id=id,
            name=name,
            secure_hardware_present=secure_hardware_present,
            third_party_signal_provider=third_party_signal_provider,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataOktaDeviceAssurancePolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOktaDeviceAssurancePolicy to import.
        :param import_from_id: The id of the existing DataOktaDeviceAssurancePolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOktaDeviceAssurancePolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fae8c13833973db89fd4ac631b484c6112e34131dde2aab8e47eaa968f2c6e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putThirdPartySignalProvider")
    def put_third_party_signal_provider(
        self,
        *,
        dtc: typing.Optional[typing.Union["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#dtc DataOktaDeviceAssurancePolicy#dtc}.
        '''
        value = DataOktaDeviceAssurancePolicyThirdPartySignalProvider(dtc=dtc)

        return typing.cast(None, jsii.invoke(self, "putThirdPartySignalProvider", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSecureHardwarePresent")
    def reset_secure_hardware_present(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureHardwarePresent", []))

    @jsii.member(jsii_name="resetThirdPartySignalProvider")
    def reset_third_party_signal_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThirdPartySignalProvider", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionType")
    def disk_encryption_type(
        self,
    ) -> "DataOktaDeviceAssurancePolicyDiskEncryptionTypeOutputReference":
        return typing.cast("DataOktaDeviceAssurancePolicyDiskEncryptionTypeOutputReference", jsii.get(self, "diskEncryptionType"))

    @builtins.property
    @jsii.member(jsii_name="jailbreak")
    def jailbreak(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "jailbreak"))

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> "DataOktaDeviceAssurancePolicyOsVersionOutputReference":
        return typing.cast("DataOktaDeviceAssurancePolicyOsVersionOutputReference", jsii.get(self, "osVersion"))

    @builtins.property
    @jsii.member(jsii_name="osVersionConstraint")
    def os_version_constraint(
        self,
    ) -> "DataOktaDeviceAssurancePolicyOsVersionConstraintList":
        return typing.cast("DataOktaDeviceAssurancePolicyOsVersionConstraintList", jsii.get(self, "osVersionConstraint"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="screenlockType")
    def screenlock_type(
        self,
    ) -> "DataOktaDeviceAssurancePolicyScreenlockTypeOutputReference":
        return typing.cast("DataOktaDeviceAssurancePolicyScreenlockTypeOutputReference", jsii.get(self, "screenlockType"))

    @builtins.property
    @jsii.member(jsii_name="thirdPartySignalProvider")
    def third_party_signal_provider(
        self,
    ) -> "DataOktaDeviceAssurancePolicyThirdPartySignalProviderOutputReference":
        return typing.cast("DataOktaDeviceAssurancePolicyThirdPartySignalProviderOutputReference", jsii.get(self, "thirdPartySignalProvider"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secureHardwarePresentInput")
    def secure_hardware_present_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureHardwarePresentInput"))

    @builtins.property
    @jsii.member(jsii_name="thirdPartySignalProviderInput")
    def third_party_signal_provider_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataOktaDeviceAssurancePolicyThirdPartySignalProvider"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataOktaDeviceAssurancePolicyThirdPartySignalProvider"]], jsii.get(self, "thirdPartySignalProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a9298c7c78d16dce947aadd506dd4d6a8d1a04c19e7a726dbe47bebb8dd481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88b0a5ab20b94083c3c31d3d99270d1bcf645ea2651ffbd39efe92f3ec11c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureHardwarePresent")
    def secure_hardware_present(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secureHardwarePresent"))

    @secure_hardware_present.setter
    def secure_hardware_present(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b898c2036f73790df6168d98cce3aa3367e0dab0f8d99eaab316cd7041acee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureHardwarePresent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "name": "name",
        "secure_hardware_present": "secureHardwarePresent",
        "third_party_signal_provider": "thirdPartySignalProvider",
    },
)
class DataOktaDeviceAssurancePolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        third_party_signal_provider: typing.Optional[typing.Union["DataOktaDeviceAssurancePolicyThirdPartySignalProvider", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: ID of the user type to retrieve, conflicts with ``name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#id DataOktaDeviceAssurancePolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Name of user type to retrieve, conflicts with ``id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#name DataOktaDeviceAssurancePolicy#name}
        :param secure_hardware_present: Indicates if the device contains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#secure_hardware_present DataOktaDeviceAssurancePolicy#secure_hardware_present}
        :param third_party_signal_provider: Indicates if the device contains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#third_party_signal_provider DataOktaDeviceAssurancePolicy#third_party_signal_provider}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(third_party_signal_provider, dict):
            third_party_signal_provider = DataOktaDeviceAssurancePolicyThirdPartySignalProvider(**third_party_signal_provider)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d391b99ae8cf8b05207466fc1ba0269b9e1acf9e1feee088ba372c0a8cb5c09a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument secure_hardware_present", value=secure_hardware_present, expected_type=type_hints["secure_hardware_present"])
            check_type(argname="argument third_party_signal_provider", value=third_party_signal_provider, expected_type=type_hints["third_party_signal_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if secure_hardware_present is not None:
            self._values["secure_hardware_present"] = secure_hardware_present
        if third_party_signal_provider is not None:
            self._values["third_party_signal_provider"] = third_party_signal_provider

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''ID of the user type to retrieve, conflicts with ``name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#id DataOktaDeviceAssurancePolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of user type to retrieve, conflicts with ``id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#name DataOktaDeviceAssurancePolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secure_hardware_present(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if the device contains a secure hardware functionality.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#secure_hardware_present DataOktaDeviceAssurancePolicy#secure_hardware_present}
        '''
        result = self._values.get("secure_hardware_present")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def third_party_signal_provider(
        self,
    ) -> typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProvider"]:
        '''Indicates if the device contains a secure hardware functionality.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#third_party_signal_provider DataOktaDeviceAssurancePolicy#third_party_signal_provider}
        '''
        result = self._values.get("third_party_signal_provider")
        return typing.cast(typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProvider"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyDiskEncryptionType",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaDeviceAssurancePolicyDiskEncryptionType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyDiskEncryptionType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaDeviceAssurancePolicyDiskEncryptionTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyDiskEncryptionTypeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57795250cdf956a14a41b416d2594510268617ce62e18f8189f8b67f77143ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "include"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOktaDeviceAssurancePolicyDiskEncryptionType]:
        return typing.cast(typing.Optional[DataOktaDeviceAssurancePolicyDiskEncryptionType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOktaDeviceAssurancePolicyDiskEncryptionType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973bc0751868d03cfa213ec8998cedf11941f3ddadbd6f08f5f8b9e232e45ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersion",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaDeviceAssurancePolicyOsVersion:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyOsVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionConstraint",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaDeviceAssurancePolicyOsVersionConstraint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyOsVersionConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f59485af704b8ecea7b62aab476ea5816f5a72ae2103a5e1ad9820f2a80cdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="distanceFromLatestMajor")
    def distance_from_latest_major(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "distanceFromLatestMajor"))

    @builtins.property
    @jsii.member(jsii_name="latestSecurityPatch")
    def latest_security_patch(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "latestSecurityPatch"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement]:
        return typing.cast(typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abafa2c8d6227d3975d265574b2ed76a87445a4f815f88cbfa5b0ab638d1a7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOktaDeviceAssurancePolicyOsVersionConstraintList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionConstraintList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710c707032de612da97fcd699e23aa2c8b694131fad871a553bc5defa5c85c93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOktaDeviceAssurancePolicyOsVersionConstraintOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f424a439486359df3d5cb1bdd42971e5aa0c866af02a525fd3a8ec6388d0fd01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOktaDeviceAssurancePolicyOsVersionConstraintOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe6c0907c53346ec9874ef44b42dcded8c7b4f1e5fcb9f6aa8b4acd6b62453e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d18cdc08df0a4b063fcaf148631af7ea30c43fe2b8fd0d1119dcedd78bc057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ca8fc02a6fb4a262b59658d8c1415165cbd79b4d79e76aabb2e8480aa356bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOktaDeviceAssurancePolicyOsVersionConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionConstraintOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a841490dc094aa87096e2f1029a4c868131870566b0f87e580e7cb4fbe39f8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dynamicVersionRequirement")
    def dynamic_version_requirement(
        self,
    ) -> DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirementOutputReference:
        return typing.cast(DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirementOutputReference, jsii.get(self, "dynamicVersionRequirement"))

    @builtins.property
    @jsii.member(jsii_name="majorVersionConstraint")
    def major_version_constraint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "majorVersionConstraint"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraint]:
        return typing.cast(typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94aec4bcf6f5ae9fd901aab399eb006dfa957bf63128f7e03390f24943ab27a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504294a014fc028054888be3baf91fafb8a0deca95c4b9a9f0d1a9fad060b4f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="distanceFromLatestMajor")
    def distance_from_latest_major(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "distanceFromLatestMajor"))

    @builtins.property
    @jsii.member(jsii_name="latestSecurityPatch")
    def latest_security_patch(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "latestSecurityPatch"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement]:
        return typing.cast(typing.Optional[DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d8cff87880b09fcc1ddc2747246eb29568b4c3485cd45194cfe1d4820839ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOktaDeviceAssurancePolicyOsVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyOsVersionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0510efc7b2470e3715dbee30e1e97d59c356e9a40625600d63807e1f825bb5b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dynamicVersionRequirement")
    def dynamic_version_requirement(
        self,
    ) -> DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirementOutputReference:
        return typing.cast(DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirementOutputReference, jsii.get(self, "dynamicVersionRequirement"))

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimum"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataOktaDeviceAssurancePolicyOsVersion]:
        return typing.cast(typing.Optional[DataOktaDeviceAssurancePolicyOsVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0ebbf4417565909dd7162e1cdab42739930dbe18daf98df3f7900b922bf183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyScreenlockType",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaDeviceAssurancePolicyScreenlockType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyScreenlockType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaDeviceAssurancePolicyScreenlockTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyScreenlockTypeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9c3105122ed8d03fcb1d498bb0053195d0771f8ada51d3814a3c5ee7e7243d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "include"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOktaDeviceAssurancePolicyScreenlockType]:
        return typing.cast(typing.Optional[DataOktaDeviceAssurancePolicyScreenlockType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOktaDeviceAssurancePolicyScreenlockType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce69388a0624be061e6ec444cc7c60294448920399822472501357d8a849a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProvider",
    jsii_struct_bases=[],
    name_mapping={"dtc": "dtc"},
)
class DataOktaDeviceAssurancePolicyThirdPartySignalProvider:
    def __init__(
        self,
        *,
        dtc: typing.Optional[typing.Union["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dtc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#dtc DataOktaDeviceAssurancePolicy#dtc}.
        '''
        if isinstance(dtc, dict):
            dtc = DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc(**dtc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436e865f5ff1ac82b9ec22323565fdd5d338fae6f6b4cc4632784920ca1f80e2)
            check_type(argname="argument dtc", value=dtc, expected_type=type_hints["dtc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dtc is not None:
            self._values["dtc"] = dtc

    @builtins.property
    def dtc(
        self,
    ) -> typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#dtc DataOktaDeviceAssurancePolicy#dtc}.'''
        result = self._values.get("dtc")
        return typing.cast(typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyThirdPartySignalProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc",
    jsii_struct_bases=[],
    name_mapping={
        "allow_screen_lock": "allowScreenLock",
        "browser_version": "browserVersion",
        "built_in_dns_client_enabled": "builtInDnsClientEnabled",
        "chrome_remote_desktop_app_blocked": "chromeRemoteDesktopAppBlocked",
        "crowd_strike_agent_id": "crowdStrikeAgentId",
        "crowd_strike_customer_id": "crowdStrikeCustomerId",
        "device_enrollment_domain": "deviceEnrollmentDomain",
        "disk_encrypted": "diskEncrypted",
        "key_trust_level": "keyTrustLevel",
        "managed_device": "managedDevice",
        "os_firewall": "osFirewall",
        "os_version": "osVersion",
        "password_protection_warning_trigger": "passwordProtectionWarningTrigger",
        "realtime_url_check_mode": "realtimeUrlCheckMode",
        "safe_browsing_protection_level": "safeBrowsingProtectionLevel",
        "screen_lock_secured": "screenLockSecured",
        "site_isolation_enabled": "siteIsolationEnabled",
        "third_party_blocking_enabled": "thirdPartyBlockingEnabled",
        "windows_machine_domain": "windowsMachineDomain",
        "windows_user_domain": "windowsUserDomain",
    },
)
class DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc:
    def __init__(
        self,
        *,
        allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        browser_version: typing.Optional[typing.Union["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        built_in_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crowd_strike_agent_id: typing.Optional[builtins.str] = None,
        crowd_strike_customer_id: typing.Optional[builtins.str] = None,
        device_enrollment_domain: typing.Optional[builtins.str] = None,
        disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_trust_level: typing.Optional[builtins.str] = None,
        managed_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_version: typing.Optional[typing.Union["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        password_protection_warning_trigger: typing.Optional[builtins.str] = None,
        realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        safe_browsing_protection_level: typing.Optional[builtins.str] = None,
        screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        windows_machine_domain: typing.Optional[builtins.str] = None,
        windows_user_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_screen_lock: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#allow_screen_lock DataOktaDeviceAssurancePolicy#allow_screen_lock}.
        :param browser_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#browser_version DataOktaDeviceAssurancePolicy#browser_version}.
        :param built_in_dns_client_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#built_in_dns_client_enabled DataOktaDeviceAssurancePolicy#built_in_dns_client_enabled}.
        :param chrome_remote_desktop_app_blocked: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#chrome_remote_desktop_app_blocked DataOktaDeviceAssurancePolicy#chrome_remote_desktop_app_blocked}.
        :param crowd_strike_agent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#crowd_strike_agent_id DataOktaDeviceAssurancePolicy#crowd_strike_agent_id}.
        :param crowd_strike_customer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#crowd_strike_customer_id DataOktaDeviceAssurancePolicy#crowd_strike_customer_id}.
        :param device_enrollment_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#device_enrollment_domain DataOktaDeviceAssurancePolicy#device_enrollment_domain}.
        :param disk_encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#disk_encrypted DataOktaDeviceAssurancePolicy#disk_encrypted}.
        :param key_trust_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#key_trust_level DataOktaDeviceAssurancePolicy#key_trust_level}.
        :param managed_device: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#managed_device DataOktaDeviceAssurancePolicy#managed_device}.
        :param os_firewall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#os_firewall DataOktaDeviceAssurancePolicy#os_firewall}.
        :param os_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#os_version DataOktaDeviceAssurancePolicy#os_version}.
        :param password_protection_warning_trigger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#password_protection_warning_trigger DataOktaDeviceAssurancePolicy#password_protection_warning_trigger}.
        :param realtime_url_check_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#realtime_url_check_mode DataOktaDeviceAssurancePolicy#realtime_url_check_mode}.
        :param safe_browsing_protection_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#safe_browsing_protection_level DataOktaDeviceAssurancePolicy#safe_browsing_protection_level}.
        :param screen_lock_secured: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#screen_lock_secured DataOktaDeviceAssurancePolicy#screen_lock_secured}.
        :param site_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#site_isolation_enabled DataOktaDeviceAssurancePolicy#site_isolation_enabled}.
        :param third_party_blocking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#third_party_blocking_enabled DataOktaDeviceAssurancePolicy#third_party_blocking_enabled}.
        :param windows_machine_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#windows_machine_domain DataOktaDeviceAssurancePolicy#windows_machine_domain}.
        :param windows_user_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#windows_user_domain DataOktaDeviceAssurancePolicy#windows_user_domain}.
        '''
        if isinstance(browser_version, dict):
            browser_version = DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion(**browser_version)
        if isinstance(os_version, dict):
            os_version = DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion(**os_version)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89b3f1f8a4dee0aefaeed6cb0515e9767c951e3a5702a57b3835aded42312e9)
            check_type(argname="argument allow_screen_lock", value=allow_screen_lock, expected_type=type_hints["allow_screen_lock"])
            check_type(argname="argument browser_version", value=browser_version, expected_type=type_hints["browser_version"])
            check_type(argname="argument built_in_dns_client_enabled", value=built_in_dns_client_enabled, expected_type=type_hints["built_in_dns_client_enabled"])
            check_type(argname="argument chrome_remote_desktop_app_blocked", value=chrome_remote_desktop_app_blocked, expected_type=type_hints["chrome_remote_desktop_app_blocked"])
            check_type(argname="argument crowd_strike_agent_id", value=crowd_strike_agent_id, expected_type=type_hints["crowd_strike_agent_id"])
            check_type(argname="argument crowd_strike_customer_id", value=crowd_strike_customer_id, expected_type=type_hints["crowd_strike_customer_id"])
            check_type(argname="argument device_enrollment_domain", value=device_enrollment_domain, expected_type=type_hints["device_enrollment_domain"])
            check_type(argname="argument disk_encrypted", value=disk_encrypted, expected_type=type_hints["disk_encrypted"])
            check_type(argname="argument key_trust_level", value=key_trust_level, expected_type=type_hints["key_trust_level"])
            check_type(argname="argument managed_device", value=managed_device, expected_type=type_hints["managed_device"])
            check_type(argname="argument os_firewall", value=os_firewall, expected_type=type_hints["os_firewall"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
            check_type(argname="argument password_protection_warning_trigger", value=password_protection_warning_trigger, expected_type=type_hints["password_protection_warning_trigger"])
            check_type(argname="argument realtime_url_check_mode", value=realtime_url_check_mode, expected_type=type_hints["realtime_url_check_mode"])
            check_type(argname="argument safe_browsing_protection_level", value=safe_browsing_protection_level, expected_type=type_hints["safe_browsing_protection_level"])
            check_type(argname="argument screen_lock_secured", value=screen_lock_secured, expected_type=type_hints["screen_lock_secured"])
            check_type(argname="argument site_isolation_enabled", value=site_isolation_enabled, expected_type=type_hints["site_isolation_enabled"])
            check_type(argname="argument third_party_blocking_enabled", value=third_party_blocking_enabled, expected_type=type_hints["third_party_blocking_enabled"])
            check_type(argname="argument windows_machine_domain", value=windows_machine_domain, expected_type=type_hints["windows_machine_domain"])
            check_type(argname="argument windows_user_domain", value=windows_user_domain, expected_type=type_hints["windows_user_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_screen_lock is not None:
            self._values["allow_screen_lock"] = allow_screen_lock
        if browser_version is not None:
            self._values["browser_version"] = browser_version
        if built_in_dns_client_enabled is not None:
            self._values["built_in_dns_client_enabled"] = built_in_dns_client_enabled
        if chrome_remote_desktop_app_blocked is not None:
            self._values["chrome_remote_desktop_app_blocked"] = chrome_remote_desktop_app_blocked
        if crowd_strike_agent_id is not None:
            self._values["crowd_strike_agent_id"] = crowd_strike_agent_id
        if crowd_strike_customer_id is not None:
            self._values["crowd_strike_customer_id"] = crowd_strike_customer_id
        if device_enrollment_domain is not None:
            self._values["device_enrollment_domain"] = device_enrollment_domain
        if disk_encrypted is not None:
            self._values["disk_encrypted"] = disk_encrypted
        if key_trust_level is not None:
            self._values["key_trust_level"] = key_trust_level
        if managed_device is not None:
            self._values["managed_device"] = managed_device
        if os_firewall is not None:
            self._values["os_firewall"] = os_firewall
        if os_version is not None:
            self._values["os_version"] = os_version
        if password_protection_warning_trigger is not None:
            self._values["password_protection_warning_trigger"] = password_protection_warning_trigger
        if realtime_url_check_mode is not None:
            self._values["realtime_url_check_mode"] = realtime_url_check_mode
        if safe_browsing_protection_level is not None:
            self._values["safe_browsing_protection_level"] = safe_browsing_protection_level
        if screen_lock_secured is not None:
            self._values["screen_lock_secured"] = screen_lock_secured
        if site_isolation_enabled is not None:
            self._values["site_isolation_enabled"] = site_isolation_enabled
        if third_party_blocking_enabled is not None:
            self._values["third_party_blocking_enabled"] = third_party_blocking_enabled
        if windows_machine_domain is not None:
            self._values["windows_machine_domain"] = windows_machine_domain
        if windows_user_domain is not None:
            self._values["windows_user_domain"] = windows_user_domain

    @builtins.property
    def allow_screen_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#allow_screen_lock DataOktaDeviceAssurancePolicy#allow_screen_lock}.'''
        result = self._values.get("allow_screen_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def browser_version(
        self,
    ) -> typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#browser_version DataOktaDeviceAssurancePolicy#browser_version}.'''
        result = self._values.get("browser_version")
        return typing.cast(typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion"], result)

    @builtins.property
    def built_in_dns_client_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#built_in_dns_client_enabled DataOktaDeviceAssurancePolicy#built_in_dns_client_enabled}.'''
        result = self._values.get("built_in_dns_client_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def chrome_remote_desktop_app_blocked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#chrome_remote_desktop_app_blocked DataOktaDeviceAssurancePolicy#chrome_remote_desktop_app_blocked}.'''
        result = self._values.get("chrome_remote_desktop_app_blocked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crowd_strike_agent_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#crowd_strike_agent_id DataOktaDeviceAssurancePolicy#crowd_strike_agent_id}.'''
        result = self._values.get("crowd_strike_agent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def crowd_strike_customer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#crowd_strike_customer_id DataOktaDeviceAssurancePolicy#crowd_strike_customer_id}.'''
        result = self._values.get("crowd_strike_customer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_enrollment_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#device_enrollment_domain DataOktaDeviceAssurancePolicy#device_enrollment_domain}.'''
        result = self._values.get("device_enrollment_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#disk_encrypted DataOktaDeviceAssurancePolicy#disk_encrypted}.'''
        result = self._values.get("disk_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_trust_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#key_trust_level DataOktaDeviceAssurancePolicy#key_trust_level}.'''
        result = self._values.get("key_trust_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_device(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#managed_device DataOktaDeviceAssurancePolicy#managed_device}.'''
        result = self._values.get("managed_device")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def os_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#os_firewall DataOktaDeviceAssurancePolicy#os_firewall}.'''
        result = self._values.get("os_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def os_version(
        self,
    ) -> typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#os_version DataOktaDeviceAssurancePolicy#os_version}.'''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional["DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion"], result)

    @builtins.property
    def password_protection_warning_trigger(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#password_protection_warning_trigger DataOktaDeviceAssurancePolicy#password_protection_warning_trigger}.'''
        result = self._values.get("password_protection_warning_trigger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realtime_url_check_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#realtime_url_check_mode DataOktaDeviceAssurancePolicy#realtime_url_check_mode}.'''
        result = self._values.get("realtime_url_check_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def safe_browsing_protection_level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#safe_browsing_protection_level DataOktaDeviceAssurancePolicy#safe_browsing_protection_level}.'''
        result = self._values.get("safe_browsing_protection_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def screen_lock_secured(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#screen_lock_secured DataOktaDeviceAssurancePolicy#screen_lock_secured}.'''
        result = self._values.get("screen_lock_secured")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def site_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#site_isolation_enabled DataOktaDeviceAssurancePolicy#site_isolation_enabled}.'''
        result = self._values.get("site_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def third_party_blocking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#third_party_blocking_enabled DataOktaDeviceAssurancePolicy#third_party_blocking_enabled}.'''
        result = self._values.get("third_party_blocking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def windows_machine_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#windows_machine_domain DataOktaDeviceAssurancePolicy#windows_machine_domain}.'''
        result = self._values.get("windows_machine_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def windows_user_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#windows_user_domain DataOktaDeviceAssurancePolicy#windows_user_domain}.'''
        result = self._values.get("windows_user_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion",
    jsii_struct_bases=[],
    name_mapping={"minimum": "minimum"},
)
class DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion:
    def __init__(self, *, minimum: typing.Optional[builtins.str] = None) -> None:
        '''
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#minimum DataOktaDeviceAssurancePolicy#minimum}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9de7766f3ddb02aaaab42b0055b3ab94ec51a6d4e33b215a86274125d023d7a)
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minimum is not None:
            self._values["minimum"] = minimum

    @builtins.property
    def minimum(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#minimum DataOktaDeviceAssurancePolicy#minimum}.'''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f272d136122c0e705ab61ae18dc8cc09e46c4f84ba5eef3907adab248990b0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinimum")
    def reset_minimum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimum", []))

    @builtins.property
    @jsii.member(jsii_name="minimumInput")
    def minimum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumInput"))

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimum"))

    @minimum.setter
    def minimum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731bafc80f192dd1994541c7470f440459feae8530305072fdd19f193f7141b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6cdf31d971862bb798952f83dc794a47207d93b5a9005ed84e2499947ddf384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion",
    jsii_struct_bases=[],
    name_mapping={"minimum": "minimum"},
)
class DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion:
    def __init__(self, *, minimum: typing.Optional[builtins.str] = None) -> None:
        '''
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#minimum DataOktaDeviceAssurancePolicy#minimum}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e18eac13546377c65ba6f3211bfe349ae1a9c4051bdacc6f884277d3ac8347e)
            check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minimum is not None:
            self._values["minimum"] = minimum

    @builtins.property
    def minimum(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#minimum DataOktaDeviceAssurancePolicy#minimum}.'''
        result = self._values.get("minimum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e10381f6222b14050d0d0d0c5ba8ec8d23a16ea14bc9a4d50842dae45a55c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinimum")
    def reset_minimum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimum", []))

    @builtins.property
    @jsii.member(jsii_name="minimumInput")
    def minimum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumInput"))

    @builtins.property
    @jsii.member(jsii_name="minimum")
    def minimum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimum"))

    @minimum.setter
    def minimum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e9cf2523d6ee0cd8b58bd03d7e21233cdffc9906453570c2eefc0471dd1c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9a22fcaf810822b75a9eb9beb96494dcb8aa5e2b3cf5f2822256b0306fd2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb244041f89728b005c3f178dbcb2e0b8d49beb53e1bc10a210edab4ec65bf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBrowserVersion")
    def put_browser_version(
        self,
        *,
        minimum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#minimum DataOktaDeviceAssurancePolicy#minimum}.
        '''
        value = DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion(
            minimum=minimum
        )

        return typing.cast(None, jsii.invoke(self, "putBrowserVersion", [value]))

    @jsii.member(jsii_name="putOsVersion")
    def put_os_version(self, *, minimum: typing.Optional[builtins.str] = None) -> None:
        '''
        :param minimum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#minimum DataOktaDeviceAssurancePolicy#minimum}.
        '''
        value = DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion(
            minimum=minimum
        )

        return typing.cast(None, jsii.invoke(self, "putOsVersion", [value]))

    @jsii.member(jsii_name="resetAllowScreenLock")
    def reset_allow_screen_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowScreenLock", []))

    @jsii.member(jsii_name="resetBrowserVersion")
    def reset_browser_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBrowserVersion", []))

    @jsii.member(jsii_name="resetBuiltInDnsClientEnabled")
    def reset_built_in_dns_client_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuiltInDnsClientEnabled", []))

    @jsii.member(jsii_name="resetChromeRemoteDesktopAppBlocked")
    def reset_chrome_remote_desktop_app_blocked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChromeRemoteDesktopAppBlocked", []))

    @jsii.member(jsii_name="resetCrowdStrikeAgentId")
    def reset_crowd_strike_agent_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrowdStrikeAgentId", []))

    @jsii.member(jsii_name="resetCrowdStrikeCustomerId")
    def reset_crowd_strike_customer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrowdStrikeCustomerId", []))

    @jsii.member(jsii_name="resetDeviceEnrollmentDomain")
    def reset_device_enrollment_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceEnrollmentDomain", []))

    @jsii.member(jsii_name="resetDiskEncrypted")
    def reset_disk_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncrypted", []))

    @jsii.member(jsii_name="resetKeyTrustLevel")
    def reset_key_trust_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyTrustLevel", []))

    @jsii.member(jsii_name="resetManagedDevice")
    def reset_managed_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedDevice", []))

    @jsii.member(jsii_name="resetOsFirewall")
    def reset_os_firewall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsFirewall", []))

    @jsii.member(jsii_name="resetOsVersion")
    def reset_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersion", []))

    @jsii.member(jsii_name="resetPasswordProtectionWarningTrigger")
    def reset_password_protection_warning_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordProtectionWarningTrigger", []))

    @jsii.member(jsii_name="resetRealtimeUrlCheckMode")
    def reset_realtime_url_check_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealtimeUrlCheckMode", []))

    @jsii.member(jsii_name="resetSafeBrowsingProtectionLevel")
    def reset_safe_browsing_protection_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSafeBrowsingProtectionLevel", []))

    @jsii.member(jsii_name="resetScreenLockSecured")
    def reset_screen_lock_secured(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScreenLockSecured", []))

    @jsii.member(jsii_name="resetSiteIsolationEnabled")
    def reset_site_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSiteIsolationEnabled", []))

    @jsii.member(jsii_name="resetThirdPartyBlockingEnabled")
    def reset_third_party_blocking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThirdPartyBlockingEnabled", []))

    @jsii.member(jsii_name="resetWindowsMachineDomain")
    def reset_windows_machine_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsMachineDomain", []))

    @jsii.member(jsii_name="resetWindowsUserDomain")
    def reset_windows_user_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsUserDomain", []))

    @builtins.property
    @jsii.member(jsii_name="browserVersion")
    def browser_version(
        self,
    ) -> DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersionOutputReference:
        return typing.cast(DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersionOutputReference, jsii.get(self, "browserVersion"))

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(
        self,
    ) -> DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersionOutputReference:
        return typing.cast(DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersionOutputReference, jsii.get(self, "osVersion"))

    @builtins.property
    @jsii.member(jsii_name="allowScreenLockInput")
    def allow_screen_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowScreenLockInput"))

    @builtins.property
    @jsii.member(jsii_name="browserVersionInput")
    def browser_version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion]], jsii.get(self, "browserVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="builtInDnsClientEnabledInput")
    def built_in_dns_client_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "builtInDnsClientEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="chromeRemoteDesktopAppBlockedInput")
    def chrome_remote_desktop_app_blocked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "chromeRemoteDesktopAppBlockedInput"))

    @builtins.property
    @jsii.member(jsii_name="crowdStrikeAgentIdInput")
    def crowd_strike_agent_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crowdStrikeAgentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="crowdStrikeCustomerIdInput")
    def crowd_strike_customer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crowdStrikeCustomerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceEnrollmentDomainInput")
    def device_enrollment_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceEnrollmentDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptedInput")
    def disk_encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskEncryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTrustLevelInput")
    def key_trust_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyTrustLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="managedDeviceInput")
    def managed_device_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "managedDeviceInput"))

    @builtins.property
    @jsii.member(jsii_name="osFirewallInput")
    def os_firewall_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "osFirewallInput"))

    @builtins.property
    @jsii.member(jsii_name="osVersionInput")
    def os_version_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion]], jsii.get(self, "osVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordProtectionWarningTriggerInput")
    def password_protection_warning_trigger_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordProtectionWarningTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="realtimeUrlCheckModeInput")
    def realtime_url_check_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "realtimeUrlCheckModeInput"))

    @builtins.property
    @jsii.member(jsii_name="safeBrowsingProtectionLevelInput")
    def safe_browsing_protection_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "safeBrowsingProtectionLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="screenLockSecuredInput")
    def screen_lock_secured_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "screenLockSecuredInput"))

    @builtins.property
    @jsii.member(jsii_name="siteIsolationEnabledInput")
    def site_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "siteIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="thirdPartyBlockingEnabledInput")
    def third_party_blocking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "thirdPartyBlockingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsMachineDomainInput")
    def windows_machine_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowsMachineDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsUserDomainInput")
    def windows_user_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowsUserDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="allowScreenLock")
    def allow_screen_lock(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowScreenLock"))

    @allow_screen_lock.setter
    def allow_screen_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a070a126840849b6c7c274d18c260c585727800050eb436664b100e098e9cae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowScreenLock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="builtInDnsClientEnabled")
    def built_in_dns_client_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "builtInDnsClientEnabled"))

    @built_in_dns_client_enabled.setter
    def built_in_dns_client_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f4283dac226638d0961441ccd7f1bd7f36693c0129597922d09b3449b15ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtInDnsClientEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chromeRemoteDesktopAppBlocked")
    def chrome_remote_desktop_app_blocked(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "chromeRemoteDesktopAppBlocked"))

    @chrome_remote_desktop_app_blocked.setter
    def chrome_remote_desktop_app_blocked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211d03536c86714fe56ea031e6408d4b7bcd06b60ac0360803e64103f3cc3655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chromeRemoteDesktopAppBlocked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crowdStrikeAgentId")
    def crowd_strike_agent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crowdStrikeAgentId"))

    @crowd_strike_agent_id.setter
    def crowd_strike_agent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426d47fac63ab7dc2f83ee31d9ddcd4e98ba6f6d47eb6d85044171cf7dfad7fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crowdStrikeAgentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crowdStrikeCustomerId")
    def crowd_strike_customer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crowdStrikeCustomerId"))

    @crowd_strike_customer_id.setter
    def crowd_strike_customer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3b96f36a24992d0171a306de250cff8c5a84d78a83fd18ed896f1bc8df8cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crowdStrikeCustomerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceEnrollmentDomain")
    def device_enrollment_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceEnrollmentDomain"))

    @device_enrollment_domain.setter
    def device_enrollment_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799651ed93d2bbb116c4e79457d0b574d157b449255e724db756249f1e72ecac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceEnrollmentDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncrypted")
    def disk_encrypted(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskEncrypted"))

    @disk_encrypted.setter
    def disk_encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704e78b50ff6454829f3435018562916842d55a3ffeddd4154335a74b117ca5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyTrustLevel")
    def key_trust_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyTrustLevel"))

    @key_trust_level.setter
    def key_trust_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9da80ec70110953a58c1769a3f57cb7f2976885d04c1860271664aa3884f644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyTrustLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedDevice")
    def managed_device(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "managedDevice"))

    @managed_device.setter
    def managed_device(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a085ac3efc95c2573a3377a4ec0bbff73e1b934893f327d8ca40c5d305c6f13d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedDevice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osFirewall")
    def os_firewall(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "osFirewall"))

    @os_firewall.setter
    def os_firewall(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f36e591d676d0ce9634a7230f82a20810209023e981e46b6076f6454ad7ef30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osFirewall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordProtectionWarningTrigger")
    def password_protection_warning_trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordProtectionWarningTrigger"))

    @password_protection_warning_trigger.setter
    def password_protection_warning_trigger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3ce4113411bfec020b88809afd7fd17a2720ff7a385b5f7e97dba4a72d73ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordProtectionWarningTrigger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realtimeUrlCheckMode")
    def realtime_url_check_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "realtimeUrlCheckMode"))

    @realtime_url_check_mode.setter
    def realtime_url_check_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb09e73a323fbdcc66acbf353543a952acdef7ca06fc1449d44f52e7fafc87ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realtimeUrlCheckMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="safeBrowsingProtectionLevel")
    def safe_browsing_protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "safeBrowsingProtectionLevel"))

    @safe_browsing_protection_level.setter
    def safe_browsing_protection_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69aa5499f25e20ff0dca9b6a6e2c188539b71a7cb0e5ac6395cbf34e6b1a7346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "safeBrowsingProtectionLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="screenLockSecured")
    def screen_lock_secured(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "screenLockSecured"))

    @screen_lock_secured.setter
    def screen_lock_secured(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71572028ad14b66c6e13a847d5f180cc397ec14f4ab8f5a843b5f834277c15b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "screenLockSecured", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteIsolationEnabled")
    def site_isolation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "siteIsolationEnabled"))

    @site_isolation_enabled.setter
    def site_isolation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ede0fd12c79ce7b58d4bed0c3dc4ef09e0fd9fbfd153b90f60a29807a2878aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thirdPartyBlockingEnabled")
    def third_party_blocking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "thirdPartyBlockingEnabled"))

    @third_party_blocking_enabled.setter
    def third_party_blocking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4467b341ea29f3e24baa068f571b67b99cf32c2aba78b6d30aad55f7750719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thirdPartyBlockingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowsMachineDomain")
    def windows_machine_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowsMachineDomain"))

    @windows_machine_domain.setter
    def windows_machine_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f85125263b0aaa45283086c3aff170d095939b92bdbebfae371dc730b45e8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowsMachineDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowsUserDomain")
    def windows_user_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowsUserDomain"))

    @windows_user_domain.setter
    def windows_user_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35445d00f982c9f9b8c50bc6712638eb325326cf8d2c93d086ee16711f38da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowsUserDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8085f316f1448a17d09a52bf66d57ad8eba1f9f60b6468ff71f1238bb43c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataOktaDeviceAssurancePolicyThirdPartySignalProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaDeviceAssurancePolicy.DataOktaDeviceAssurancePolicyThirdPartySignalProviderOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02977a11ba2dd1e8d9daac653f0aa2e3d112c96c9511b8bace7560b91107d2a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDtc")
    def put_dtc(
        self,
        *,
        allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        browser_version: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        built_in_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crowd_strike_agent_id: typing.Optional[builtins.str] = None,
        crowd_strike_customer_id: typing.Optional[builtins.str] = None,
        device_enrollment_domain: typing.Optional[builtins.str] = None,
        disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_trust_level: typing.Optional[builtins.str] = None,
        managed_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_version: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        password_protection_warning_trigger: typing.Optional[builtins.str] = None,
        realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        safe_browsing_protection_level: typing.Optional[builtins.str] = None,
        screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        windows_machine_domain: typing.Optional[builtins.str] = None,
        windows_user_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_screen_lock: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#allow_screen_lock DataOktaDeviceAssurancePolicy#allow_screen_lock}.
        :param browser_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#browser_version DataOktaDeviceAssurancePolicy#browser_version}.
        :param built_in_dns_client_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#built_in_dns_client_enabled DataOktaDeviceAssurancePolicy#built_in_dns_client_enabled}.
        :param chrome_remote_desktop_app_blocked: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#chrome_remote_desktop_app_blocked DataOktaDeviceAssurancePolicy#chrome_remote_desktop_app_blocked}.
        :param crowd_strike_agent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#crowd_strike_agent_id DataOktaDeviceAssurancePolicy#crowd_strike_agent_id}.
        :param crowd_strike_customer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#crowd_strike_customer_id DataOktaDeviceAssurancePolicy#crowd_strike_customer_id}.
        :param device_enrollment_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#device_enrollment_domain DataOktaDeviceAssurancePolicy#device_enrollment_domain}.
        :param disk_encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#disk_encrypted DataOktaDeviceAssurancePolicy#disk_encrypted}.
        :param key_trust_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#key_trust_level DataOktaDeviceAssurancePolicy#key_trust_level}.
        :param managed_device: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#managed_device DataOktaDeviceAssurancePolicy#managed_device}.
        :param os_firewall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#os_firewall DataOktaDeviceAssurancePolicy#os_firewall}.
        :param os_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#os_version DataOktaDeviceAssurancePolicy#os_version}.
        :param password_protection_warning_trigger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#password_protection_warning_trigger DataOktaDeviceAssurancePolicy#password_protection_warning_trigger}.
        :param realtime_url_check_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#realtime_url_check_mode DataOktaDeviceAssurancePolicy#realtime_url_check_mode}.
        :param safe_browsing_protection_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#safe_browsing_protection_level DataOktaDeviceAssurancePolicy#safe_browsing_protection_level}.
        :param screen_lock_secured: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#screen_lock_secured DataOktaDeviceAssurancePolicy#screen_lock_secured}.
        :param site_isolation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#site_isolation_enabled DataOktaDeviceAssurancePolicy#site_isolation_enabled}.
        :param third_party_blocking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#third_party_blocking_enabled DataOktaDeviceAssurancePolicy#third_party_blocking_enabled}.
        :param windows_machine_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#windows_machine_domain DataOktaDeviceAssurancePolicy#windows_machine_domain}.
        :param windows_user_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.17.0/docs/data-sources/device_assurance_policy#windows_user_domain DataOktaDeviceAssurancePolicy#windows_user_domain}.
        '''
        value = DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc(
            allow_screen_lock=allow_screen_lock,
            browser_version=browser_version,
            built_in_dns_client_enabled=built_in_dns_client_enabled,
            chrome_remote_desktop_app_blocked=chrome_remote_desktop_app_blocked,
            crowd_strike_agent_id=crowd_strike_agent_id,
            crowd_strike_customer_id=crowd_strike_customer_id,
            device_enrollment_domain=device_enrollment_domain,
            disk_encrypted=disk_encrypted,
            key_trust_level=key_trust_level,
            managed_device=managed_device,
            os_firewall=os_firewall,
            os_version=os_version,
            password_protection_warning_trigger=password_protection_warning_trigger,
            realtime_url_check_mode=realtime_url_check_mode,
            safe_browsing_protection_level=safe_browsing_protection_level,
            screen_lock_secured=screen_lock_secured,
            site_isolation_enabled=site_isolation_enabled,
            third_party_blocking_enabled=third_party_blocking_enabled,
            windows_machine_domain=windows_machine_domain,
            windows_user_domain=windows_user_domain,
        )

        return typing.cast(None, jsii.invoke(self, "putDtc", [value]))

    @jsii.member(jsii_name="resetDtc")
    def reset_dtc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDtc", []))

    @builtins.property
    @jsii.member(jsii_name="dtc")
    def dtc(
        self,
    ) -> DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOutputReference:
        return typing.cast(DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOutputReference, jsii.get(self, "dtc"))

    @builtins.property
    @jsii.member(jsii_name="dtcInput")
    def dtc_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc]], jsii.get(self, "dtcInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProvider]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProvider]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProvider]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514eaa8dfef8e0347dd07492c5c19d920a0c11e20d5785ec10a4e384a85215d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOktaDeviceAssurancePolicy",
    "DataOktaDeviceAssurancePolicyConfig",
    "DataOktaDeviceAssurancePolicyDiskEncryptionType",
    "DataOktaDeviceAssurancePolicyDiskEncryptionTypeOutputReference",
    "DataOktaDeviceAssurancePolicyOsVersion",
    "DataOktaDeviceAssurancePolicyOsVersionConstraint",
    "DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement",
    "DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirementOutputReference",
    "DataOktaDeviceAssurancePolicyOsVersionConstraintList",
    "DataOktaDeviceAssurancePolicyOsVersionConstraintOutputReference",
    "DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement",
    "DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirementOutputReference",
    "DataOktaDeviceAssurancePolicyOsVersionOutputReference",
    "DataOktaDeviceAssurancePolicyScreenlockType",
    "DataOktaDeviceAssurancePolicyScreenlockTypeOutputReference",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProvider",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersionOutputReference",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersionOutputReference",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOutputReference",
    "DataOktaDeviceAssurancePolicyThirdPartySignalProviderOutputReference",
]

publication.publish()

def _typecheckingstub__5b3abb5b7a942ac7114f3a37018de45309c6edd37c571ce00e3ac05c7b15b026(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    third_party_signal_provider: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fae8c13833973db89fd4ac631b484c6112e34131dde2aab8e47eaa968f2c6e7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a9298c7c78d16dce947aadd506dd4d6a8d1a04c19e7a726dbe47bebb8dd481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88b0a5ab20b94083c3c31d3d99270d1bcf645ea2651ffbd39efe92f3ec11c56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b898c2036f73790df6168d98cce3aa3367e0dab0f8d99eaab316cd7041acee7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d391b99ae8cf8b05207466fc1ba0269b9e1acf9e1feee088ba372c0a8cb5c09a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    third_party_signal_provider: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProvider, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57795250cdf956a14a41b416d2594510268617ce62e18f8189f8b67f77143ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973bc0751868d03cfa213ec8998cedf11941f3ddadbd6f08f5f8b9e232e45ca9(
    value: typing.Optional[DataOktaDeviceAssurancePolicyDiskEncryptionType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f59485af704b8ecea7b62aab476ea5816f5a72ae2103a5e1ad9820f2a80cdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abafa2c8d6227d3975d265574b2ed76a87445a4f815f88cbfa5b0ab638d1a7ef(
    value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraintDynamicVersionRequirement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710c707032de612da97fcd699e23aa2c8b694131fad871a553bc5defa5c85c93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f424a439486359df3d5cb1bdd42971e5aa0c866af02a525fd3a8ec6388d0fd01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe6c0907c53346ec9874ef44b42dcded8c7b4f1e5fcb9f6aa8b4acd6b62453e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d18cdc08df0a4b063fcaf148631af7ea30c43fe2b8fd0d1119dcedd78bc057(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ca8fc02a6fb4a262b59658d8c1415165cbd79b4d79e76aabb2e8480aa356bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a841490dc094aa87096e2f1029a4c868131870566b0f87e580e7cb4fbe39f8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94aec4bcf6f5ae9fd901aab399eb006dfa957bf63128f7e03390f24943ab27a8(
    value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersionConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504294a014fc028054888be3baf91fafb8a0deca95c4b9a9f0d1a9fad060b4f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d8cff87880b09fcc1ddc2747246eb29568b4c3485cd45194cfe1d4820839ee(
    value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersionDynamicVersionRequirement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0510efc7b2470e3715dbee30e1e97d59c356e9a40625600d63807e1f825bb5b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0ebbf4417565909dd7162e1cdab42739930dbe18daf98df3f7900b922bf183(
    value: typing.Optional[DataOktaDeviceAssurancePolicyOsVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9c3105122ed8d03fcb1d498bb0053195d0771f8ada51d3814a3c5ee7e7243d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce69388a0624be061e6ec444cc7c60294448920399822472501357d8a849a68(
    value: typing.Optional[DataOktaDeviceAssurancePolicyScreenlockType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436e865f5ff1ac82b9ec22323565fdd5d338fae6f6b4cc4632784920ca1f80e2(
    *,
    dtc: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89b3f1f8a4dee0aefaeed6cb0515e9767c951e3a5702a57b3835aded42312e9(
    *,
    allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    browser_version: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    built_in_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crowd_strike_agent_id: typing.Optional[builtins.str] = None,
    crowd_strike_customer_id: typing.Optional[builtins.str] = None,
    device_enrollment_domain: typing.Optional[builtins.str] = None,
    disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_trust_level: typing.Optional[builtins.str] = None,
    managed_device: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_version: typing.Optional[typing.Union[DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    password_protection_warning_trigger: typing.Optional[builtins.str] = None,
    realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    safe_browsing_protection_level: typing.Optional[builtins.str] = None,
    screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    windows_machine_domain: typing.Optional[builtins.str] = None,
    windows_user_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9de7766f3ddb02aaaab42b0055b3ab94ec51a6d4e33b215a86274125d023d7a(
    *,
    minimum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f272d136122c0e705ab61ae18dc8cc09e46c4f84ba5eef3907adab248990b0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731bafc80f192dd1994541c7470f440459feae8530305072fdd19f193f7141b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cdf31d971862bb798952f83dc794a47207d93b5a9005ed84e2499947ddf384(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcBrowserVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e18eac13546377c65ba6f3211bfe349ae1a9c4051bdacc6f884277d3ac8347e(
    *,
    minimum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e10381f6222b14050d0d0d0c5ba8ec8d23a16ea14bc9a4d50842dae45a55c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e9cf2523d6ee0cd8b58bd03d7e21233cdffc9906453570c2eefc0471dd1c25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9a22fcaf810822b75a9eb9beb96494dcb8aa5e2b3cf5f2822256b0306fd2bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtcOsVersion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb244041f89728b005c3f178dbcb2e0b8d49beb53e1bc10a210edab4ec65bf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a070a126840849b6c7c274d18c260c585727800050eb436664b100e098e9cae7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f4283dac226638d0961441ccd7f1bd7f36693c0129597922d09b3449b15ca2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211d03536c86714fe56ea031e6408d4b7bcd06b60ac0360803e64103f3cc3655(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426d47fac63ab7dc2f83ee31d9ddcd4e98ba6f6d47eb6d85044171cf7dfad7fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3b96f36a24992d0171a306de250cff8c5a84d78a83fd18ed896f1bc8df8cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799651ed93d2bbb116c4e79457d0b574d157b449255e724db756249f1e72ecac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704e78b50ff6454829f3435018562916842d55a3ffeddd4154335a74b117ca5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9da80ec70110953a58c1769a3f57cb7f2976885d04c1860271664aa3884f644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a085ac3efc95c2573a3377a4ec0bbff73e1b934893f327d8ca40c5d305c6f13d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f36e591d676d0ce9634a7230f82a20810209023e981e46b6076f6454ad7ef30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3ce4113411bfec020b88809afd7fd17a2720ff7a385b5f7e97dba4a72d73ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb09e73a323fbdcc66acbf353543a952acdef7ca06fc1449d44f52e7fafc87ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69aa5499f25e20ff0dca9b6a6e2c188539b71a7cb0e5ac6395cbf34e6b1a7346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71572028ad14b66c6e13a847d5f180cc397ec14f4ab8f5a843b5f834277c15b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ede0fd12c79ce7b58d4bed0c3dc4ef09e0fd9fbfd153b90f60a29807a2878aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4467b341ea29f3e24baa068f571b67b99cf32c2aba78b6d30aad55f7750719(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f85125263b0aaa45283086c3aff170d095939b92bdbebfae371dc730b45e8bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35445d00f982c9f9b8c50bc6712638eb325326cf8d2c93d086ee16711f38da8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8085f316f1448a17d09a52bf66d57ad8eba1f9f60b6468ff71f1238bb43c1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProviderDtc]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02977a11ba2dd1e8d9daac653f0aa2e3d112c96c9511b8bace7560b91107d2a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514eaa8dfef8e0347dd07492c5c19d920a0c11e20d5785ec10a4e384a85215d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataOktaDeviceAssurancePolicyThirdPartySignalProvider]],
) -> None:
    """Type checking stubs"""
    pass
