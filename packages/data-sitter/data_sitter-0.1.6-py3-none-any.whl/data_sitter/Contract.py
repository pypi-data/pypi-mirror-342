import json
import yaml
from typing import Any, Dict, List, NamedTuple
from functools import cached_property

from pydantic import BaseModel

from .Validation import Validation
from .field_types import BaseField
from .FieldResolver import FieldResolver
from .rules import ProcessedRule, RuleRegistry, RuleParser


class ContractWithoutFields(Exception):
    pass


class ContractWithoutName(Exception):
    pass


class Field(NamedTuple):
    name: str
    type: str
    rules: List[str]


class Contract:
    name: str
    fields: List[Field]
    rule_parser: RuleParser
    field_resolvers: Dict[str, FieldResolver]


    def __init__(self, name: str, fields: List[Field], values: Dict[str, Any]) -> None:
        self.name = name
        self.fields = fields
        self.rule_parser = RuleParser(values)
        self.field_resolvers = {
            _type: FieldResolver(RuleRegistry.get_type(_type), self.rule_parser)
            for _type in list({field.type for field in self.fields})  # Unique types
        }

    @classmethod
    def from_dict(cls, contract_dict: dict):
        if "name" not in contract_dict:
            raise ContractWithoutName()
        if "fields" not in contract_dict:
            raise ContractWithoutFields()

        return cls(
            name=contract_dict["name"],
            fields=[Field(**field) for field in contract_dict["fields"]],
            values=contract_dict.get("values", {}),
        )

    @classmethod
    def from_json(cls, contract_json: str):
        return cls.from_dict(json.loads(contract_json))

    @classmethod
    def from_yaml(cls, contract_yaml: str):
        return cls.from_dict(yaml.load(contract_yaml, yaml.Loader))

    @cached_property
    def field_validators(self) -> Dict[str, BaseField]:
        field_validators = {}
        for field in self.fields:
            field_resolver = self.field_resolvers[field.type]
            field_validators[field.name] = field_resolver.get_field_validator(field.name, field.rules)
        return field_validators

    @cached_property
    def rules(self) -> Dict[str, List[ProcessedRule]]:
        rules = {}
        for field in self.fields:
            field_resolver = self.field_resolvers[field.type]
            rules[field.name] = field_resolver.get_processed_rules(field.rules)
        return rules

    def validate(self, item: dict) -> Validation:
        return Validation.validate(self.pydantic_model, item)

    @cached_property
    def pydantic_model(self) -> BaseModel:
        return type(self.name, (BaseModel,), {
            "__annotations__": {
                name: field_validator.get_annotation()
                for name, field_validator in self.field_validators.items()
            }
        })

    @cached_property
    def contract(self) -> dict:
        return {
            "name": self.name,
            "fields": [
                {
                    "name": name,
                    "type": field_validator.type_name.value,
                    "rules": [rule.parsed_rule for rule in self.rules.get(name, [])]
                }
                for name, field_validator in self.field_validators.items()
            ],
            "values": self.rule_parser.values
        }

    def get_json_contract(self, indent: int=2) -> str:
        return json.dumps(self.contract, indent=indent)

    def get_yaml_contract(self, indent: int=2) -> str:
        return yaml.dump(self.contract, Dumper=yaml.Dumper, indent=indent, sort_keys=False)

    def get_front_end_contract(self) -> dict:
        return {
            "name": self.name,
            "fields": [
                {
                    "name": name,
                    "type": field_validator.type_name.value,
                    "rules": [
                        rule.get_front_end_repr()
                        for rule in self.rules.get(name, [])
                    ]
                }
                for name, field_validator in self.field_validators.items()
            ],
            "values": self.rule_parser.values
        }
